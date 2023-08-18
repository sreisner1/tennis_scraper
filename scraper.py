import time
from datetime import datetime, timedelta

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
    file = open('/Users/samreisner/Desktop/Tennis_Scraper/courts.csv', 'w', newline='') 

    writer = csv.writer(file)
    return writer

def is_empty_file():
    with open('/Users/samreisner/Desktop/Tennis_Scraper/courts.csv', 'r') as file:
        return not any(csv.reader(file))  # Check if any rows exist  
      
def read_file():
    if is_empty_file():
        return []
    file = open('/Users/samreisner/Desktop/Tennis_Scraper/courts.csv') 
    csvreader = csv.reader(file)
    all_courts = []
    for row in csvreader:
        all_courts.append(row)
    file.close()
    return all_courts

def write_to_file(data):
    writer = open_file()
    for row in data:
        print(row)
        writer.writerow(row)    

def delete_file():
    f = open('/Users/samreisner/Desktop/Tennis_Scraper/courts.csv', "w")
    f.truncate()
    f.close()

def all_openings(court_data, courts, times):
    all_openings = []
    for i in range(court_data):
        time = str(int(times[i].split(':')[0]))
        court = str(int(courts[i]))
        lst = [time, court]
        all_openings.append(lst)
    return all_openings
 
def send_messages(court_data):
    for i in range(len(court_data)):
        time = court_data[i][0]
        court = court_data[i][1]
        message = "Court " + court + " is available today at " + time
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

def after_seven():
    curr_hour = get_current_hour()
    if curr_hour >= 19:
        delete_file()
        return True 
    return False
  

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
    #driver_path = '/Users/samreisner/Desktop/Tennis_Scraper/chromedriver'
    #chrome_service = ChromeService(driver_path)

    # driver = webdriver.Chrome(ChromeDriverManager(version="114.0.5735.90").install())

    driver = webdriver.Safari()
    
    #driver.set_page_load_timeout(10)  # 10 seconds

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
    # Find the table element using its tag name ('table')
    table = driver.find_element(By.TAG_NAME, 'table')

    # Find all the rows within the table using the 'tr' tag
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # The number of rows is the length of the 'rows' list
    num_rows = len(rows)

    row = 2 + starting_row

    while row < num_rows + 1:
        xpath = "//*[@id='GridView2']/tbody/tr[{}]/td[4]".format(row)
        row_data = driver.find_element(By.XPATH, xpath)
        #print(row_data.text)
        if row_data.text == " " or row_data.text == None:
            xpath = "//*[@id='GridView2']/tbody/tr[{}]/td[1]".format(row)
            court_time.append(driver.find_element(By.XPATH, xpath).text)
            xpath = "//*[@id='GridView2']/tbody/tr[{}]/td[3]".format(row)
            courts.append(driver.find_element(By.XPATH, xpath).text)
            courts_found += 1
        else:
            time.sleep(1)
        row += 1
    return courts_found, court_time, courts

def run_program():
    print("Running program ...") 
    
    #add an output file
    
    #csv file is structed as: time, court
    if after_seven():
        print("After 7. Turn on tomorrow")
        return False
    hour = get_current_hour()

    starting = get_starting_row(hour)
    #every hour is +6 rows (except 5 & 6)
    driver = get_to_court_sheet()
    driver = get_today_sheet(driver)
    num_courts_found, times, courts_today = scrape_table(driver, starting)
    sent_courts = read_file()
    all_openings_today = all_openings(num_courts_found, courts_today, times)
    courts_to_send = find_unique(sent_courts, all_openings_today)
    print("These are the open courts, ", courts_to_send)
    send_messages(courts_to_send)
    write_to_file(courts_to_send)
    driver.quit()

    
def main():
    run_program()
    
    
if __name__ == "__main__":
    main()

    
