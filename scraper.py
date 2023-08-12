import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import text_dad

def get_current_hour():
    # Get the current date and time
    current_datetime = datetime.now()

    # Get the current hour from the datetime object
    current_hour = current_datetime.hour
    current_minute = current_datetime.minute
    #if less than 15 after the hour, we will still look at the current hour
    if current_minute <= 15:
        return current_hour - 1
    return current_hour
  

def get_starting_row(hour):
    if hour < 8:
        return 0
    diff = hour + 1 - 8
    total = 6 * diff
    if hour == 17:
        return total + 2
    elif hour >= 18:
        #scrape the next day
        return 0
    return total

def get_to_court_sheet():

    driver = webdriver.Safari('/Users/samreisner/Desktop/Tennis_Scraper/chromedriver')  # Optional argument, if not specified will search path.

    driver.get('https://saltaire.chelseareservations.com/');

    input_field = driver.find_element(By.NAME, 'UsernameTextBox')
    input_field.send_keys("326")
    #input_field.send_keys(Keys.RETURN)


    input_field = driver.find_element(By.NAME, "PasswordTextBox")

    input_field.send_keys("TennisMan68")
    input_field.send_keys(Keys.RETURN)
    time.sleep(3)


    #ans = driver.find_elements(By.CLASS_NAME, 'dx-content dxm-hasText dx')
    ans = driver.find_element(By.CSS_SELECTOR, 'a[href="TNReviewCourtSheet.aspx"]')

    link = "https://saltaire.chelseareservations.com/tennis/TNReviewCourtSheet.aspx"
    driver.get(link)
    return driver

def get_today_sheet(driver):
    display_button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.NAME, "btnDisplay")))
    display_button.click()
    time.sleep(1)
    return driver
  
def get_tomorrow_sheet(driver):
    choose_tomorrow = driver.find_element(By.XPATH, '//*[@id="ddlPlaydate"]/option[2]')
    choose_tomorrow.click()
    time.sleep(3)
    display_button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.NAME, "btnDisplay")))
    display_button.click()
    time.sleep(1)
    return driver

def scrape_table(driver, starting_row):
    courts_found = 0
    court_time = []
    row = 2 + starting_row
    name = 4
    #68 rows in the whole table
    while row < 4:
        xpath = "//*[@id='GridView2']/tbody/tr[{}]/td[4]".format(row)
        row_data = driver.find_element(By.XPATH, xpath)
        print(row_data.text)
        if len(row_data.text) > 1:
            time.sleep(4)
        else:
            xpath = "//*[@id='GridView2']/tbody/tr[{}]/td[1]".format(row)
            court_time.append(driver.find_element(By.XPATH, xpath).text)
            courts_found += 1
        row += 1
    return courts_found, court_time

def main():
    hour = get_current_hour()
    starting = get_starting_row(hour)
    #every hour is +6 rows (except 5 & 6)
    driver = get_to_court_sheet()
    driver = get_today_sheet(driver)
    courts_found_today, times_today = scrape_table(driver, starting)
    get_tomorrow_sheet(driver)
    courts_found_tom, times_tom = scrape_table(driver, 0)
    print(courts_found_today, courts_found_tom)
    #need to edit this
    if courts_found_today + courts_found_tom > 0:
        text_dad.send_message()
    


if __name__ == "__main__":
    main()

