from selenium.webdriver.common.by import By


class KonyvatarMoziURLs(object):
    vetitesek = "http://konyvtarmozi.hu/vetitesek.aspx"
    letszam = "http://konyvtarmozi.hu/letszam.aspx"
    fotok = "http://konyvtarmozi.hu/kepesProgram.aspx"


class CommonLocator(object):
    '''
    Ez az ID több oldalon is előfordul ezért kiemelem
    '''
    _l_common_locator = (By.ID, 'ctl00_ContentPlaceHolder1_GridViewVetitesek')


class VetitesekPageLocators(CommonLocator):
    '''
    A http://konyvtarmozi.hu/vetitesek.aspx oldalhoz tartozó lokátorok
    '''
    l_elmult_vetites_table = (By.ID, 'ctl00_ContentPlaceHolder1_GridViewElmult')
    l_kovetkezo_vetitesek_table = CommonLocator._l_common_locator


class PillanatkepekPageLocators(CommonLocator):
    '''
    A http://konyvtarmozi.hu/kepesProgram.aspx oldalhoz tartozó lokátorok
    '''

    l_kepes_vetitesek_table = CommonLocator._l_common_locator


class LetszamRogzitesePageLocators(CommonLocator):
    '''
    A http://konyvtarmozi.hu/letszam.aspx oldalhoz tartozó lokátorok
    '''
    l_film_dropdown_list = (By.ID, 'ctl00_ContentPlaceHolder1_DropDownListFilm')
    l_intezmeny_dropdown_list = (By.ID, 'ctl00_ContentPlaceHolder1_DropDownListKonyvtar')
    l_vetites_valaszto_table = CommonLocator._l_common_locator
    l_kivalaszt_btn_locators = (By.XPATH, '//input[@type="button" and @value="Kiválaszt"]')
    l_vetites_datuma_locators = (By.XPATH, '//table[@id="ctl00_ContentPlaceHolder1_GridViewVetitesek"]//td[2]')
    l_felvezeto_vendeg_locators = (By.XPATH, '//table[@id="ctl00_ContentPlaceHolder1_GridViewVetitesek"]//td[3]')
    l_azonosito_locator = (By.ID, 'ctl00_ContentPlaceHolder1_LabelID')
    l_gyerek_input_locator = (By.ID, 'ctl00_ContentPlaceHolder1_TextBoxGyerek')
    l_felnott_input_locator = (By.ID, 'ctl00_ContentPlaceHolder1_TextBoxFelnott')
    l_nagyi_input_locator = (By.ID, 'ctl00_ContentPlaceHolder1_TextBoxNagyi')
