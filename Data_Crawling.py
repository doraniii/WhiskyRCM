import time
from tqdm import tqdm

import weaviate
from weaviate.util import generate_uuid5

from makeUrl import func_selectStyle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

options = Options()
options.add_argument("--headless")
options.add_argument("start-maximized")
options.add_argument('--disable-dev-shm-usage')
# 리눅스 서버같은 GUI환경이 지원안될 때 필요한 옵션
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument('--remote-debugging-port=8903')

url = 'https://whiskyadvocate.com/ratings-reviews'
driver = webdriver.Chrome(options=options)

subBtnEle = 'submit.button.mwFilter-submit.mwFormSubmit'
eleClass = 'mwInput.checkList.new.filter.select.multiline.noMobile.name-filtersdefaultcustom_rating_brand.list'
urlList = func_selectStyle(url, eleClass, subBtnEle)

def func_crawData(urlList) :
    dataRows = []

    try :
        for i in tqdm(urlList[197:]):
            driver.get(i)   

            wait = WebDriverWait(driver, 5) 

            try :  

                WhiskyItemsCnt = len(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".mwDirectory-item"))))
                
                for j in range(WhiskyItemsCnt) :
                    WhiskyItems = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".mwDirectory-item")))
                    
                    item = WhiskyItems[j]
                    moreBtn = item.find_element(By.CLASS_NAME, 'postsItemLink')
                    driver.execute_script("arguments[0].click();", moreBtn)
                    time.sleep(5)
                    
                    name = driver.find_element(By.CLASS_NAME, 'postDetailsTitle').text
                    price = driver.find_element(By.CLASS_NAME, 'ratingsPrice').text

                    origin = driver.find_element(By.CLASS_NAME, 'postDetailsStats').text
                    index = origin.find('Category')

                    if len(origin[index:].split(': ')) > 1 :
                        category = origin[index:].split(': ')[1]
                    else :
                        category = ' '

                    review = driver.find_element(By.CLASS_NAME, 'postDetailsContent').text

                    # 각 오프젝트에 대해 uuid가 필요하다
                    uuid = generate_uuid5(j)

                    dataRows.append(
                        {"uuid" : uuid,
                        "Name" : name,
                        "Price" : price,
                        "Category" : category,
                        "Review" : review})
                    
                    driver.back()
                    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".mwDirectory-item")))

            except NoSuchElementException as e :
                continue
            except TimeoutException as e :
                continue
            
    except Exception as e:
        print(dataRows)
        print(e)
    
    return dataRows

result = func_crawData(urlList)
print(result)
