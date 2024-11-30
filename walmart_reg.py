

import os, time, random, string, re
import reg_mail, otp_fetch
from free_proxies import FreeProxy

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
import undetected_chromedriver as uc

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager



file = 'data.txt' # tuỳ biến

companyName = ""
ein = ""
address = ""
phoneNum = ""
zipcode = ""

# Hàm để lọc tách thông tin
def extractInfo(filename):
    global companyName, ein, address, phoneNum, zipcode

    with open(filename, 'r') as file:
        lines = file.readlines()


        for i in range(len(lines)):
            line = lines[i].strip()

            # Tìm tên công ty theo logic cách 5 dòng
            if i % 5 == 0:
                companyName = line

            # EIN
            elif line.startswith("EIN Number"):
                ein = line.replace("EIN Number: ", "")

            # phone
            elif line.startswith("Phone"):
                phoneNum = line.replace("Phone: ", "")

            # zipcode
            elif line.startswith("Zip Code"):
                zipcode = line.replace("Zip Code: ", "")


# zip code
# 32003 · 32008 · 32009 · 32011 · 32013 · 32024 · 32025 · 32033 · 32034 · 32038 · 32040 · 32043 · 32044 · 32046 · 32052 · 32053 · 32054

# Tên bang ở Mỹ cho phần chọn state
stateMapping = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DC": "District of Columbia", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana",
    "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Montana", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia",
    "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", "AA": "Armed Forces Americas",
    "AP": "Armed Forces Pacific", "AE": "Armed Forces Europe", "AS": "American Samoa", "GU": "Guam",
    "MP": "Northern Mariana Islands", "PW": "Palau", "PR": "Puerto Rico", "VI": "Virgin Islands"
}
# Hàm tìm mã tiểu bang từ tên tiểu bang
def getStateCode(stateName):
    for code, name in stateMapping.items():
        if name.lower() == stateName.lower():
            return code
    return None

# Đọc tệp và lọc thông tin địa chỉ
def parseAddr(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        # Tìm dòng chứa từ "Address:"
        if line.startswith("Address:"):
            # Tách lấy phần tên tiểu bang từ địa chỉ
            addressParts = line.split(',')[-1].strip()
            global stateName, city
            stateName = addressParts.split(',')[-1].strip() # Lấy phần tên tiểu bang từ trước dấu phẩy cuối
            city = line.split(',')[-2].strip() # Tương tự cách 2 dấu phẩy
            stateCode = getStateCode(stateName)
            select.select_by_value(stateCode)
##########################################################################################################
def clrscr():
    os.system('cls' if os.name == 'nt' else 'clear')

def click(xpath):
    driver.find_element(By.XPATH, xpath).click()

def webDriverWait(ID, var):
    return WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, ID))).send_keys(var)




def main():
    clrscr()
    if not os.path.exists('email.txt') or os.stat('email.txt').st_size == 0: # Nếu email rỗng thì tạo email, else ...
        reg_mail.main()
        main()
    else:
        with open(r"./email.txt", 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # lọc từng dòng file email
            for line in lines:
                if line.strip():
                    free_proxy = FreeProxy()
                    print("Getting proxy list...")
                    proxy_list = free_proxy.get_proxy_list()
                    print(proxy_list)

                    for _ in range(2):
                        random_proxy = random.choice(proxy_list)
                        print(random_proxy)

                        email, password = line.strip().split(':') # Tách ký tự :
                        options = ChromeOptions()
                        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
                        # Tránh detect
                        options.add_argument('--disable-blink-features=AutomationControlled')
                        options.add_argument(f"--proxy-server={random_proxy}")
                        options.add_argument('--ignore-ssl-errors=yes')
                        options.add_argument('--ignore-certificate-errors')
                        options.add_argument('--allow-insecure-localhost')
                        # options.add_argument("--headless=new") --> Ẩn hiện Chrome
                        # service = webdriver.ChromeService(log_output="./driver.log") --> Log
                        options.add_argument("--start-maximized") # Toàn màn hình
                        global driver
                        driver = uc.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) # Nếu muốn hiển thị log thì thêm service=service vào

                        random_name = ''.join(random.choices(string.ascii_letters, k=6)) # Dùng để tạo tên ngãu nhiên

                        try:
                            if line.startswith("Address:"):
                                # Tách lấy phần tên tiểu bang từ địa chỉ
                                addressParts = line.split(',')[-1].strip()
                                global stateName, city, stateCode
                                city = line.split(',')[-2].strip()
                                stateName = addressParts.split(',')[-1].strip() # Lấy phần tên tiểu bang từ trước dấu phẩy cuối
                                stateCode = getStateCode(stateName)
                            driver.get("https://business.walmart.com") # truy cập web

                            # if driver.current_url.startswith("https://business.walmart.com/blocked"):
                            #     time.sleep(10)
                                # click('/html/body/div/a/svg/g/path[4]') # Nút icon con người
                                # time.sleep(12) # Chờ hiện nút press again
                                # click('/html/body/div/div/div[2]/div[2]/p') # Nút press again
                                # click('/html/body/div[2]/div/div[2]/div[1]/div/div[1]/button') # Ấn dấu X khi lần đầu vào web
                                # time.sleep(2)
                            click('/html/body/div[2]/div/div[2]/div[1]/div/div[1]/button') #Ấn dấu X khi lần đầu vào web
                            click('/html/body/div/div[1]/section/div/div/div/a') # Ấn Get started để sign up

                            # WebDriverWait chờ tối đa 1 giây để tìm phần tử khi phần tử này xuất hiện, chương trình sẽ tự động nhập
                            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'ld_ui_textfield_0'))).send_keys(random_name) # Nhập First name
                            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'ld_ui_textfield_1'))).send_keys(random_name) # Nhập Last name
                            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'ld_ui_textfield_2'))).send_keys(email) # Nhập Email
                            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'ld_ui_textfield_3'))).send_keys(password) # Nhập Password
                            click('//button[@type="submit"]') # Continue
                            time.sleep(5)


                            # if driver.current_url.startswith("https://identity.walmart.com/account/signup"):
                            #     # Bước xác minh Human (Nếu xuất hiện)
                            #     click('/html/body/div/a/svg/g/path[4]') # Nút icon con người
                            #     time.sleep(12) # Chờ hiện nút press again
                            #     click('/html/body/div/div/div[2]/div[2]/p') # Nút press again
                            if driver.current_url.startswith("https://identity.walmart.com/account/verifyyouraccount?scope="):
                                otp = otp_fetch.main()
                                # Nhập otp 6 số
                                driver.find_element(By.XPATH, '/html/body/div/section/div/form/fieldset/div[1]').send_keys(otp)

                                time.sleep(1)
                                click('/html/body/div/section/div/form/button') # Verify
                                # OTP
                            else:
                                # name
                                webDriverWait('react-aria7775843507-:r1:', companyName)
                                # EIN
                                webDriverWait('react-aria7775843507-:r4:', ein)
                                # I'm a sole proprietor
                                webDriverWait('react-aria6381866530-:r5:', '')
                                # phone num
                                webDriverWait('react-aria7775843507-:r6:', phoneNum)
                                # address
                                webDriverWait('addressLineOne', stateName)
                                #city
                                webDriverWait('react-aria7775843507-:rc:', city)
                                #zip code
                                webDriverWait('react-aria7775843507-:rg:', zipcode)
                                # state
                                global select
                                select = Select(driver.find_element(By.ID, 'react-aria59907744-:re:'))
                                parseAddr(file)
                                click('//*[@id="org-create-form"]') #submit


                        except Exception as e:
                            print(f"{email} - \033[31mERROR\033[37m")

                        finally:
                            driver.close()

main()
