import time
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

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

# 필요한 Elements 가져오기
def func_findEle(eleClass) :
    getElements = driver.find_element(By.CLASS_NAME, eleClass)

    # 리스트 가져오기
    getList = getElements.find_element(By.CLASS_NAME, 'list')
    child_divs = getList.find_elements(By.TAG_NAME, 'div')

    # select box option 가져오기
    select_element = driver.find_element(By.NAME, 'filters[default][custom_rating_brand][]')
    select = Select(select_element)
    option_list = select.options

    return child_divs, option_list


# 위스키 브랜드 선택. 선택한 option별로 url이 달라지기 때문에 옵션 선택 별로 url 저장
def func_selectStyle(url, eleClass, subBtnEle) :
    urlList = []
    driver.get(url)

    child_divs, option_list = func_findEle(eleClass)

    for i in tqdm(range(1, len(child_divs))) :
        list = child_divs[i]
        opt = option_list[i]
        action = ActionChains(driver)
        action.move_to_element(driver.find_element(By.CLASS_NAME, eleClass)).perform()

        driver.execute_script("arguments[0].classList.add('selected');", list)
        driver.execute_script("arguments[0].setAttribute('selected', 'selected');", opt)

        action.move_to_element(driver.find_element(By.CLASS_NAME, subBtnEle)).perform()
        searchBtn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, subBtnEle)))
        searchBtn.click()

        time.sleep(5)
        currentUrl = driver.current_url
        index = currentUrl.find('custom_rating_brand')
        #현재 url에 필터값을 끼워넣어준다
        finalUrl = currentUrl[:index] + 'min_score=85&min_price=1&' + currentUrl[index:]
        urlList.append(finalUrl)
        
        time.sleep(5)
        
        action.move_to_element(driver.find_element(By.CLASS_NAME, eleClass)).perform()
        resetBtn = driver.find_element(By.CLASS_NAME, 'reset.button.mwFilter-reset.mwFormSubmit')
        driver.execute_script("arguments[0].click();", resetBtn)

        time.sleep(5)
        
        child_divs, option_list = func_findEle(eleClass)
        
    return urlList

optionUrlList = func_selectStyle(url, eleClass, subBtnEle)