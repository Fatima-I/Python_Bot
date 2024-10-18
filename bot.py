import pandas as pd
from selenium import webdriver
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import time
import re
import threading
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

scope = [
    "https://www.googleapis.com/auth/spreadsheets"
]

credentials = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(credentials)

sheet_id = "1Ii3g9GzR8_X3ZWXuR7vGLbjWnUECwDFuQyOPFw9_khU"
g_sheet = client.open_by_key(sheet_id)

data = g_sheet.sheet1.get_all_values()

dataframe = pd.DataFrame(data[1:], columns=data[0])

#print(dataframe)

rows = (int) (len(dataframe.index))

#print("Columns:", dataframe.columns.tolist())

#print(rows)

print("From which row, you want to start form filling?")

starting_row = (int) (input())
if(starting_row < 2 or starting_row > rows+1):
    while(starting_row < 2 or starting_row > rows+1):
        print("Invalid Row Number, write again")
        starting_row = (int) (input())

count = starting_row-2

print("Enter Number Of Threads")

no_Of_Threads = (int) (input())
if(no_Of_Threads < 0 or no_Of_Threads > rows-1):
    while(no_Of_Threads < 0 or no_Of_Threads > rows):
        print("Invalid Input, write again")
        no_Of_Threads = (int) (input())

def is_Valid_Name(n):
    for char in n:
        if(not(char.isalpha() or char.isspace())):
            print("Inalid Name (Skipping the row)")
            return False
    return True

def is_Valid_Email(e):
    valid_email = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if(re.match(valid_email,e,re.IGNORECASE)):
        return True
    print("Invalid Email (Skipping the row)")
    return False

def is_Null_Value(v):
    #if(pd.isna(dataframe[v]) or pd.isnull(dataframe[v])):
    #    return False
    #return True
    return pd.notna(v)

def form_filling(i):
    if(dataframe['Form_Filling'][i] == "Done"):
        print("A form is already filled with same data")
    elif(is_Valid_Name(dataframe['Names'][i]) and is_Valid_Email(dataframe['Emails'][i])
                and is_Null_Value(dataframe['Names'][i]) and is_Null_Value(dataframe['Emails'][i])):
        web = webdriver.Chrome()
        web.get('https://tally.so/r/wzrV0a')

        time.sleep(2)

        name = dataframe['Names'][i]
        name_pathx = web.find_element(By.XPATH,'//*[@id="6ba08823-0306-4a31-8683-ed6708253c1d"]')
        name_pathx.send_keys(name)
        print(name)

        email = dataframe['Emails'][i]
        email_pathx = web.find_element(By.XPATH,'//*[@id="116217f0-7823-440b-8e05-7e1f023ebd88"]')
        email_pathx.send_keys(email)
        print(email)

        done_pathx = web.find_element(By.XPATH,'//*[@id="__next"]/div/main/section/form/div[2]/div[1]/button/span')
        done_pathx.click()
        print("done")

        dataframe['Form_Filling'][i] = "Done"
        time.sleep(2)
    else:
        dataframe['Form_Filling'][i] = "Incorrect Data"

threads = []
while(count != rows):
    for i in range(1,(no_Of_Threads+1)):
        if (count >= rows):
            break
        else:
            new_threads = threading.Thread(target=form_filling,args=[count])
            threads.append(new_threads)
            new_threads.start()
            count=count+1
    for t in threads:
        t.join()

#print(dataframe)

form_dataframe = pd.DataFrame(dataframe['Form_Filling'])
row=1
col=3
worksheet = g_sheet.get_worksheet(0)
set_with_dataframe(worksheet,form_dataframe,row,col)
print("Google Sheet has been")