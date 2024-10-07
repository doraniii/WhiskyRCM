import time
import weaviate

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
# 디버깅 모드를 위한 옵션
options.add_argument('--remote-debugging-port=8903')

url = 'https://whiskyadvocate.com/ratings-reviews'
driver = webdriver.Chrome(options=options)

eleClass = 'mwInput.checkList.new.filter.select.multiline.noMobile.name-filtersdefaultcustom_rating_category.list'
subBtnEle = 'submit.button.mwFilter-submit.mwFormSubmit'

# 필요한 Elements 가져오기
def func_findEle(eleClass) :
    getElements = driver.find_element(By.CLASS_NAME, eleClass)

    # 리스트 가져오기
    getList = getElements.find_element(By.CLASS_NAME, 'list')
    child_divs = getList.find_elements(By.TAG_NAME, 'div')

    # select box option 가져오기
    select_element = driver.find_element(By.NAME, 'filters[default][custom_rating_category][]')
    select = Select(select_element)
    option_list = select.options

    return child_divs, option_list

# 위스키 스타일을 선택. 선택한 option별로 url이 달라지기 때문에 옵션 선택 별로 url 저장
def func_selectStyle(url, eleClass, subBtnEle) :
    urlList = []
    driver.get(url)

    child_divs, option_list = func_findEle(eleClass)

    for i in range(1, len(child_divs)) :
        list = child_divs[i+1]
        opt = option_list[i+1]
        action = ActionChains(driver)
        action.move_to_element(driver.find_element(By.CLASS_NAME, eleClass)).perform()

        driver.execute_script("arguments[0].classList.add('selected');", list)
        driver.execute_script("arguments[0].setAttribute('selected', 'selected');", opt)

        action.move_to_element(driver.find_element(By.CLASS_NAME, subBtnEle)).perform()
        searchBtn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, subBtnEle)))

        searchBtn.click()

        time.sleep(5)
        currentUrl = driver.current_url
        urlList.append(currentUrl)

        time.sleep(5)
        action.move_to_element(driver.find_element(By.CLASS_NAME, eleClass)).perform()

        resetBtn = driver.find_element(By.CLASS_NAME, 'reset.button.mwFilter-reset.mwFormSubmit')
        resetBtn.click()
        time.sleep(5)
        
        child_divs, option_list = func_findEle(eleClass)

    return urlList

optionUrlList = func_selectStyle(url, eleClass, subBtnEle)

def func_getElements() :
    whkResult = driver.find_element(By.ID, "directoryResults")
    wskObjs = whkResult.find_elements(By.CLASS_NAME, "mwDirectory-item")

    return wskObjs

# selectStyle함수에서 반환받은 리스트로 하나씩 select해서 나온 결과에 대한 위스키들의 정보를 크롤링
def func_crawlData(urls):
    whiskyJson = {}
    whiskyList = []

    #테스트로 selectList 3개만. 나중에 전체 리스트로 변경
    for url in urls:
        url = url
        driver.get(url)

        wskObjs = func_getElements()

        for i in range(len(wskObjs)) :
            wskObj = wskObjs[i].find_element(By.CLASS_NAME, "postsItemLink")
            time.sleep(5)
            driver.execute_script("arguments[0].click();", wskObj)      
       
            # 위스키 이름
            wskName = driver.find_element(By.CLASS_NAME, "postDetailsTitle").text
            # 위스키 카테고리
            CategoryOrigin = driver.find_element(By.CLASS_NAME, "postDetailsStats").text
            Category = CategoryOrigin.split('Category: ')[-1]
            # 위스키 설명
            wskSub = driver.find_element(By.CLASS_NAME, "postDetailsContent").text

            whiskyJson['name'] = wskName
            whiskyJson["category"] = Category
            whiskyJson["review"] = wskSub

            whiskyList.append(whiskyJson)

            driver.back()
            wskObjs = func_getElements()
            time.sleep(5)
         
    return whiskyList

result = func_crawlData(optionUrlList)  
print(result)