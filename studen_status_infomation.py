from common import *
from bs4 import BeautifulSoup

URL_STUDENT_STATUS_INFOMATION = 'http://202.199.224.119:8080/eams/stdDetail.action'


class StudentStatusInfomation(object):
    def get_student_infomations(self):
        data = {}
        html = get_context(URL_STUDENT_STATUS_INFOMATION)
        soup = BeautifulSoup(html, 'lxml')
        # 学籍信息和联系信息中的部分信息 （两者提取方法一样
        table_1, table_2 = soup.find_all(class_='infoTable')
        tds = table_1.find_all('td') + table_2.find_all('td')
        count = 0
        tds_len = len(tds)
        while(count < tds_len):
            if 'class' in tds[count].attrs.keys():
                if 'title' in tds[count]['class']:
                    title = tds[count].string[:-1]  # 去掉冒号
                    data[title] = tds[count+1].string
                    count += 1
            count += 1
        # 联系信息其他部分
        table = soup.find(class_='infoContactTable')
        headers = [td.string for td in table.find('tr').find_all('td')]
        familay_info_tds = table.find_all('td')[len(headers):]  # 剔除headers
        familay_info_lst = []
        for i in range(len(familay_info_tds)//len(headers)):
            temp = {}
            for j in range(len(headers)):
                temp[headers[j]] = familay_info_tds[len(headers)*i + j].string
            familay_info_lst.append(temp)
        data['家庭信息'] = familay_info_lst
        return data
