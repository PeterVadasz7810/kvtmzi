import operator
from selenium.webdriver.common.by import By
from datetime import datetime as DT
from locators import VetitesekPageLocators, KonyvatarMoziURLs
from vetitesobj import Vetites
import filmobj
import libraryobj


class VetitesekPage(object):

    def __init__(self, webdrv, libraries, date_from='2015-10-05', date_to=''):
        self.__base_date = DT.strptime('2015-10-05', '%Y-%m-%d')
        sortkey = operator.attrgetter('date')
        self.__list_of_events = []
        self.__filtered_list_of_events = []
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

        site_datas_elmult = self.browser.find_element(*VetitesekPageLocators.l_elmult_vetites_table)
        
        for row in site_datas_elmult.find_elements(By.TAG_NAME, 'tr')[1:]:  # because the first row contains th elements
            cells = row.find_elements(By.TAG_NAME, 'td')

            # if not relevant, throw it 
            if not (self.date_from <= DT.strptime(cells[2].text, '%Y.%m.%d. %H:%M:%S') <= self.date_to):
                continue

            # if not relevant, throw it
            if cells[1].text.split(' ', 1)[0].strip() not in self.__list_of_libraries:
                continue

            for x, cell in enumerate(cells):
                if (x == 0) or (x == 1):
                    id = cell.find_element(By.TAG_NAME, 'a').get_attribute('href').split('=')[1].strip()
                if x == 0:
                    film = filmobj.Film(cell.text, id)
                    tmp_list.append(film)
                elif x == 1:
                    lib = libraryobj.Library(cell.text, cell.text.split(' ', 1)[0].strip(), id)
                    tmp_list.append(lib)
                else:
                    tmp_list.append(cell.text)

            vetites = Vetites(*tmp_list)
            self.__list_of_events.append(vetites)
            tmp_list.clear()

    def get_date_from(self) -> DT:
        return self.date_from

    def get_date_to(self) -> DT:
        return self.date_to

    def get_list_of_all_events(self) -> list:
        return self.__list_of_events

    def get_list_of_events(self, date_from='', date_to='') -> list:
        tmp_date = DT.now()
        if date_from != '':
            self.set_date_from(date_from)
        if date_to != '':
            self.set_date_to(date_to)
        if self.date_from > self.date_to:
            tmp_date = self.date_to
            self.date_to = self.date_from
            self.date_from = tmp_date

        self.__filtered_list_of_events.clear()
        self.__filtered_list_of_events = list(
            filter(lambda event: self.date_from <= event.date <= self.date_to, self.__list_of_events))
        return self.__filtered_list_of_events

    def get_number_of_all_events(self) -> int:
        return len(self.__list_of_events)

    def get_number_of_filtered_events(self) -> int:
        return len(self.__filtered_list_of_events)

    def set_date_from(self, date_from):
        if self.__base_date > DT.strptime(date_from, '%Y-%m-%d'):
            self.date_from = self.__base_date
        else:
            self.date_from = DT.strptime(date_from, '%Y-%m-%d')

    def set_date_to(self, date_to):
        if self.__base_date > DT.strptime(date_to, '%Y-%m-%d'):
            self.date_to = self.__base_date
        else:
            self.date_to = DT.strptime(date_to, '%Y-%m-%d')
