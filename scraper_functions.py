# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os 
import sys
import re
import time
import pandas as pd
from tkinter import *
from bs4 import BeautifulSoup
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException   
import numpy as np
from sys import platform

BUSINESS_CATEGORY = "files/business-category/Categories.csv"


def get_chrome_driver():
    if platform == "darwin":
        os.chmod('/usr/local/bin/chromedriver', 755) 
        options = webdriver.ChromeOptions()
        options = webdriver.ChromeOptions()
        #options.add_argument('headless')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        chrome_driver_binary = "/usr/local/bin/chromedriver"
        driver = webdriver.Chrome(chrome_driver_binary, options=options)
        return driver
    
    if platform == "win32":
        options = webdriver.ChromeOptions()
        #options.add_argument('headless')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome('chromedriver/windows/chromedriver.exe', options=options)
        return driver
  
    
  
    
def generated_time():
    geneerated_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    return geneerated_time


def ask_file_directory():
    root = Tk()
    root.withdraw()
    dataSet_file_directory = filedialog.askopenfilename()
    return dataSet_file_directory
  
    
def check_file_format(provided_file):
    file_name = os.path.basename(provided_file)
    if(file_name.endswith(".csv")):
        return 1
    elif(file_name.endswith(".xlsx")):
        return 2
    else:
        return 0
  
    

def read_dataframe(data_file):
    if(check_file_format(data_file) == 1):
        df = pd.read_csv(data_file)
        df =  df[df.columns[0]].dropna()
        return df 
    elif(check_file_format(data_file) == 2):
        df = pd.read_excel(open(data_file,'rb'), sheet_name='Sheet 1')
    return df


def read_business_category():
    df = read_dataframe(BUSINESS_CATEGORY)
    return df
   
            
def save_into_csv(df):
    df = df.to_csv("GoogleMaps-Scraped-Data-"+str(generated_time())+".csv", encoding='utf-8-sig' ,index=False)
    return True

def create_dataframe(column_list):
    df = pd.DataFrame(columns = column_list ) 
    return df

def repeat_address(address,index_start_range,index_end_range):
    data = []
    for i in range(index_start_range,index_end_range+1):
        data.append(address)
    return data
    
def read_website_df():
    website_url_dataset_path = ask_file_directory()
    website_url_df = read_dataframe(website_url_dataset_path)
    website_Len = len(read_dataframe(website_url_dataset_path).drop_duplicates())
   
    print("Selected Data File Consist Of Website Url --->", os.path.basename(website_url_dataset_path))
    print("Total Url Found in file", website_Len )
    return website_url_df


def ask_paremeters():
    print("\nEnter any keywords to get more relevants from Google Maps\nFor example if you add keyword canda the script will search the web address along with the provided keyword")
    print("\nAdd your key words followed by ',' E.g: canda,ottawa")
    keywords = input("Enter the keyword, if no keywords then press enter --->: ")
    if(keywords ==""):
        return []
    else: 
        keywords = keywords.split(',')
        print("Selected keyword",keywords)
        return keywords


def add__url_parameters(url,parameters):
    for i in range (len (parameters)):
        url = (url+" {} ".format( parameters[i]))
    return url 




def ask_reading_limit(total_records):
    record_limit = input('If you would like to process entire dataset, Enter "Y" ' 
                            'Else Enter the number of rows you would like to process:---> ')
    
    if (record_limit == 'Y'):
         print("Process full dataset")
         return int(total_records)
    
    elif(record_limit.isdigit()):
        if (total_records >= int(record_limit)):
             print("Process only " +str(record_limit)+" dataset")
             return int(record_limit)
       
    else:
        print("Invalid Choice, Setting limit to full dataset")
        return total_records
    
    
    
    
def ask_csv_limit(total_records):
    csv_limit = input('\nGenerate CSV Batch, Enter "Y" Else Enter the number of rows'
                            'at which you would like csv to be generated--->')
    csv_limit.strip()
    if(csv_limit == "Y"):
         print("Process full dataset")
         return int(total_records)
    
    elif(csv_limit.isdigit()):
        if(total_records >= int(csv_limit)):
            print("Generate CSV  after every " +str(csv_limit)+" rows")
            return int(csv_limit)
      
    else:
        print("NO BATCH CSV GENERATION")
        csv_limit = 0 
        return csv_limit
    
    
    

def shorten(s, subs):
    i = s.index(subs)
    return s[:i+len(subs)]


def found_results(s, subs):
    i = s.index(subs)
    return s[i+len(subs):-2]


def check_category(category, text):
    for cat in category:
        if(cat in text):
            return [cat,True]
    return ["Not Matched",False]
     
    
    
def goto_into_next_page(page_content):
   
     if (page_content.find('button',{'class':'n7lv7yjyC35__button noprint'})):
         print("More results Found on Next Page...")
         time.sleep(2)
         return True
     elif (page_content.find('button',{'class':'n7lv7yjyC35__button noprint n7lv7yjyC35__button-disabled'})):
         print("Displaying all the results")
         return False
     else:
        print("not working")
        return False
   


