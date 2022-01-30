from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime as DT
from locators import LetszamRogzitesePageLocators, KonyvatarMoziURLs
from letszamobj import Letszam


class LetszamPage(object):

    def __init__(self, webdrv):
        self.browser = webdrv
        self.browser.implicitly_wait(10)
        self.browser.get(KonyvatarMoziURLs.letszam)

    def __select_dropdown(self, locator, value):
        dropdown = Select(self.browser.find_element(*locator))
        dropdown.select_by_value(value)

    def __choose_button(self, date, guest):
        btn = -1
        vetites_valaszto_tabla = WebDriverWait(self.browser, 30).until(
            EC.visibility_of_element_located(LetszamRogzitesePageLocators.l_vetites_valaszto_table))

        for row in vetites_valaszto_tabla.find_elements(By.TAG_NAME, 'tr')[1:]:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if (DT.strptime(cells[1].text, '%Y.%m.%d. %H:%M:%S') == date) and (
                    cells[2].text == guest):
                btn = cells[0].find_element(By.TAG_NAME, 'input')
        return btn

    def get_letszam(self, event):
        self.__select_dropdown(LetszamRogzitesePageLocators.l_film_dropdown_list, event.film.id)
        sleep(2)

        self.__select_dropdown(LetszamRogzitesePageLocators.l_intezmeny_dropdown_list, event.library.id)
        sleep(2)

        btn_kivalaszt = self.__choose_button(event.date, event.guest)

        if btn_kivalaszt != -1:
            btn_kivalaszt.click()
            vetites_id = self.browser.find_element(*LetszamRogzitesePageLocators.l_azonosito_locator).text
            gyerek = self.browser.find_element(*LetszamRogzitesePageLocators.l_gyerek_input_locator).get_attribute(
                'value')
            felnott = self.browser.find_element(
                *LetszamRogzitesePageLocators.l_felnott_input_locator).get_attribute(
                'value')
            nagyi = self.browser.find_element(*LetszamRogzitesePageLocators.l_nagyi_input_locator).get_attribute(
                'value')
            return Letszam(event, vetites_id, gyerek, felnott, nagyi)
        else:
            return -1
