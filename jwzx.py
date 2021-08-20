from login import Login
from course import Course
from marjor import Major
from studen_status_infomation import StudentStatusInfomation
from empty_classroom import EmptyClassroom
from common import *


class JWZX(Login, Course, Major, StudentStatusInfomation, EmptyClassroom):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_current_semester():
        return get_current_semester()

    @staticmethod
    def get_semester(year, month):
        return get_semester(year, month)

    @staticmethod
    def get_semester_map():
        return get_semester_map()
