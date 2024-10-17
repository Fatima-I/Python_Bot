import pandas as pd
from selenium import webdriver
import time
import re
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

sheet_id = '1Ii3g9GzR8_X3ZWXuR7vGLbjWnUECwDFuQyOPFw9_khU'
sheet_name = "Form Data"
gid = '0'

read = pd.read_csv('https://docs.google.com/spreadsheets/d/1Ii3g9GzR8_X3ZWXuR7vGLbjWnUECwDFuQyOPFw9_khU/export?format=csv')
print(read)
#print(read.iloc[0])
read = read.drop_duplicates()
read = read.dropna()
read = read.reset_index()

print(read)
#rows = (int) (read.index.stop)
rows = (int) (len(read.index))
print(rows)

print("From which row, you want to start form filling?")

starting_row = (int) (input())
if(starting_row < 2 or starting_row > rows+1):
    while(starting_row < 2 or starting_row > rows+1):
        print("Invalid Row Number, write again")
        starting_row = (int) (input())
    
#print(name)

def is_Valid_Name(n):
    for char in n:
        if(not(char.isalpha() or char.isspace())):
            print("Inalid Name (Skipping the row)")
            return False
    return True

def is_Valid_Email(e):
    valid_email = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if(re.match(valid_email,e)):
        return True
    return False

for i in range ((starting_row-2),rows):   
    if(is_Valid_Name(read['Names'][i]) and is_Valid_Email(read['Emails'][i])):
        web = webdriver.Chrome()
        web.get('https://tally.so/r/wzrV0a')

        time.sleep(2)

        name = read['Names'][i]
        name_pathx = web.find_element(By.XPATH,'//*[@id="6ba08823-0306-4a31-8683-ed6708253c1d"]')
        name_pathx.send_keys(name)
        print(name)

        email = read['Emails'][i]
        email_pathx = web.find_element(By.XPATH,'//*[@id="116217f0-7823-440b-8e05-7e1f023ebd88"]')
        email_pathx.send_keys(email)
        print(email)

        done_pathx = web.find_element(By.XPATH,'//*[@id="__next"]/div/main/section/form/div[2]/div[1]/button/span')
        done_pathx.click()
        print("done")

        time.sleep(2)