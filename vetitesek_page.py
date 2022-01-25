import operator
from selenium.webdriver.common.by import By
from datetime import datetime as DT
from locators import VetitesekPageLocators, KonyvatarMoziURLs
from vetitesobj import Vetites


class VetitesekPage(object):

    def __init__(self, webdrv, libraries, date_from='2015-10-05', date_to=''):
        self.__base_date = DT.strptime('2015-10-05', '%Y-%m-%d')
        sortkey = operator.attrgetter('date')
        self.__list_of_events = []
        self.__list_of_libraries = libraries
        self.date_from = DT.strptime(date_from, '%Y-%m-%d')
        if date_to == '':
            self.date_to = DT.now()
        else:
            self.date_to = DT.strptime(date_to, '%Y-%m-%d')
        self.browser = webdrv
        self.browser.implicitly_wait(10)
        self.browser.get(KonyvatarMoziURLs.vetitesek)
        self.__get_site_data()

        self.__list_of_events.sort(key=sortkey, reverse=False)

    def __get_site_data(self):
        tmp_list = []
        # site_datas_soron_kovetkezo = self.browser.find_elements(*VetitesekPageLocators.l_kovetkezo_vetitesek_table)
        site_datas_elmult = self.browser.find_element(*VetitesekPageLocators.l_elmult_vetites_table)
        for row in site_datas_elmult.find_elements(By.TAG_NAME, 'tr')[1:]: # because the first row contains th elements
            for cell in row.find_elements(By.TAG_NAME, 'td'):
                tmp_list.append(cell.text)
            tmp_list[1] = tmp_list[1].split(' ', 1)[0].strip()
            if tmp_list[1] in self.__list_of_libraries:
                vetites = Vetites(*tmp_list)
                self.__list_of_events.append(vetites)
            tmp_list.clear()

    def get_date_from(self):
        return self.date_from

    def get_date_to(self):
        return self.date_to

    def get_list_of_all_events(self):
        return self.__list_of_events

    def get_list_of_events_from(self, date_from=''):
        if date_from != '':
            self.set_date_from(date_from)
        return filter(lambda event: event.date >= self.date_from, self.__list_of_events)

    def get_list_of_events_to(self, date_to=''):
        if date_to != '':
            self.set_date_to(date_to)
        return filter(lambda event: event.date <= self.date_to, self.__list_of_events)

    def get_list_of_events_from_to(self, date_from='', date_to=''):
        if date_from != '':
            self.set_date_from(date_from)
        if date_to != '':
            self.set_date_to(date_to)
        return filter(lambda event: self.date_from <= event.date <= self.date_to, self.__list_of_events)

    def get_number_of_all_events(self):
        return len(self.__list_of_events)

    def set_date_from(self, date_from):
        '''TODO: date_from nem lehet nagyobb a mai nap -1 nap és nem lehet kisebb mint a __base_date'''
        self.date_from = DT.strptime(date_from, '%Y-%m-%d')

    def set_date_to(self, date_to):
        '''TODO: date_to nem lehet kisebb mint a __base_date +1 nap és nem lehet nagyobb mint a mai nap'''
        self.date_to = DT.strptime(date_to, '%Y-%m-%d')
