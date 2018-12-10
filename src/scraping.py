import time
import urllib
import os
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Scraper():
    def __init__(self):
        self.loadDriver()
    
    def loadDriver(self):
        self.driver = webdriver.Chrome(executable_path='/Users/kim/Downloads/chromeDriver/chromedriver')
        self.driver.implicitly_wait(3)

    def scrape(self, scrollCount, tag, path):
        
        if not os.path.isdir(path):
            raise Exception(path + ' 라는 경로를 찾을 수 없습니다.')
        if not tag:
            raise Exception('적절한 태그 값을 입력해주세요.')

        url = 'https://www.instagram.com/explore/tags/' + tag
        
        try:
            self.driver.get(url)
            time.sleep(2)
            body = self.driver.find_element_by_tag_name('body')
            for i in range(scrollCount):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
            img = self.driver.find_elements_by_css_selector('div.KL4Bh > img')
        except Exception as e:
            self.loadDriver()
            raise Exception('브라우저에 문제가 생겨 브라우저를 새로 로딩합니다. 다시 스크래핑을 시도하세요.')
        
        if len(img) == 0:
            raise Exception('검색 결과가 없습니다.')

        for src in img:
            alt = ''
            print(src.get_attribute('alt'))
#            try:
            alt = src.get_attribute('alt')
            src = src.get_attribute('src')
#            except Exception as e:
#                self.loadDriver()
#                raise Exception('저장 도중 브라우저에 문제가 생겨 브라우저를 새로 로딩합니다. 다시 스크래핑을 시도하세요.')

            fileName = src.split('/')[-1]
            if '?' in fileName:
                fileName = fileName[:fileName.index('?')]
            if ':' in alt:
                alt = alt[alt.index(':')+1:]
            
            if os.path.isfile(path + '/' + alt + fileName):
                print('the file already exist')
                continue
            urllib.request.urlretrieve(src, path + '/' + alt + '#' + fileName )
            print(path + '/' + alt + '#' + fileName + 'is saved!')



