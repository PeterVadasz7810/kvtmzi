from locators import VetitesekPageLocators, KonyvatarMoziURLs
from vetitesobj import Vetites


class VetitesekPage(object):

    def __init__(self, webdrv, libraries, date_from='', date_to=''):
        self.__list_of_events = []
        self.__list_of_libraries = libraries
        self.date_from = date_from
        self.date_to = date_to
        self.browser = webdrv
        self.browser.implicitly_wait(10)
        self.browser.get(KonyvatarMoziURLs.vetitesek)

        self.__get_site_data()

    def __get_site_data(self):
        tmp_list = []
        # site_datas_soron_kovetkezo = self.browser.find_elements(*VetitesekPageLocators.l_kovetkezo_vetitesek_table)
        site_datas_elmult = self.browser.find_elements(*VetitesekPageLocators.l_elmult_vetites_table)
        for row in site_datas_elmult.find_elements_by_tag_name('tr'):
            for cell in row.find_elements_by_tag_name('td'):
                tmp_list.append(cell.text)
            tmp_list[1] = tmp_list[1].split(' ', 1)[0]
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
        pass

    def get_list_of_events_to(self, date_to=''):
        pass

    def get_list_of_events_from_to(self, date_from='', date_to=''):
        pass
