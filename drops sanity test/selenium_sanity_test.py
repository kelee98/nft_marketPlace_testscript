import unittest
import time
import json
import requests
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire.utils import decode
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import HtmlTestRunner


class DropsSanityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
    	# 해당 클래스가 실행될 때마다 동작해야 하는 함수
        # driver 셋팅, 브라우저 오픈 등
        cls.options = webdriver.ChromeOptions()
        #클립 a2a 창을 열기 위해 유저에이전트가 모바일이여야 함 
        cls.options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 9; SM-A530N Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.116 Mobile Safari/537.36;KAKAOTALK 1909000")
        cls.driver = webdriver.Chrome("./chromedriver", options = cls.options)
        cls.driver.get("https://qa.klipdrops.com")
        #drops 공지 사항 모달이 뜰경우, 모달 창 닫기 실행
        try :
            cls.driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div/div/div/div[2]/a").click()
        except:
            print("긴급공지 없음")
        cls.driver.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
    	# 해당 클래스가 종료될 때마다 동작해야 하는 함수
        # driver 종료 등
        time.sleep(50)
        cls.driver.close()
        cls.driver.quit()
        
    #def setUp(self):
    	# 각 테스트케이스가 실행되기 전에 동작해야 하는 함수
        # 로그인 등
         # modal 창 있을 경우 , 창 닫기
    #def tearDown(self):
    	# 각 테스트케이스가 종료될 때 동작해야 하는 함수
        # 로그아웃 등

    def test_case1(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.LINK_TEXT,"Home").click()
        time.sleep(3)
        self.driver.save_screenshot('main.png')
        return print("비회원일 때 홈 접근 가능")
    def test_case2(self) :
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.LINK_TEXT,"1D1D").click()
        time.sleep(10)
        self.driver.save_screenshot('1d1d_main.png')
        return print("비회원일 때 1d1d 진입 가능 ")
    def test_case3(self) :
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.LINK_TEXT,"dFactory").click()
        time.sleep(6)
        self.driver.save_screenshot('dfactory_main.png')
        return print("비회원 일때 dfactory 진입 가능")
    def test_case4(self) :
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.LINK_TEXT,"Market").click()
        time.sleep(6)
        self.driver.save_screenshot('market_main.png')
        return print("비회원 일때 market 진입 가능")
    def test_case5(self):
        #Mypage tab 클릭
        time.sleep(5)
        mypage_login = self.driver.find_element(By.LINK_TEXT, "My Page")
        mypage_login.click()
        self.driver.implicitly_wait(10)
        return print("비회원 일때 my 페이지 진입 가능")
    
    #6. 로그인 테스트
    def test_case6(self):
        driver =self.driver
        #driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div/div/div/div[2]/a").click()
        driver.implicitly_wait(100)
        #Mypage tab 클릭
        #mypage_login = self.driver.find_element(By.XPATH, '//*[@id="App"]/div/div[8]/ul/li[5]/a')
        #mypage_login.click()
        login = self.driver.find_element(By.XPATH,'//*[@id="App"]/div/div[3]/a')
        login.click()
        
        # drops 로그인 시 , a2a requestkey 가 생성 됨 
        # 해당 request key 는 /v2/account/prepare api 응답 값에 있음 
        # 네트워크를 캡처 하면서 /v2/account/prepare api가 나타 날 때 까지 기달림 (seleniumwire 를 사용해야 해당 기능 사용 가능함)
        request = driver.wait_for_request('.*/v2/account/prepare.*')
        status_code = request.response.status_code
        print(f'{request.url}, 응답코드 {request.response.status_code}, 컨텐츠 유형: {request.response.headers}')
        
        response_str = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity')).decode('utf-8')
        assert status_code == 200, f'{request.url} 요청에 대한 응답 실패: {status_code}: {response_str}'
        response_json = json.loads(response_str)
        requestsKey = response_json['request_key']
        
        #request key를 받은 login api 를 클립에서 열어야 하기 때문에 새탭을 염
        driver.execute_script("window.open('');")
        #새탭을 열고 klip a2a 주소 (endpotin+requestkey 결합된 주소 ) 로 이동 
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://qa2.klipwallet.com/")
        #driver.implicitly_wait(10)
        #del driver.requests  # 초기화

        # 승인 요청 klip api 전송
        header = {
            'Cookie':'_ga_8EHLQ3CPHF=GS1.1.1671597840.15.1.1671597852.0.0.0; __cuid=0897093691c34f94b3c3cd3f714ef9b0; amp_fef1e8=765f84fc-0c24-4696-a2d9-4720e6d941a0R...1gkshdaio.1gkshdatu.4.3.7; _ga=GA1.2.1304195934.1665993266; _ga_NGJB7TTPD6=GS1.1.1674629493.13.1.1674629546.7.0.0; _gid=GA1.2.347660892.1676858863; _gat_UA-121647508-19=1; _gat_UA-121647508-21=1; klip-session=MTY3Njg1ODg4MnxOd3dBTkZaV1QwUlZWREpCVEV4Sk4waEtVa2t6TkRWUlIwUkpRMUpPVFVGVlYxcFJXVU5aTmt4T1dVdEtOVlJXUWtSQ1NVdzNRMEU9fE3Un1ISUJwbpugx9LW9IiS0Dp9uQVYd54TxmujjZ-gC',
            'user-agent':'Mozilla/5.0 (Linux; Android 9; SM-A530N Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.116 Mobile Safari/537.36;KAKAOTALK 1909000',
            'Content-Type': 'application/json'
            }
        json_data = {"request_key":requestsKey}
        response = requests.post('https://qa2-api.klipwallet.com/v1/a2a/auth',headers=header,json=json_data)
        print(response)
        
        driver.switch_to.window(driver.window_handles[0])




        
        return print("drops 로그인 완료")

    #마켓플레이스에 작품 등록 
    def test_case7(self):   
        self.driver.find_element(By.LINK_TEXT, "My Page").click()
        self.driver.find_element(By.XPATH,'//*[@id="App"]/div/div[2]/section[3]/div[2]/div/div[1]/div[1]').click()
        self.driver.find_element(By.CLASS_NAME,"drop-container").click()
        self.driver.find_element(By.XPATH,'//*[@id="App"]/div/div[3]/a[2]').click()
        self.driver.find_element(By.XPATH,'//*[@id="App"]/div/div/div/div/div[2]/div[1]/div[3]/div[2]/div[1]/input').send_keys("1")
        self.driver.find_element(By.XPATH,'//*[@id="App"]/div/div/div/div/div[2]/div[1]/div[3]/div[2]/div[1]/a').click()
        
        #양수도계약서 클릭
        self.driver.find_element(By.XPATH,"/html/body/div/div/div/div/div/div/div[2]/div[1]/div[5]/div/div[2]/div/div/div/a").click()
        self.driver.execute_script("window.scrollTo(0, 1000)")
        self.driver.find_element(By.XPATH,"/html/body/div/div/div/div/div/div/div[2]/div[3]/a[2]").click()
        self.driver.find_element(By.XPATH,"/html/body/div[3]/div/div[2]/div/div/div[3]/div/a").click()
        
        time.sleep(3)
        self.driver.execute_script("window.scrollTo(0, 2500)")
        self.driver.find_element(By.XPATH,'//*[@id="App"]/div/div/div/div/div[2]/div[3]/div[1]/div/label/span[1]/input').click()
        self.driver.find_element(By.XPATH,'//*[@id="App"]/div/div/div/div/div[2]/div[3]/div[2]/div/label/span[1]/input').click()
        self.driver.find_element(By.XPATH,'//*[@id="App"]/div/div/div/div/div[2]/div[3]/div[3]/div/label/span[1]/input').click()
        self.driver.find_element(By.XPATH,'//*[@id="App"]/div/div/div/div/div[2]/div[4]/a[2]').click()


        self.driver.execute_script("window.scrollTo(0, 1000)")
        self.driver.find_element(By.XPATH,'//*[@id="App"]/div/div/div/div/div[2]/section[2]/div[2]/a[2]').click()

        request= self.driver.wait_for_request('.*/sell.*')
        while request.method != "POST"  :
            del self.driver.requests
            request= self.driver.wait_for_request('.*/sell.*')
        if request.method == "POST" :
            status_code = request.response.status_code
            print(f'{request.url}, 응답코드 {request.response.status_code}, 컨텐츠 유형: {request.response.headers}')
            response_str = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity')).decode('utf-8')
            assert status_code == 200, f'{request.url} 요청에 대한 응답 실패: {status_code}: {response_str}'
            response_json = json.loads(response_str)
            print(response_json)
            requestsKey = response_json['request_key']
            print(requestsKey)

        #klip 승인 api  요청 
        header = {
            'Cookie':'_ga_8EHLQ3CPHF=GS1.1.1671597840.15.1.1671597852.0.0.0; __cuid=0897093691c34f94b3c3cd3f714ef9b0; amp_fef1e8=765f84fc-0c24-4696-a2d9-4720e6d941a0R...1gkshdaio.1gkshdatu.4.3.7; _ga=GA1.2.1304195934.1665993266; _ga_NGJB7TTPD6=GS1.1.1674629493.13.1.1674629546.7.0.0; _gid=GA1.2.347660892.1676858863; _gat_UA-121647508-19=1; _gat_UA-121647508-21=1; klip-session=MTY3Njg2NjI1M3xOd3dBTkZaV1QwUlZWREpCVEV4Sk4waEtVa2t6TkRWUlIwUkpRMUpPVFVGVlYxcFJXVU5aTmt4T1dVdEtOVlJXUWtSQ1NVdzNRMEU9fIkXYmawhOgx5BLA12RdWOqaiV3WM3b9oHOycGBdtC_L',
            'user-agent':'Mozilla/5.0 (Linux; Android 9; SM-A530N Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.116 Mobile Safari/537.36;KAKAOTALK 1909000',
            'Content-Type': 'application/json'
            }
        json_data = {"request_key":requestsKey,"pin":"966c4c0422b7843240d3dbbfb7611cc9dfc85e94d789161b2c35d8d5fa495426","card_name":""}
        response = requests.post('https://qa2-api.klipwallet.com/v1/a2a/sign',headers=header,json=json_data)
        print(response)
        time.sleep(20)
        self.driver.save_screenshot('market_sell_complete_.png')
        return print("작품 판매 등록 완료")
    
    # 마켓 플레이스 작품 등록 후  양수도계약서 확인
    def test_case8(self):
        self.driver.find_element(By.XPATH,"/html/body/div/div/div/div/div/div/div/div[6]/a[2]").click()


    #market place 에서 첫번째 작품 구매 테스트    
    def test_case9(self):
    	# ABC Test의 테스트케이스 함수
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.LINK_TEXT,"Market").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.CLASS_NAME,"drop-container").click()
        self.driver.implicitly_wait(10)
        self.driver.execute_script("window.scrollTo(0, 700)")
        self.driver.find_element(By.XPATH,f'//button[contains(text(), "구매하기")]').click()
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH,"/html/body/div/div/div/div/div/div/div[2]/div[3]/a[2]").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH,"/html/body/div[3]/div/div[2]/div/div/div[3]/div/a").click()
        self.driver.implicitly_wait(10)
        #스크롤
        self.driver.execute_script("window.scrollTo(0, 700)")
        
        # 약관 동의 버튼 3개 클릭
        self.driver.find_element(By.XPATH,"/html/body/div/div/div/div/div/div/div[2]/div[4]/div/div/div/div[1]/div/label/span[1]/input").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH,"/html/body/div/div/div/div/div/div/div[2]/div[4]/div/div/div/div[2]/div/label/span[1]/input").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH,"/html/body/div/div/div/div/div/div/div[2]/div[4]/div/div/div/div[3]/div/label/span[1]/input").click()
        self.driver.implicitly_wait(10)
        

        #결제 하기 버튼 클릭
        self.driver.find_element(By.XPATH,"/html/body/div/div/div/div/div/div/div[2]/div[7]/a[2]").click()
        #self.driver.find_element(By.XPATH,"/html/body/div/div/div/div/div/div/div[2]/div[3]/a[2]").click()
        # drops 로그인 시 , a2a requestkey 가 생성 됨 
        # 해당 request key 는 /v2/account/prepare api 응답 값에 있음 
        # 네트워크를 캡처 하면서 /v2/account/prepare api가 나타 날 때 까지 기달림 (seleniumwire 를 사용해야 해당 기능 사용 가능함)
        request=self.driver.wait_for_request('.*/purchase.*')
        while request.method != "POST"  :
            del self.driver.requests
            request=self.driver.wait_for_request('.*/purchase.*')
        if request.method == "POST" :
            status_code = request.response.status_code
            print(f'{request.url}, 응답코드 {request.response.status_code}, 컨텐츠 유형: {request.response.headers}')
            response_str = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity')).decode('utf-8')
            assert status_code == 200, f'{request.url} 요청에 대한 응답 실패: {status_code}: {response_str}'
            response_json = json.loads(response_str)
            print(response_json)
            requestsKey = response_json['request_key']
            print(requestsKey)
            #새탭을 열고 klip a2a 주소 (endpotin+requestkey 결합된 주소 ) 로 이동 
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get("https://qa2.klipwallet.com/?target=a2a?request_key="+requestsKey)
            self.driver.implicitly_wait(10)
            self.driver.find_element(By.XPATH,f'//button[contains(text(), "다음")]').click()
            #klip pin 번호 입력(텍스트 포함 문자 찾아서 입력)
            self.driver.find_element(By.XPATH,f'//button[contains(text(), "1")]').click()
            self.driver.find_element(By.XPATH,f'//button[contains(text(), "2")]').click()
            self.driver.find_element(By.XPATH,f'//button[contains(text(), "1")]').click()
            self.driver.find_element(By.XPATH,f'//button[contains(text(), "2")]').click()
            self.driver.find_element(By.XPATH,f'//button[contains(text(), "1")]').click()
            self.driver.find_element(By.XPATH,f'//button[contains(text(), "2")]').click()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.save_screenshot('market_purchase_complete.png')
    
    #def test_case2(self):
    #양수도계약서 본문 추출 할 경우 element 찾아서 text 를가져와서 for문 돌린 다음에 .text 함수를 사용해 돌린다 =>.text 함수가 있는지 알아 봐야 한다.
       #news_titles = self.driver.find_elements_by_css_selector(".news_tit")
        #for i in news_titles:
            #title = i.text()
            # print(title)


        

        
        




        
        


if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(report_title="drops sanity test result"))
    
    
