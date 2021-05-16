"""Connect toiframe.inguru.ru and search SEARCH_TEXT"""
import re
import sys

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def search(search_text):
    options = Options()
    options.headless = True
    driver = Firefox(options=options)
    data_dict = {}
    try:
        # driver.get(f'https://iframe.inguru.ru/kalkulyator_osago_first#calculation=10&license={search_text}')
        driver.get("https://iframe.inguru.ru/")
        driver.find_element_by_xpath(
            '//*[@id="__main__"]/div[1]/div[1]/div/div[' "4]/form/div/div/input"
        ).send_keys(search_text + "\ue007")
        cur_url = driver.current_url
        WebDriverWait(driver, 60).until(ec.invisibility_of_element((By.CLASS_NAME, "react-loading-skeleton")))
        driver.find_element_by_class_name("button").click()
        WebDriverWait(driver, 60).until(ec.invisibility_of_element((By.CLASS_NAME, "css-1vmnjpn-skeletonStyles-Skeleton")))
        if cur_url == driver.current_url:
            error = driver.find_element_by_css_selector(".error span:nth-child(" "1) > span").text
            raise Exception(f"Не указан параметр:{error}")
        element = driver.find_element_by_xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div/div').text
        data_dict['Марка'] = element
        print(element)
        element = driver.find_element_by_xpath('/html/body/div[2]/div/main/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div/div').text
        data_dict['Модель'] = element
        print(element)
        elements = driver.find_elements_by_css_selector('[class = "form-el__content valid filled"]')
        for el in elements:
            a = el.find_element_by_css_selector(
                'span > span:nth-child(1)').get_attribute('textContent')
            b = el.find_element_by_css_selector('input').get_attribute('value').replace(" ", "")
            print(f'{a}:{b}')
            data_dict[a] = b
        answer = f"<code><b>{data_dict['Госномер']}</b></code>\n{data_dict['Марка']}, {data_dict['Модель']}, {data_dict['Год выпуска']} года, {data_dict['Мощность, л.с.']} л.с.\nVIN: <code>{data_dict['Номер VIN']}</code>\nСТС: <code>{data_dict['Серия и номер СТС']}</code>\nДата выдачи СТС: {data_dict['Дата выдачи СТС']}"
        return answer

    except BaseException as ex:
        print(ex, sys.exc_info()[0])
        return "Error"
    finally:
        driver.quit()


if __name__ == "__main__":
    while True:
        gosnomer = input('Введите номер:\n')
        if gosnomer == '0':
            gosnomer = "Е202ТУ197"
        if not re.fullmatch(r"[А, В, Е, К, М, Н, О, Р, С, Т, У, Х]\d\d\d[А, В, Е, К, М, Н, О, Р, С, Т, У, Х]{2}\d{2,3}", gosnomer):
            print("Номер не распознан")
            continue
        print("...")
        print(search(gosnomer))
