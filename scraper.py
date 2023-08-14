
 import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService


import csv
import text_dad

def open_file():
    file = open('/Users/samreisner/Desktop/Tennis_Scraper/courts.csv') 
    writer = csv.writer(file)
    return writer
    
def read_file():
    all_courts = []
    file = open_file()
    csvreader = csv.reader(file)
    next(csvreader)
    for row in csvreader:
        all_courts.append(row)
    file.close()
    return all_courts

def write_to_file(data):
    file = open_file()
    for row in data:
        file.writerow(row)    
    file.close()

def delete_file():
    f = open('/Users/samreisner/Desktop/Tennis_Scraper/courts.csv', "w")
    f.truncate()
    f.close()

def all_openings(court_data, courts, times, day):
    all_openings = []
    for i in range(court_data):
        time = str(int(times[i].split(':')[0]))
        court = str(int(courts[i]))
        lst = [time, court, day]
        all_openings.append(lst)
    return all_openings
 
def send_messages(court_data, courts, times, day):
    for i in range(court_data):
        time = str(int(times[i].split(':')[0]))
        court = courts[i]
        message = "Court " + court + " is available " + day +  " at " + time
        print(message)
        text_dad.send_message(message)

def find_unique(sent_courts, all_courts): 
    unique = [item for item in all_courts if item not in sent_courts]
    return unique

def get_current_hour():
    # Get the current date and time
    current_datetime = datetime.now()

    # Get the current hour from the datetime object
    current_hour = current_datetime.hour
    current_minute = current_datetime.minute
    #if less than 15 after the hour, we will still look at the current hour
    if current_minute < 15:
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
        return 68
    return total

def get_to_court_sheet():
    driver_path = '/Users/samreisner/Desktop/Tennis_Scraper/chromedriver'
    chrome_service = ChromeService(driver_path)
    driver = webdriver.Chrome(service=chrome_service)

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
    courts = []
    row = 2 + starting_row
    name = 4
    #68 rows in the whole table
    while row < 40:
        xpath = "//*[@id='GridView2']/tbody/tr[{}]/td[4]".format(row)
        row_data = driver.find_element(By.XPATH, xpath)
        #print(row_data.text)
        if len(row_data.text) > 1:
            time.sleep(1)
        else:
            xpath = "//*[@id='GridView2']/tbody/tr[{}]/td[1]".format(row)
            court_time.append(driver.find_element(By.XPATH, xpath).text)
            xpath = "//*[@id='GridView2']/tbody/tr[{}]/td[3]".format(row)
            courts.append(driver.find_element(By.XPATH, xpath).text)
            courts_found += 1
        row += 1
    return courts_found, court_time, courts

def main():
    hour = get_current_hour()
    starting = get_starting_row(hour)
    #every hour is +6 rows (except 5 & 6)
    driver = get_to_court_sheet()
    #driver = get_today_sheet(driver)
    #courts_found_today, times_today = scrape_table(driver, starting)
    get_tomorrow_sheet(driver)
    courts_found_tom, times_tom, courts_tom = scrape_table(driver, 0)

    sent_courts = read_file()
    #all_openings_today = all_openings(courts_found_t, courts, times_tom, 'today')

    all_openings_tomorrow = all_openings(courts_found_tom, courts_tom, times_tom, 'tomorrow')
    #all_openings_today = all_openings(courts_found_t, courts, times_tom, 'today')

    print(sent_courts, all_openings_tomorrow)
    courts_to_send = find_unique(sent_courts, all_openings_tomorrow)
    print(courts_to_send)
    #delete_file()
    write_to_file(courts_to_send)
    
    #after 7, everyday erase the file

if __name__ == "__main__":
    main()
