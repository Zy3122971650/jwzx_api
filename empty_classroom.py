from common import *
from bs4 import BeautifulSoup

url_query_empty_classroom = 'http://202.199.224.119:8080/eams/classroom/occupy/class-details!unitDetail.action?semesterId={semester}&iWeek={week}&room.building.id={id}'


class EmptyClassroom(object):
    def __init__(self) -> None:
        super().__init__()
        self.room_building_id_map = {
            '博文楼': 7, '博雅楼': 13, '新华楼': 19, '中和楼': 17, '致远楼': 18, '知行楼': 8, '物理实验室': 15, '主楼机房': 9, '尔雅楼': 20, '静远楼': 11, '葫芦岛物理实验室': 16, '葫芦岛机房': 21, '耘慧楼': 14}

    def construct_url(self, semester, week, id):
        return url_query_empty_classroom.format(semester=semester, week=week, id=id)

    def get_empty_classrooms(self, building_name, semester, week):
        data = []
        building_id = self.room_building_id_map[building_name]
        url = self.construct_url(semester=semester, week=week, id=building_id)
        html = get_context(url)
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find(class_='table-b')

        # headers = [i.string for i in table.find('tr').find_all('td')]
        headers = ['classroom', 'capacity', 'type', 'Mon',
                   'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        trs = table.find_all('tr')[1:]
        for tr in trs:
            temp = {}
            tds = tr.find_all('td')
            for i in range(len(tds)):
                if tds[i].string == None:
                    temp[headers[i]] = list(tds[i].stripped_strings)
                else:
                    temp[headers[i]] = tds[i].string
            data.append(temp)
        return data
