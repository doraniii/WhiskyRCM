import time
import weaviate

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

options = Options()
options.add_argument("--headless")
# 리눅스 서버같은 GUI환경이 지원안될 때 필요한 옵션
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

url = 'https://whiskyadvocate.com/ratings-reviews'
driver = webdriver.Chrome(options=options)

# 위스키 스타일을 선택. select box로 선택할 수 있는 모든 위스키 스타일을 list로 반환
def func_selectStyle(url) :
    urlList = []
    driver.get(url)

    getElements = driver.find_element(By.CLASS_NAME, 'mwInput.checkList.new.filter.select.multiline.noMobile.name-filtersdefaultcustom_rating_category.list')

    # 리스트 가져오기
    getList = getElements.find_element(By.CLASS_NAME, 'list')
    child_divs = getList.find_elements(By.TAG_NAME, 'div')

    # select box option 가져오기
    select_element = driver.find_element(By.NAME, 'filters[default][custom_rating_category][]')
    select = Select(select_element)
    option_list = select.options

    # 버튼
    searchBtn = driver.find_element(By.CLASS_NAME,'submit.button.mwFilter-submit.mwFormSubmit')
    resetBtn = driver.find_element(By.CLASS_NAME, 'reset.button.mwFilter-reset.mwFormSubmit')

    for list, opt in zip(child_divs[1:3], option_list[1:3]) :
   
        driver.execute_script("arguments[0].classList.add('selected');", list)
        driver.execute_script("arguments[0].setAttribute('selected', 'selected');", opt)

        searchBtn.click()
        time.sleep(5)
        currentUrl = driver.current_url
        print(currentUrl)
        urlList.append(currentUrl)
        time.sleep(10)
        driver.execute_script("arguments[1].classList.remove('selected');", list)
        driver.execute_script("arguments[1].removeAttribute('selected');", opt)

 
    return urlList

func_selectStyle(url)