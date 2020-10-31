# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
from pathlib import Path
cwd = str(Path(__file__).parent)
sys.path.insert(0, cwd)
from scraper_functions import *
import itertools 

GOOGLE_MAP_URL= "https://www.google.com/maps/search/"
BUSINESS_CATEGORY =  read_business_category().tolist()
WEBSITE_URLS_DF = read_website_df()


READING_LIMIT = ask_reading_limit(len(WEBSITE_URLS_DF.drop_duplicates()))
CSV_LIMIT = ask_csv_limit(len(WEBSITE_URLS_DF))
parameters = ask_paremeters()


def filter_url_address():
   count = 0 
   url_list = []
   
   for web_address in WEBSITE_URLS_DF:
       if (count == READING_LIMIT ):
           break
       else:
           url = GOOGLE_MAP_URL + web_address
           url = add__url_parameters(url,parameters)
           url_list.append(url)
           count = count + 1
   url_list = set(url_list)
   url_list = list(url_list) 
   return url_list  



def check_page_type(page_content):
    text = page_content.get_text().strip()
    if ("Suggest an edit" in text):
        return "Single"
    elif ("Showing results" in text):
        return "Multi" 
    elif ("Partial match" in text):
        return "Partial"  ##partial matches
    elif ("Google Maps can't find" in text):
        return "No result" 
    else:
        return "No result" 



def try_find_element_by_xpath(driver, xpath):
    try:
        element =  driver.find_element_by_xpath(xpath)
        return element
    except:
        element = "N/A"
        return element


def try_find_elements_by_xpath(driver,xpath):
    try:
        element =  driver.find_elements_by_xpath(xpath)
        return element
    except:
        element = "N/A"
        return element




def try_find_element_by_classname(driver,xpath):
    try:
        element =  driver.find_elements_by_class_name(xpath)
        return element
    except:
        element = "N/A"
        return element



def convert_xpath_to_atag_list(driver_path_list):
    if(driver_path_list =="N/A"):
        return "N/A"
    else:
        extracted_list = []
        for data in driver_path_list:
             if data is None or data == '':
                  extracted_list.append('N/A')
             else:
                 extracted_list.append(data.get_attribute('href'))
        return extracted_list


def convert_xpath_to_list(driver_path_list):
    if(driver_path_list =="N/A"):
        return "N/A"
    else:
        extracted_list = []
        if(len(driver_path_list) > 0 ):
            for data in driver_path_list:
                 if data is None or data == '':
                      extracted_list.append('N/A')
                 else:
                     extracted_list.append(data.text)
        else:
             extracted_list = ['N/A']
        return extracted_list




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
    
        

## multiple result found 
## extract information from all rectangles left
def scrap_mutli_result_information(web_address,driver,page_content):
     
     time.sleep(5)
     print("Multiple Results Found............... ")
     print("Extracting details............... ")
     Mutli_Search_Result_dataframe = pd.DataFrame(columns = ['SearchedWebsite','SearchIndex','Name', 'Category','Description','Phone','Extracted Website','Rating', 'Reviews']) 
    
     try:  
         
         title = try_find_element_by_classname(driver,'section-result-title')
         
         ratings = try_find_element_by_classname(driver,'section-result-rating')
         reviews = try_find_element_by_classname(driver,'section-result-num-ratings')    
         category = try_find_element_by_classname(driver,'section-result-details')
         location = try_find_element_by_classname(driver,'section-result-location')
         description =  try_find_element_by_classname(driver,'section-result-descriptions')
         showing_result_label = try_find_element_by_classname(driver,'n7lv7yjyC35__left') 
        
         phone_number  =  try_find_elements_by_xpath (driver,"//div[@class='section-result-hours-phone-container']/span[@class='section-result-info section-result-phone-number']")
         website_links = try_find_elements_by_xpath (driver,"//div[@class='section-result-content']//a[@class='section-result-action section-result-action-wide']")
         
         #opening_hour = driver.find_elements_by_class_name('section-result-info section-result-opening-hours')
         #closing_hour = driver.find_elements_by_class_name('section-result-info section-result-closed') 
         
         title = convert_xpath_to_list(title)
         ratings = convert_xpath_to_list(ratings)
         reviews = convert_xpath_to_list(reviews)
         category = convert_xpath_to_list(category)
         description = convert_xpath_to_list(description)
         phone_number = convert_xpath_to_list(phone_number)
         showing_results = convert_xpath_to_list(showing_result_label)
         website_links = convert_xpath_to_atag_list(website_links)
       
         showing_results = showing_results[0].split(' ')
         
         showing_results_length = int(showing_results[4])
         
         index_start = int(showing_results[2])
         index_end = int(showing_results[4])
       
             
         showing_results_length = [str(i) for i in range(index_start,index_end+1)]
         web_address_search = repeat_address(web_address,index_start,index_end)
        
         
         
         Mutli_Search_Result_dataframe['SearchedWebsite'] = pd.Series(web_address_search)
         Mutli_Search_Result_dataframe['SearchIndex'] = pd.Series(showing_results_length) 
         Mutli_Search_Result_dataframe['Name'] = pd.Series(title)  
         Mutli_Search_Result_dataframe['Category'] = pd.Series(category)  
       
         Mutli_Search_Result_dataframe['Description'] = pd.Series(description)   
         Mutli_Search_Result_dataframe['Phone'] = pd.Series(phone_number)    
         Mutli_Search_Result_dataframe['Extracted Website'] = pd.Series(website_links)     
         Mutli_Search_Result_dataframe['Rating']  = pd.Series(ratings)      
         Mutli_Search_Result_dataframe['Reviews'] = pd.Series(reviews)     
         print(Mutli_Search_Result_dataframe)
         print("=============Extracted Information=================")
         print(Mutli_Search_Result_dataframe)
         print("===================================================")
         return Mutli_Search_Result_dataframe
     
     except:
         print("no  more results")
         return Mutli_Search_Result_dataframe 



##
## checks the next page 
## call th function to extract 
## details from each multiple page
def scrap_from_mutli_result(web_address,driver,page_content):
    multi_result_dataframes = list() 
    next_page = True
    while(check_page_type(page_content)== 'Multi'):
        while(next_page): 
            if(goto_into_next_page(page_content)):
                if (check_page_type(page_content)== 'Multi'):
                    page_dataframe = scrap_mutli_result_information(web_address,driver,page_content)         
                    multi_result_dataframes.append(page_dataframe)
                    try:
                        driver.find_element_by_id("n7lv7yjyC35__section-pagination-button-next").click()
                        time.sleep(2)
                        page_content = driver.page_source
                        page_content = BeautifulSoup(page_content,'html.parser')
                        
                    except:
                        print("end of the results")
                        next_page = False
                        break
                else:
                     if (check_page_type(page_content)== 'Multi'):
                             page_dataframe = scrap_mutli_result_information(web_address,driver,page_content)         
                             multi_result_dataframes.append(page_dataframe)
                             print("Displaying mutli single page")
                             next_page = False
                             break
            else:
                print("New page detected")
                break 
        break   
    
        
    if (len(multi_result_dataframes) <= 1):
        df = multi_result_dataframes[0]
        print(df)
        return df     
            
    else:
        df = pd.concat(multi_result_dataframes)[multi_result_dataframes[0].columns]
        print("=============Extracted Information=================")
        print(df)
        print("===================================================")
        return df 




def scrap_from_single_result(web_address,driver,page_content):
     print('Reading single result')

     single_dataframe = pd.DataFrame(columns = ['SearchedWebsite','SearchIndex','Name', 'Category','Description','Phone','Extracted Website','Rating', 'Reviews']) 
     title = try_find_element_by_xpath(driver,"//h1[@class='section-hero-header-title-title GLOBAL__gm2-headline-5']")
     description = try_find_element_by_xpath(driver,"//div[@class='section-editorial-quote']")
     rating = try_find_element_by_xpath(driver,"//span[@class='section-star-display']")
     address = try_find_element_by_xpath(driver,"//*[@data-item-id='address']")
     website = try_find_element_by_xpath(driver,"//*[@data-item-id='authority']")
     phone   = try_find_element_by_xpath(driver,"//*[contains(@data-item-id,'phone:')]") 
     review_n_cat = try_find_elements_by_xpath(driver,"//span[@class='section-rating-term']")
     review_n_cat = convert_xpath_to_list(review_n_cat)
     title = title.text
     address = address.get_attribute('aria-label') 
     website = website.get_attribute('aria-label')
     phone = phone.get_attribute('aria-label')  
     description = description
     rating = rating.text     
     review =  str(review_n_cat[0])
     category = str(review_n_cat[1])
     print(title,description,address,address,phone,review,category)
     single_dataframe = single_dataframe.append({'SearchedWebsite' : web_address , 'SearchIndex' : '1' , 'Name': title,  'Category': category ,'Description': description,'Phone':phone,'Extracted Website': website, 'Rating': rating, 'Reviews': review }, ignore_index = True)
     print(single_dataframe)
   
     
   
     return single_dataframe
        
        
        
        
        
def scrap_from_partial_result(web_address,driver,page_content):
    print("Partial results")



def scrap_data_from_url():
    Final_dataframe = pd.DataFrame(columns = ['Searched Website','Found Results','Name', 'Rating', 'Reviews','Category','Description','Phone']) #prepare column for the csv  
    df_list = list()
    website_list  = filter_url_address()
   
    count = 1
    
    for web_address in website_list:
        driver = get_chrome_driver()
        print(str(count) +"/" + str(len(website_list)) ,"reading........."+ str(web_address))
       
        driver.get(web_address)
        wait = WebDriverWait(driver, 10) 
        page_content = driver.page_source
        page_content = BeautifulSoup(page_content,'html.parser')
        web_address = web_address.rsplit('/', 1)[-1]
        if (check_page_type(page_content) == "Single"):
            try:
                single_df = scrap_from_single_result(web_address,driver,page_content)  #Found single result
                df_list.append(single_df)
            except:
                 print("Extration ignore........")
           
            
        elif (check_page_type(page_content) == "Multi"):
            try:
                multi_df = scrap_from_mutli_result(web_address,driver,page_content)  ## Found multiple results 
                df_list.append(multi_df)
            except:
                print("Extration ignore........")
            
         
        elif (check_page_type(page_content) == "Partial"):
            
            scrap_from_partial_result(web_address,driver,page_content) # Found partial or single result
            
        else:
             print("Google Maps can't find",web_address) ### could not found the result
        
        
        if (CSV_LIMIT > 0):
             if count % CSV_LIMIT == 0:
                  df = pd.concat(df_list)[df_list[0].columns]    
                  save_into_csv(df)
                  
        count = count + 1
        
        time.sleep(5)    
        driver.quit() 
    
    df = pd.concat(df_list)[df_list[0].columns]    
    save_into_csv(df)
    print("Script Finished")
            

print(scrap_data_from_url())
