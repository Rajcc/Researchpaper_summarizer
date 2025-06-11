import selenium as sl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from transformers import pipeline
import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests 
# from bs4 import BeautifulSoup
# Create a summarizer pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

#os.environ['TRANSFORMERS_CACHE'] = "C:/Users/HP/.cache"
# Load model directly


A=input("enter==")
if A.strip()=="":
    print("enter your query")
else: 
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")##to make chrome run in background
    driver =webdriver.Chrome(options=options)## controls chrome driver
    driver.get("https://scholar.google.com")
    
    
    # Check if 'Scholar' is in title
    assert "scholar" in driver.title.lower()
    # Find the search box(q) and enter the query
    elem=driver.find_element(By.NAME,"q")
    elem.clear()
    for char in A:
        elem.send_keys(char)
        time.sleep(0.1)
    elem.send_keys(Keys.RETURN)
    time.sleep(8)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "gs_r"))
    )
    results=driver.find_elements(By.CLASS_NAME,"gs_r")
    for i,result in enumerate(results,start=1):
        try:
            title_element=result.find_element(By.CLASS_NAME,"gs_rt")
            title=title_element.text
            content=result.find_element(By.CLASS_NAME,"gs_ri")
            content_store=content.text #extracts content from gs_ri not the html
            text=content_store.strip() #strips off any white space
            if text:
             
                input_length = len(text.split())
                max_len = max(30, int(input_length * 0.5))
                try:
                    summary = summarizer(
                        content_store,
                        max_length=max_len,
                        min_length=20,
                        do_sample=False
                    )[0]['summary_text']
                except Exception as e:
                    summary = f"Summarization failed: {e}"
            else:
                summary = "No content to summarize."
            try:
                link=title_element.find_element(By.TAG_NAME,"a")
                link=link.get_attribute("href") 
            except:
                link="no link"
            print ("Title=",title)
            print("Link=",link)
            print("analysis=",summary)
        except Exception as e:
                print(f"error parsing result{i}:{e}") 
    driver.quit()      
            