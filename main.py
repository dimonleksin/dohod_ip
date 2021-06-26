import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import io
def scan(year):
    url = 'https://ofd.nalog.ru/search.html?mode=extended'
    driver = webdriver.Chrome(executable_path='G:\\chromedriver\\chromedriver.exe')
    driver.get(url=url)
    time.sleep(2)
    region = driver.find_element_by_id('uni_select_13')
    region.clear()
    region.send_keys('64 - Саратовская область')
    region.send_keys(Keys.ENTER)
    time.sleep(1)
    sity = driver.find_element_by_id('uni_select_23')
    sity.send_keys('САРАТОВ Г')
    sity.send_keys(Keys.ENTER)
    time.sleep(2)
    date_own = driver.find_element_by_id('uni_select_8')
    date_own.clear()
    date_own.send_keys(f'10.{year}.2021')
    time.sleep(1)
    date_own.send_keys(Keys.ENTER)
    driver.find_element_by_id('unichk_0').click()
    go = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/form/div[1]/div[4]/div[2]/button')
    go.click()
    time.sleep(15)
#driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/form/div[2]/div[2]/div[1]/div[1]/ul[2]/li[6]/a').click()
#time.sleep(15)
    pagen = int(driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/form/div[2]/div[2]/div[3]/div/ul[1]/li[6]/a').text)
    for i in range(pagen):
        print(f'{datetime.datetime.now().strftime("%H:%M:%S")} - открыта страница {i + 1} из {pagen}')
        html = driver.page_source
        with open(f'{i}_pagen.html', 'w', encoding='utf-8') as file:
            writer = file.write(html)
        try:
            driver.find_element_by_link_text('Следующая →').click()
        except Exception as ex:
            print(ex)
        time.sleep(20)
    driver.close()

    name = []
    inn = []
    result = []
    for i in range(pagen):
        with io.open(f'{i}_pagen.html', encoding='utf-8') as file:
            r = file.read()
            soup = BeautifulSoup(r, 'lxml')
            name = [i.text for i in soup.find_all('a', class_='lnk lnk-document-stamp')]
            inn = [inn_i.text[4:] for inn_i in soup.find_all('div', class_='rsmp-result result-inn')]
            print(f'Открыт файл {i}_pagen.html')
            for item in range(int(len(name))):
                result.append(
                    {
                        'name': name[item],
                        'inn': inn[item]
                    }
                )
    with open('result.json', 'a', encoding='utf-8') as file:
        json.dump(result, file, indent = 4, ensure_ascii = False)
    print('Готово')

while True:
    i = input('Введите месяц включенгия в реестр :')
    if isdigit(i):
        scan(i)
