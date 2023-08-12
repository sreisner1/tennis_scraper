import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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
display_button = driver.find_element(By.NAME, "btnDisplay")
display_button.click()
time.sleep(2)
row = 2
name = 4
#68 rows in the whole table
while row < 5:
    xpath = "//*[@id='GridView2']/tbody/tr[{}]/td[4]".format(row)

    row_data = driver.find_element(By.XPATH, xpath)
    print(row_data.text)
    if len(row_data.text) > 1:
        time.sleep(4)
        row += 1
    else:
        print("found a court")
print("No Courts :(")
