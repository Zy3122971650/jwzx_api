from common import *


class Major(object):
    def __init__(self) -> None:
        super().__init__()
        self.CHANGE_MAJOR_URL = 'http://202.199.224.119:8080/eams/stdApply.action'

    def get_change_major_data(self):
        html = get_context(self.CHANGE_MAJOR_URL)
        return self.parse_change_major_data(html)

    def parse_change_major_data(self, html):
        data = []
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table', class_='table table-hover table-bordered')
        table_tbody = table.find('tbody')
        table_tbody_items = table_tbody.find_all('tr')
        for table_tbody_item in table_tbody_items:
            td_tags = table_tbody_item.find_all('td')
            temp_dict = {}
            temp_dict['major'] = td_tags[1].string
            temp_dict['college'] = td_tags[0].string
            temp_dict['current'] = int(td_tags[3].string)
            temp_dict['plan'] = int(td_tags[4].string)
            data.append(temp_dict)
        data.sort(key=self.sort_change_major_data, reverse=True)
        return data

    def sort_change_major_data(self, item):
        if item['current'] == 0:
            return 0.01/item['plan']
        else:
            return item['current']/item['plan']
