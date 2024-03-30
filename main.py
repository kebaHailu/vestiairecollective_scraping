import time 
from selenium import webdriver as wd 
from selenium.webdriver.common.by import By 


url = 'https://www.vestiairecollective.com/men/#gender=Men%232'

driver = wd.Chrome() 
driver.get(url) 
time.sleep(20)
elemnts = driver.find_elements(By.XPATH,'//*[@id="__next"]/div/main/div[3]/div/div[1]/div[2]/div[2]/ul')
time.sleep(10)
for elemnt in elemnts:
    print(elemnt.text)
    link = elemnt.find_elements(By.CLASS_NAME, 'un-helper-link')
    for lnk in link:
        print(lnk.text)


driver.quit()


# elements 
# link - //*[@id="product_id_42756977"]/div[3]/a[1], //*[@id="product_id_42774659"]/div[3]/a[1]

# detail 
# //*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul


# general info 
# '''
# Online since:2024-03-29
# Categories :Men
# Category:Clothing
# Sub-category:Shirts
# Designer:Louis Vuitton
# Condition:Very good conditionMore info
# Material:Cotton
# Color:Black
# Size:XL InternationalSizing guide
# Location:United States, from the seller Ningen
# Reference:42756977
# '''

# /html/body/div[2]/div/main/div[3]/div/div[1]/div[2]/div[2]/ul/li[2]/div
# //*[@id="product_id_42781397"]/div[3]/a[1]
# //*[@id="product_id_42781397"]