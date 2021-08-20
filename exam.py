import re
from bs4 import BeautifulSoup
from common import *


class Exam(object):

    def __init__(self) -> None:
        super().__init__()
        self.URL_EXAM_TABLE = 'http://202.199.224.119:8080/eams/stdExamTable.action'
        self.URL_EXAM_TIME = 'http://202.199.224.119:8080/eams/stdExamTable!examTable.action'
        self.URL_EXAM_GRADE = 'http://202.199.224.119:8080/eams/teach/grade/course/person!search.action'
        self.URL_EXAM_ALL_GRADE_AND_GPA = 'http://202.199.224.119:8080/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR'

        self.RE_EXAM_BATCH_ID = '<option\s*?value=\"(\S*?)\"\s*?[\s\S]*?>([\S\s]*?)</option>'

    def get_exam_time(self, year, month, _type):
        _type = str(_type)
        semester = get_semester(year, month)
        exam_batch_id_map = self.__get_exam_batch_id_map(semester)
        exam_batch_id = exam_batch_id_map[_type]

        params = (
            ('examBatch.id', exam_batch_id),
            ('_', str(time.time())),
        )
        txt = get_context(self.URL_EXAM_TIME, params=params)

        soup = BeautifulSoup(txt, 'lxml')
        rows = soup.find_all('tr')
        header = rows[0].find_all('th')
        header = [s.string for s in header]
        context = rows[1:]
        data = []
        for item in context:
            temp = {}
            tds = item.find_all('td')
            for i in range(len(tds)):
                # TODO (3122971650@qq.com) 可能弄成用数字表示
                temp[header[i]] = str(tds[i].string).strip()
            data.append(temp)
        return data

    def __get_exam_batch_id_map(self, semester=None):
        data_map = {}
        data = None
        if not semester == None:
            data = {
                'semester.id': semester
            }
        txt = post_context(self.URL_EXAM_TABLE, data=data)
        # 获取无效数据的时候抛出异常
        eles = re.compile(self.RE_EXAM_BATCH_ID).findall(txt)
        for ele in eles:
            value, _type = ele
            if '补考' in _type:
                _type = '1'
            else:
                _type = '0'
            data_map[_type] = value

        return data_map

    def get_exam_grades(self, year, month):
        semester = get_semester(year, month)
        params = (
            ('semesterId', semester),
            ('projectType', ''),
            ('_', time.time()),
        )
        txt = get_context(self.URL_EXAM_GRADE, params=params)
        soup = BeautifulSoup(txt, 'lxml')
        rows = soup.find_all('tr')
        header = rows[0].find_all('th')
        header = [s.string for s in header]
        context = rows[1:]
        data = []
        for item in context:
            temp = {}
            tds = item.find_all('td')
            for i in range(len(tds)):
                # TODO (3122971650@qq.com) 可能弄成用数字表示
                temp[header[i]] = str(tds[i].string).strip()
            data.append(temp)
        return data

    def get_gpa(self):
        txt = post_context(self.URL_EXAM_ALL_GRADE_AND_GPA)
        soup = BeautifulSoup(txt, 'lxml')
        # find默认找到第一个table
        table = soup.find('table')
        rows = table.find_all('tr')[:-1]  # 剔除统计时间（无关数据）
        header = rows[0].find_all('th')
        header = [s.string for s in header]
        context = rows[1:]
        data = []
        for item in context:
            temp = {}
            # 处理学期数据
            tds = item.find_all('td')
            for i in range(len(tds)):
                # TODO (3122971650@qq.com) 可能弄成用数字表示
                temp[header[i]] = str(tds[i].string).strip()
            # 处理汇总数据
            ths = item.find_all('th')
            for i in range(len(ths)):
                # TODO (3122971650@qq.com) 可能弄成用数字表示
                if i == 0:
                    temp['在校汇总'] = str(ths[i].string).strip()
                else:
                    temp[header[i]] = str(ths[i].string).strip()

            if temp != {}:
                data.append(temp)
        return data
