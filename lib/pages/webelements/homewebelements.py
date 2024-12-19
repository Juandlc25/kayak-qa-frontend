from selenium.webdriver.common.by import By


class HomeWebElements:
    where_label = (By.XPATH, "//span[normalize-space()='Compara cientos de webs a la vez']")
    signin_button = (By.XPATH, "//div[@class='J-sA']//div[@role='button']")
    search_button = (By.XPATH, "//button[@aria-label='Buscar']")

    name_type = (By.XPATH, "//span[@class='gPDR-logo-image-compact']")
    name_tag_input = (By.XPATH, "//div[@role='listitem']")
    name_dropdown_column_input = (By.XPATH, "//div[@class='pM26 pM26-mod-multi-value']//div[@class='xAR_ xAR_-mod-padding-x-base xAR_-mod-taller-l MT35']")
    search_tag_input = (By.XPATH, "//input[@aria-label='Origen']")

    menu_dropdown = (By.XPATH, "(//div[@aria-label='Abrir navegación principal'])[1]")
    flights_dropdown_menu_option = (By.CSS_SELECTOR, "a[aria-label='Buscar vuelos '] div[class='dJtn-menu-item-title']")
    stays_dropdown_menu_option = (By.XPATH, "//div[@class='dJtn-menu-item-title'][normalize-space()='Alojamientos']")
    cars_dropdown_menu_option = (By.XPATH, "//div[@class='dJtn-menu-item-title'][normalize-space()='Carros']")
    blog_dropdown_menu_option = (By.XPATH, "//div[normalize-space()='Blog']")
    direct_dropdown_menu_option = (By.XPATH, "//div[normalize-space()='Vuelos directos']")
    trips_dropdown_menu_option = (By.XPATH, "//div[contains(text(),'Trips')]")


