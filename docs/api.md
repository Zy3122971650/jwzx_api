# API 文档

## common

### get_context
用途：
对requests使用get后获取text的封装

### post_context
用途：
对requests使用post后获取text的封装

### get_semester
用途：
获取传入年月所对应的学期代码，用在需要传入semester的方法中

参数:
- year(int)
- month(int)

返回：
- (string):对应的semester id
## Login

### login
用途：
登录到教务在线

参数：
- username(string):用于登录的账号
- passwd(string):用于登录的密码

返回：
- None

例子：
```python
    from jwzx import JWZX
    jwzx = JWZX()
    jwzx.login(username='', passwd='')
```

### keep_login（未测试）
用途：
模拟刷新保持教务在线的登录状态

参数：
- None

返回：
- None

例子：
- None

### parse_key_salt

用途：
利用正则提取本次登录应该加入密码的盐

参数：
- html(string):获取的 HTML 文档

返回：
- salt(string):加入密码中的盐

例子：
- None

### sha1_password
用途：
利用 sha1 算法加密密码

参数：
- password(string):加过盐的密码

返回：
- (string):sha1 摘要

例子：
- None

## Exam

### get_exam_time
用途：
返回所查询年月对应付的学期的考试安排信息

参数：
- year(string):要查询的年
- month(string):要查询的月
- _type(string):可选'0'或'1'，'0'代表正常考试信息，'1'代表补考信息

返回：
- data(list[dict]):包含所查询年月对应付的学期的考试安排信息的 Python 对象，详见例子

例子：
```python
    from jwzx import JWZX
    jwzx = JWZX()
    jwzx.login(username='', passwd='')
    # 获取2021年，6月份对应学期的正常考试信息，也就是第二学期（这个设计是让我们不需要思考到底是第几学年）
    print(jwzx.get_exam_time(2021, 6, '0'))
"""
[
    {'课程序号': 'H181700001032.02', '课程名称': '网络店铺装修与推广', '考试类别': '期末考试', '考试日期': '2021-07-07', '考试安排': '14:00~16:00', '考试地点': '静远楼202', '考试情况': '正常', '其它说明': ''},
    {'课程序号': 'H181730012016.01', '课程名称': '互联网思维', '考试类别': '期末考试', '考试日期': '时间未安排', '考试安排': '时间未安排', '考试地点': '地点未安排', '考试情况': '正常', '其它说明': ''},
    {'课程序号': 'H271700001040.05', '课程名称': '线性代数', '考试类别': '期末考试', '考试日期': '2021-06-04', '考试安排': '19:00~21:00', '考试地点': '尔雅楼209', '考试情况': '正常', '其它说明': ''},
]
"""
```

### get_exam_grades
用途：
返回所查询年月对应付的学期的考试成绩信息

参数：
- year(string):要查询的年
- month(string):要查询的月

返回：
- data(list[dict]):包含所查询年月对应付的学期的考试成绩信息的 Python 对象，详见例子

例子：
```python
    from jwzx import JWZX
    jwzx = JWZX()
    jwzx.login(username='', passwd='')
    # 获取2021年，6月份对应学期的考试成绩信息，也就是第二学期的考试成绩信息（这个设计是让我们不需要思考到底是第几学年）
    print(jwzx.get_exam_grades(2021, 6))
"""
[
    {'学年学期': '2020-2021 2', '课程代码': 'H271780001016', '课程序号': 'H271780001016.08', '课程名称': '大学生职业生涯规划', '课程类别': '专业课', '学分': '0.5', '期末成绩': '合格', '平时成绩': 'None', '总评成绩': '合格', '最终': '合格', '绩点': '0', '查卷申请': 'None'},
    {'学年学期': '2020-2021 2', '课程代码': 'H271700001040', '课程序号': 'H271700001040.05', '课程名称': '线性代数', '课程类别': '专业课', '学分': '2.5', '期末成绩': '75', '平时成绩': '30', '总评成绩': '83', '最终': '83', '绩点': '0', '查卷申请': 'None'}
]
"""
```

### get_gpa
用途：
获取每个学年的绩点以及汇总绩点

参数：
- None

返回：
- data(list[dict]):包含获取每个学年的绩点以及汇总绩点的 Python 对象，详见例子

例子：
```python
    from jwzx import JWZX
    jwzx = JWZX()
    jwzx.login(username='', passwd='')
    # 获取每个学年的绩点以及汇总绩点
    print(jwzx.get_gpa())
"""
[
    {'学年度': '2020-2021', '学期': '2', '门数': '13', '总学分': '27.5', '平均绩点': '2.5182'},
    {'在校汇总': '在校汇总', '学期': '13', '门数': '27.5', '总学分': '2.5182'}
]
"""
```

### __get_exam_batch_id_map
用途：
获取查询类型和请求代码的映射

参数：
- semester(string):学期代码

返回：
- data_map(dict):查询类型和请求代码的映射

例子：
- None

## Course

### get_current_week_course_data
用途：
获取当前周的课程信息，简单装封get_course_data方法

参数：
- None

返回：
- (list[dict]): 包含所查询当前周课程信息的 Python 对象,详见get_course_data

例子：
- None

### get_current_semester_course_data
用途：
获取当前学期的课程信息，简单装封get_course_data方法

参数：
- None

返回：
- (list[dict]): 包含所查询当前学期课程信息的 Python 对象,详见get_course_data

例子：
- None

### get_course_data
用途：
获取当前指定的课程信息

参数：
- semester(string):所查询学期的id，可使用get_semester获得，详见get_semester
- week(string|None):传入所要查询的周，默认返回学期课表

返回：
- (list[dict]): 包含所查询指定课程信息的 Python 对象，详见例子

例子：
```python
from jwzx import JWZX

jwzx = JWZX()
jwzx.login(username='', passwd='')
print(jwzx.get_course_data(jwzx.get_semester(2021, 6)))
"""
[
    {'class_start_end': (5,5), 'teacher': '郑淑艳、万君、杨佳欣、马江平、李坤、谢涛', 'course_code': '互联网思维', 'class_location': '静远楼211', 'day_and_class': {'day': '2', 'class': '6'}},
    {'class_start_end': (2,17), 'teacher': '鄢文宏', 'course_code': '思想道德修养与法律基础', 'class_location': '尔雅楼103', 'day_and_class': {'day': '1', 'class': '0'}}
]

class_start_end:(起始周，结束周)
day_and_class: {'day': '1', 'class': '0'}，第几天，第几节课，下标从0开始，课按小节计算
"""
```

###  get_current_week
用途：
获取当前是第几教学周

参数：
- None

返回：
- (string):当前教学周

例子：
- None

### __parse_course_data
用途：
解析教务在线发来的后台模板生成的课程信息

参数：
- html(string):后台传来的HTML文档

返回：
- datas(list[dict]):就是get_course_data方法返回的数据

###  __get_course_ids
用途：
解析嵌入在courseTableForStd.action中的必须请求参数

参数：
- None

返回：
- (string):请求用的course_id

例子：
- None



## StudentStatusInfomation

### get_student_infomations
用途：
获取学籍等信息

参数：
- None

返回：
- data(dict)

例子：
```python
from jwzx import JWZX

jwzx = JWZX()
jwzx.login(username='', passwd='')
print(jwzx.get_student_infomations())
“”“
{'学号': '', '姓名': '', '英文名': '', '性别': '', '年级': '', '学制': '', '项目': '', '学历层次': '', '学生类别': '本科4年', '院系': '营销管理学院', '专业': '电子商务', '方向': None, '入校时间': '2020-09-01', '毕业时间': '2024-07-01', '行政管理院系': '营销管理学院', '学习形式': '普通全日制', '是否在籍': '是', '是否在校': '是', '所属校区': '辽宁工大葫芦岛校区', '所属班级': '', '学籍生效日期': '2020-09-01', '是否有学籍': '是', '学籍状态': '在校', '是否在职': '否', '备注': None, '电子邮件': '3122971650@qq.com', '联系电话': '', '移动电话': None, '联系地址': '', '家庭电话': None, '家庭地址': '', '家庭地址邮编': None, '火车站': '', '家庭信息': [{'家庭成员': '', '与本人关系': '父母', '监护人': '是', '证件类型': '身份证', '证件号码': '', '联系电话': '', '工作单位': '', '工作邮编': '', '工作地址': ''}, {'家庭成员': '', '与本人关系': '父母', '监护人': '是', '证件类型': '身份证', '证件号码': '', '联系电话': '', '工作单位': '', '工作邮编': '', '工作地址': ''}]}

”“”
```

## EmptyClassroom

### construct_url
用途：
构造请求url

参数：
- semester:所查询学期的代码
- week：所查询的教学周
- id：所查询教学楼的id

返回：
- url

### get_empty_classroom
用途：
获取教室的占用信息

参数：
- building_name(string):教学楼的名字，如尔雅楼
- semester：所要查询的学期id
- week:所查询的教学周

返回：
- data([dict]):所查询教学楼对应教学周的全部教室占用信息

例子：
```python
from jwzx import JWZX

jwzx = JWZX()
jwzx.login(username='', passwd='')
print(jwzx.get_empty_classrooms('尔雅楼', jwzx.get_semester(2021, 6), 1))

"""
[{'classroom': '尔雅楼101', 'capacity': '320', 'type': '多媒体教室', 'Mon': ['2', '3', '4'], 'Tue': ['1', '2', '3', '4', '5', '6', '7', '8'], 'Wed': ['9', '10'], 'Thu': ['5', '6', '7', '8'], 'Fri': ['1', '2', '3', '4', '5', '6'], 'Sat': ['1', '2', '3', '5', '6'], 'Sun': ['1', '2', '3']}, {'classroom': '尔雅楼103', 'capacity': '200', 'type': '多媒体教室', 'Mon': ['5', '6', '7', '8'], 'Tue': ['5', '6'], 'Wed': ['5', '6', '7', '8'], 'Thu': ['5', '6', '7', '8', '9', '10'], 'Fri': ['1', '2', '7', '8', '9', '10'], 'Sat': ['5', '6'], 'Sun': ['1', '2', '3']}, {'classroom': '尔雅楼104', 'capacity': '200', 'type': '多媒体教室', 'Mon': ['5', '6', '7', '8'], 'Tue': ['5', '6'], 'Wed': ['5', '6', '7', '8'], 'Thu': ['3', '4', '9', '10'], 'Fri': ['1', '2'], 'Sat': [], 'Sun': ['1', '2', '3', '4']}, ......]

"""
```