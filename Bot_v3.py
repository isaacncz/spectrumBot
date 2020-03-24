import selenium 
import time
import io
import requests
import discord

from discord import Webhook, RequestsWebhookAdapter, File
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import schedule 
import time 

#import from other py file
import functions as funct

# dot env file
import os
from dotenv import load_dotenv
load_dotenv()

# funct.reset_table("spectrum")

Webhook1 = Webhook.partial(os.getenv("WEBHOOK1_DATA"),os.getenv("WEBHOOK1_ADAPTER"),adapter=RequestsWebhookAdapter())
Webhook2 = Webhook.partial(os.getenv("WEBHOOK2_DATA"),os.getenv("WEBHOOK2_ADAPTER"),adapter=RequestsWebhookAdapter())
client = commands.Bot(command_prefix = '.')

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options = Options()
options.headless = True
# driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
# driver = webdriver.Chrome(os.getenv("DRIVER_LOCATION"))

def login(driver):
   driver.get(os.getenv("WEBSITE"))
   n = True
   while n == True:
      if (os.getenv("LOGIN_SITE") in driver.current_url ):     
         username = driver.find_element_by_name('uname')
         password = driver.find_element_by_name('password')
         status = driver.find_element_by_name('domain')
         status.send_keys("Student")
         username.send_keys(os.getenv("USER"))
         password.send_keys(os.getenv("PASSWORD"))
         password.send_keys("\n")
      
      elif "You are not logged in." in driver.page_source:
         driver.get(os.getenv("WEBSITE"))

      elif "502 Bad Gateway" in driver.page_source:
         Webhook2.send ('502 Bad Gateway: ' +  time.ctime(time.time()))   
         driver.close()
         time.sleep(60)
         main()

      elif "This site can’t be reached" in driver.page_source:
         Webhook2.send ('This site can’t be reached: ' +  time.ctime(time.time()))   
         driver.close()
         time.sleep(60)
         main()   

      elif "course" not in driver.current_url in driver.page_source:
         n = False
   print("exit while loop")

def getFile(driver):
   count = 0
   for x in range(len(driver.find_elements_by_class_name("coursename"))):
   # for x in range(1): 
      driver.find_elements_by_class_name("coursename")[x].click()
      # print(driver.title)
      for element in driver.find_elements_by_xpath('//div/div/div[2]/div/a'):
         z = driver.title
         courseCode = z.split()
         # print(y[1])
         if 'resource' in element.get_attribute("href"):
            print(courseCode[1] + " " + element.get_attribute("text"))
            dataCheck = compare(courseCode[1],element.get_attribute("text"))
            # print("resource")
            if dataCheck == False:
               count+=1
               Webhook1.send(driver.title + ':' + element.get_attribute("text") + ' have been uploaded. ' + ' Link: ' + element.get_attribute("href"))
               # Webhook.send(element.get_attribute("text") + ' have been uploaded to ' + driver.title + ' : ' + element.get_attribute("href"))
         elif 'assign' in element.get_attribute("href"):
            print(courseCode[1] + " " + element.get_attribute("text"))
            dataCheck = compare(courseCode[1],element.get_attribute("text"))
            if dataCheck == False:
               count+=1
               # print("assignment")
               Webhook1.send( driver.title + ':' + 'Assignment submission is open (' +  element.get_attribute("text") + '). Link: ' +  element.get_attribute("href"))
         elif 'Announcements' in element.get_attribute("text") and 'forum' in element.get_attribute("href"):         
            temp = element
      if temp != None:      
         temp.click()      
         for announce in driver.find_elements_by_xpath('//td[1]/a'):
          print(announce.get_attribute("text"))
          temp = None
         driver.back()
      driver.back()
   Webhook2.send("Total files found: " + str(count))
   

def compare(course,element):
   results = funct.compareQuery(course,element)
   print(results)
   if results == True:
      # add discord notification here
      print("data exist")
      return True
   else:
      print("data not exist")
      funct.insert(course,element)
      return False

def main():
   try: 
      # seconds passed since epoch
      seconds = time.time()
      local_time = time.ctime(seconds)
      # driver = webdriver.Chrome(os.getenv("DRIVER_LOCATION"),options=options)
      driver = webdriver.Chrome(os.getenv("DRIVER_LOCATION"))
      Webhook2.send("Spectrum bot running at " +  local_time)
      login(driver)
      getFile(driver)
      driver.close()

   except:
      driver.close()   

def loop():
    try:
       main()
       schedule.every(6).hours.do(main)

       while True:
          schedule.run_pending() 
          time.sleep(10)
    except: 
        loop()


# loop()
seconds = time.time()
local_time = time.ctime(seconds)
# driver = webdriver.Chrome(os.getenv("DRIVER_LOCATION"),options=options)
driver = webdriver.Chrome(os.getenv("DRIVER_LOCATION"))
Webhook2.send("Spectrum bot running at " +  local_time)
login(driver)
getFile(driver)
driver.close()


# funct.insert("GIG1005","Letter to perform")
# funct.insert("GIG1005","123")
# compare("GIG1005","123")
# compare("GIG1005","perform activities")


         



  
   





