import os
import re
import requests
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1200")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-notifications")
driver=webdriver.Chrome(executable_path="./chromedriver_win32/chromedriver", options=chrome_options)

#hacking-parameters
url = "https://codeforces.com/contest/"
contest = "1697"
page = "/standings/page/{}"
submission = "/submission/{}"
urls = []
count = 0
problemid = "1427644"

def findHack(s):
    try:
        print(s)
        print(urls)
        driver.get(s)
        wait = WebDriverWait(driver, 100)
        load = wait.until(EC.presence_of_element_located((By.XPATH, '//ol[contains(@class, "linenums")]')))
        lis = driver.find_element_by_class_name('linenums').find_elements_by_xpath("./*")
        # with open("hack.cpp", 'w', encoding="utf-8") as file:
        #     for li in lis:
        #         line = li.text
        #         file.write(line)
        #         file.write("\n")
        os.system('g++ hack.cpp -D ONLINE_JUDGE -o hack.exe')
        open("output.out.txt", "w").close()
        
        # os.system('hack.exe <input.in.txt> output.out.txt')

        # When you are expecting a TLE
        os.system('limit-runtime.bat')

        output = []
        validate = []
        with open('output.out.txt','r') as file:
            for line in file:
                if not line.isspace():
                    output.append(line.strip())
        with open('validate.out.txt','r') as file:
            for line in file:
                if not line.isspace():
                    validate.append(line.strip())
        if output == validate:
            pass
        else:
            urls.append(s)
            print("Hacked: ", s)
    except Exception as e:
        print(e)

t = 100
while t!=0:
    t-=1
    try:
        count+=1
        req = requests.get(url+contest+page.format(count))
        soup = BeautifulSoup(req.text, 'html.parser')
        submissions = []
        trs = soup.find("table", {"class": "standings"}).find_all("tr", participantid = True)
        for tr in trs:
            td =tr.find("td", {"problemid": problemid, "title": re.compile("^GNU.*")})
            if td != None and td.has_attr("acceptedsubmissionid"):
                submissions.append(url+contest+submission.format(td["acceptedsubmissionid"]))
        for s in submissions:
            findHack(s)
    except Exception as e:
        print(e)
    print(count)

print(urls)
driver.close()
driver.quit()