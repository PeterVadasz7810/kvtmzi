from selenium.webdriver.common.by import By


class VetitesekPageLocators(object):
    '''
    A http://konyvtarmozi.hu/vetitesek.aspx oldalhoz tartozó lokátorok
    '''
    l_elmult_vetites_table = (By.ID, 'ctl00_ContentPlaceHolder1_GridViewElmult')
    l_kovetkezo_vetitesek_table = (By.ID, 'ctl00_ContentPlaceHolder1_GridViewVetitesek')


class PillanatkepekPageLocators(object):
    '''
    A http://konyvtarmozi.hu/kepesProgram.aspx oldalhoz tartozó lokátorok
    '''
    l_kepes_vetitesek_table = (By.ID, 'ctl00_ContentPlaceHolder1_GridViewVetitesek')


class Letszam_rogzitesePageLocators(object):
    '''
    A http://konyvtarmozi.hu/letszam.aspx oldalhoz tartozó lokátorok
    '''
    l_film_dropdown_list = (By.ID, 'ctl00_ContentPlaceHolder1_DropDownListFilm')
    l_intezmeny_dropdown_list = (By.ID, 'ctl00_ContentPlaceHolder1_DropDownListKonyvtar')
    l_kivalaszt_btn_locators = (By.XPATH, '//input[@type="button" and @value="Kiválaszt"]')
    l_azonosito_locator = (By.ID, 'ctl00_ContentPlaceHolder1_LabelID')
    l_gyerek_input_locator = (By.ID, 'ctl00_ContentPlaceHolder1_TextBoxGyerek')
    l_felnott_input_locator = (By.ID, 'ctl00_ContentPlaceHolder1_TextBoxFelnott')
    l_nagyi_input_locator = (By.ID, 'ctl00_ContentPlaceHolder1_TextBoxNagyi')
