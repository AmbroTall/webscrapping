for x in range(1,50+1):
    # print(x)
    id = 2 + x
    if id < 10:
        id = f'0{id}'

    print(id)

# from anticaptchaofficial.recaptchav2proxyless import *
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import os
# import time
#
# path = '/home/ambrose/Documents/chromedriver'
# driver = browser = webdriver.Chrome(path)
#
# url = "https://www.georgiapublicnotice.com/Details.aspx?SID=bfixtn1mssfpyaloufw1oi5y&ID=2693871"
# page = driver.get(url)
#
# time.sleep(10)
#
# sitekey = driver.find_element(By.XPATH, '//*[@id="recaptcha"]').get_attribute('outerHTML')
# sitekey_clean = sitekey.split('" id')[0].split('data-sitekey="')[1]
# print(sitekey_clean)
# #
# solver = recaptchaV2Proxyless()
# solver.set_verbose(1)
# solver.set_key('dd32a7594766a876e1a80ebcdf16f840')
# solver.set_website_url(url)
# solver.set_website_key(sitekey_clean)
#
# g_response = solver.solve_and_return_solution()
# if g_response!= 0:
#     print("g_response"+g_response)
# else:
#     print("task finished with error"+solver.error_code)
#
# driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')
#
# driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""", g_response)
# driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')
#
# driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_btnViewNotice"]').click()
#
# time.sleep(20)