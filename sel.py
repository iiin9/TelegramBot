"""Connect to torgi.gov.ru and search SEARCH_TEXT"""
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

SEARCH_TEXT = "WDC1660231A139768"


def web_search(search_text=SEARCH_TEXT):
    options = Options()
    options.headless = True
    driver = Firefox(options=options)
    driver.get("https://torgi.gov.ru/lotSearch1.html?bidKindId=13")
    element = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div/div[3]/div[2]/div/div[1]/div"
        "/div/div/div/div/div/div/form/table/tbody/tr[4]/td[2]/input"
    )
    element.send_keys(search_text)
    driver.find_element_by_xpath('//*[@id="lot_search"]').click()
    WebDriverWait(driver, 60).until(
        ec.invisibility_of_element((By.CSS_SELECTOR, "#over"))
    )
    elements = driver.find_elements_by_css_selector(".datarow")
    elem_val = ""
    index = 1
    for element in elements:
        items = element.find_elements_by_css_selector(".datacell")
        elem_val += f"*{index}:* {items[3].text}\n_{items[4].text}_\n"
        index += 1
    driver.quit()

    return elem_val
