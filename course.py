import re
from common import *


class Course(object):
    def __init__(self) -> None:
        super().__init__()
        # 分析出学年和学期对应的代码
        self.RE_FOR_SEMESTER_STEP_1 = r'{\s*id\s*:\s*[0-9]*,[\s\S]*?"[\s\S]*?",\s*name\s*:\s*"[0-9]"'
        self.RE_FOR_SEMESTER_STEP_2 = r'{\s*id\s*:\s*([0-9]*),[\s\S]*?"([\s\S]*?)",\s*name\s*:\s*"([0-9])"'

        # self.RE_FOR_CURRENT_WEEK = r'#FFD460;\S*>[\S\s]*?第[0-9]*?周'
        # 获取当前的教学周
        self.RE_FOR_CURRENT_WEEK = r'第\s*<strong>([0-9]*)\s*</strong>\s*教学周'

        # 获取所有课的代码中分离出每一节课
        self.RE_FOR_COURSE_JS_CODE = r'var\s?teachers\s=[\s\S]*?\]\s*=\s*activity[\s\S]*?\]\s*=\s*activity'

        # Step1：分离教师名字 Step2：处理多个老师授课的情况
        self.RE_FOR_TEACHER_NAME_STEP_1 = r'var\s*teachers\s*=\s*\[([\s\S]*?)]'
        self.RE_FOR_TEACHER_NAME_STEP_2 = r'name\s*:\s*"(\S*?)"'

        # 返回 课程名字和代码 教学楼 教学周
        self.RE_FOR_COURSE_INFO = r"activity\s*=\s*new\s*TaskActivity\s*\(\s*actTeacherId.join\(',""'\)\s*,\s*actTeacherName.join\(','\)"'\s*,\s*"\S*?"\s*,\s*"(\S*?)"\s*,\s*"\S*?"\s*,\s*"(\S*?)"\s*,\s*"(\S*?)"\s*'
        self.RE_FOR_IDS = r"if\(jQuery\(\"#courseTableType\"\).val\(\)==\"std\"\)[\s\S]*?ids\",\"([\s\S]*?)\""
        self.RE_FOR_WITCH_DAY_AND_CLASS = r'index\s*?=\s*?([0-9])[\s\S]*?([0-9])'
        # 从课程名字和代码中分离课程名字
        self.RE_FOR_COURSE_NAME_IN_COURSE_INFO = r'([\s\S]*)\('

        self.URL_SCHOOL_CALENDAR = 'http://202.199.224.119:8080/eams/schoolCalendar!search.action'
        self.URL_COURSES = 'http://202.199.224.119:8080/eams/courseTableForStd!courseTable.action'
        self.URL_SEMESTER = 'http://202.199.224.119:8080/eams/homeExt!main.action'
        self.URL_SEMESTER_MAP_PREREQUISTIES = 'http://202.199.224.119:8080/eams/schoolCalendar.action'
        self.URL_SEMESTER_MAP_DATA = 'http://202.199.224.119:8080/eams/dataQuery.action'

    def get_current_week_course_data(self) -> list:

        semester = get_current_semester()

        return self.get_course_data(semester, self.get_current_week(semester_id=semester))

    def get_current_semester_course_data(self):
        """
        返回当前学期的全部课程信息
        """
        return self.get_course_data(get_current_semester(), None)

    def get_current_week(self) -> str:
        """
        返回当前的周数
        """
        html = get_context(self.URL_SEMESTER)
        return re.compile(self.RE_FOR_CURRENT_WEEK).search(html).group(1)

    def get_course_data(self, semester, week=None) -> list:
        """
        获取课程信息，需要提供semester 和 周数，可用get_semester获取semester
        Parmas:

        """
        params = {
            'ignoreHead': 1,
            "setting.kind": 'std',  # 这个参数决定了ids
            'startWeek': week,
            'project.id': '1',
            'semester.id': semester,
            'ids': self.__get_course_ids()  # IDS，写在HOME.action
        }
        html = get_context(self.URL_COURSES, params=params)
        data = self.__parse_course_data(html)
        return data

    def __parse_course_data(self, html):
        """
        Get datas from backend template,
        Return:
            [
                {
                    'class_start_end':,
                    'teacher':,
                    'course_code':,
                    'class_location':,
                    'day_and_class':,
                        {
                            'day':,
                            'class':,
                        }
                }
            ]
        """
        datas = []
        split_codes = re.compile(self.RE_FOR_COURSE_JS_CODE).findall(html)
        for code in split_codes:
            one_class = {}
            teacher_code = re.compile(
                self.RE_FOR_TEACHER_NAME_STEP_1).search(code).group(1)
            teacher = re.compile(
                self.RE_FOR_TEACHER_NAME_STEP_2).findall(teacher_code)
            teacher = '、'.join(teacher)
            course_info = re.compile(
                self.RE_FOR_COURSE_INFO).search(code).groups()
            course_code, class_loaction, class_start_end = course_info
            course_name = re.compile(
                self.RE_FOR_COURSE_NAME_IN_COURSE_INFO).search(course_code).group(1)
            which_day, which_class = re.compile(
                self.RE_FOR_WITCH_DAY_AND_CLASS).search(code).groups()

            # 临时的解析周的方法
            # TODO(3122971650@qq.com) Use other elegant mothods to prase the class' start and end week
            start = class_start_end.find('1')
            end = (len(class_start_end)-1-class_start_end[::-1].find('1'))
            class_start_end = (start, end)

            one_class['duration'] = class_start_end
            one_class['teacher'] = teacher
            one_class['course'] = course_name
            one_class['address'] = class_loaction
            one_class['time'] = {
                'week': int(which_day)+1, 'section': (int(which_class)+2)//2}
            datas.append(one_class)
        return datas

    def __get_course_ids(self):
        """
        在获取课程数据的时候要用的id
        """
        html = get_context(
            'http://202.199.224.119:8080/eams/courseTableForStd.action')
        return re.compile(self.RE_FOR_IDS).search(html).group(1)
