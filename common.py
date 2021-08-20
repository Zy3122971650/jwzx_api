import requests
import time
import re

URL_SEMESTER = 'http://202.199.224.119:8080/eams/homeExt!main.action'
URL_SEMESTER_MAP_PREREQUISTIES = 'http://202.199.224.119:8080/eams/schoolCalendar.action'
URL_SEMESTER_MAP_DATA = 'http://202.199.224.119:8080/eams/dataQuery.action'
RE_FOR_SEMESTER_STEP_1 = r'{\s*id\s*:\s*[0-9]*,[\s\S]*?"[\s\S]*?",\s*name\s*:\s*"[0-9]"'
RE_FOR_SEMESTER_STEP_2 = r'{\s*id\s*:\s*([0-9]*),[\s\S]*?"([\s\S]*?)",\s*name\s*:\s*"([0-9])"'
RE_FOR_CURRENT_WEEK = r'第\s*<strong>([0-9]*)\s*</strong>\s*教学周'

r = requests.session()

fake_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.38 Safari/537.36 Edg/91.0.864.19',
    'Upgrade-Insecure-Requests': '1',
}


def get_context(url: str, headers=None, params=None, cookie=None) -> str:
    if not headers:
        headers = fake_headers
    else:
        headers.update(fake_headers)
    if cookie:
        r.cookies.update(cookie)

    context = r.get(url, headers=headers, params=params).text
    time.sleep(0.5)
    return context


def post_context(url: str, data=None, headers=None):
    if not headers:
        headers = fake_headers
    else:
        headers.update(fake_headers)
    context = r.post(url, data=data, headers=headers).text
    time.sleep(0.5)
    return context


def get_semester_map():
    """
    获取可选学年和学期对应的id
    """
    r.get(URL_SEMESTER_MAP_PREREQUISTIES)
    header = {
        'Accept': 'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://202.199.224.119:8080/eams/schoolCalendar.action'

    }

    post_data = {
        'tagId': 'semesterBar17461306361Semester',
        'dataType': 'semesterCalendar',
        'value': '662',
        'empty': 'false'
    }
    data = post_context(
        URL_SEMESTER_MAP_DATA, data=post_data, headers=header)
    datas = re.compile(RE_FOR_SEMESTER_STEP_1).findall(data)
    semester_map = {}
    for item in datas:
        semester_id, school_year, semester = re.compile(
            RE_FOR_SEMESTER_STEP_2).search(item).groups()
        semester_map[school_year+'-'+semester] = semester_id
    return semester_map


def get_current_semester():
    """
    通过时间推测现在是第几学期
    """
    tm = time.localtime()
    year = tm[0]
    month = tm[1]
    return get_semester(year, month)


def get_semester(year, month):
    """
    通过输入的年和月得到对应学年和学期所对应的id
    """
    if month < 9:
        semester_year = "%s-%s" % (year-1, year)
        semester = '2'
    else:
        semester_year = "%s-%s" % (year, year+1)
        semester = '1'
    # key由学年-学期构成，例如2020-2021-1，就是2020-2021学年，第一学期
    key = semester_year + '-' + semester
    semester_map = get_semester_map()
    return semester_map[key]


def get_current_week(self) -> str:
    """
    返回当前的周数
    """
    html = get_context(URL_SEMESTER)
    return re.compile(RE_FOR_CURRENT_WEEK).search(html).group(1)
