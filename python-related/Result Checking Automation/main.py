from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


# - - - - - - - - - - - - - - - - - - - - - - - - ALL X-PATH VALUES - - - - - - - - - - - - - - - - - - - - - - - - - -
PLUS_BUTTON_XPATH = '//*[@id="contentarea"]/table/tbody/tr[4]/td[1]/table/tbody/tr[4]/td[1]/a/img'
FIRST_YEAR_BUTTON_XPATH = '//*[@id="menu_hon_result"]/table/tbody/tr[1]/td[3]/a'
SEARCH_BUTTON_XPATH = '//*[@id="indivisul"]/table/tbody/tr[7]/td/input'
# - - - - - - - - - - - - - - - - - - - - - - - - ALL X-PATH VALUES - - - - - - - - - - - - - - - - - - - - - - - - - -


driver = webdriver.Chrome()
driver.get("http://103.113.200.7/")

title = driver.title
driver.implicitly_wait(0.5)


def search_result():
    plus_button = driver.find_element(by=By.XPATH, value=PLUS_BUTTON_XPATH)
    driver.execute_script("arguments[0].click();", plus_button)
    
    first_year_button = driver.find_element(by=By.XPATH, value=FIRST_YEAR_BUTTON_XPATH)
    driver.execute_script("arguments[0].click();", first_year_button)
    
    exam_roll_input = driver.find_element(by=By.ID, value='roll_number')
    exam_roll_input.send_keys('2320495')
    
    registration_input = driver.find_element(by=By.ID, value='reg_no')
    registration_input.send_keys('21220091703')
    
    year_entry_input = driver.find_element(by=By.ID, value='year_1st')
    year_entry_input.send_keys('2022')
    sleep(10)
    
    search_button = driver.find_element(by=By.XPATH, value=SEARCH_BUTTON_XPATH)
    driver.execute_script("arguments[0].click();", search_button)


if __name__ == "__main__":
    search_result()
    sleep(10)
    driver.quit()
