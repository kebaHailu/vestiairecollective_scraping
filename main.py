import time , csv, subprocess , sys


try:
    from selenium import webdriver as wd
    from selenium.webdriver.common.by import By 
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'selenium'])
finally:
    from selenium import webdriver as wd 
    from selenium.webdriver.common.by import By 
    from selenium.webdriver.support.ui import WebDriverWait as ww , Select
    from selenium.webdriver.support import expected_conditions as EC 
    



###########  Collect Paths  ###########
## Collect all possible paths where we can find products ## 

values = {
    'men': ['men','#gender=Men%232',21],
    'women': ['women','#gender=Women%231',21],
    'kids': ['kids','#gender=Kids%233',21],
    'we-love': ['we-love','',21],
    'new-items': ['new-items','',21],
    'vintage': ['vintage','',21]
}
def get_url(value,cur):
    return f'https://www.vestiairecollective.com/{value[0]}/p-{cur}/{value[1]}'
urls = []
urls.append('https://www.vestiairecollective.com/vintage/')
urls.append('https://www.vestiairecollective.com/we-love/')
urls.append('https://www.vestiairecollective.com/kids/')
urls.append('https://www.vestiairecollective.com/men/')
urls.append('https://www.vestiairecollective.com/women/')
urls.append('https://www.vestiairecollective.com/new-items/')
for val in values.values():
    for i in range(2,val[2]+1):
        urls.append(get_url(val,i))
###########  Collect Paths  ###########       

# custome find element function to remove exception 
def find_element(body, path):
    try:
        res = body.find_elements(By.XPATH, path)
        if len(res) > 0:
            take =  res[0].text.strip()
            if take.startswith('(') and take.endswith(',)'):
                return take[1:len(take)-2]
            return take 
        return ""
    except:
        return ""



###########  make the final store ###########
## after every scrapping either the links or data will be stored permanently ## 

fnames = [ 'link']

# Read the existing data 
def read_csv_data():
    existing_data = []
    try:
        with open('data.csv', 'r', newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_data.append(row)
        return existing_data
    except FileNotFoundError:
        return []

def save_as_csv(data,fieldnames,finalname):

    for i in range(len(data)):
        dictdata = data[i]
        temp = dictdata.copy()
        for label in dictdata.keys():
            if label not in fieldnames:
                del temp[label]
        data[i] = temp.copy()
    with open(finalname, 'w',newline='',encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
 # Read existing data from the CSV file 
###########  make the final store ###########


########$$$$$ create a function which will change the dollar into other payment $$$$$#####
def change_price():
    #scroll to the end to access all objects in a page
    scroll_height = 0
    viewport_height = driver.execute_script("return window.innerHeight")
    scroll_increment = viewport_height // 20  # Adjust the scroll increment as desired

    while scroll_height < driver.execute_script("return document.documentElement.scrollHeight"):
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")
        scroll_height += scroll_increment

    time.sleep(2)
    

    # //*[@id="footer"]/div[1]/div/div[2]/button
    # /html/body/div[6]/div/div/div/div/div/form/div[1]/div[3]/div/select/option[3]
    # /html/body/div[6]/div/div/div/div/div/form/div[2]/div/button





driver = wd.Chrome() 
########### Start phase 1 scrapping ###########
## start the scrapping to access all avilable links for the product ##

########## uncomment if there is any error with links.csv file or want to add other links ##########
# all_links = set()
# for url in urls:
#     driver.get(url) 
    
#     #scroll to the end to access all objects in a page
#     scroll_height = 0
#     viewport_height = driver.execute_script("return window.innerHeight")
#     scroll_increment = viewport_height // 20  # Adjust the scroll increment as desired

#     while scroll_height < driver.execute_script("return document.documentElement.scrollHeight"):
#         driver.execute_script(f"window.scrollTo(0, {scroll_height});")
#         scroll_height += scroll_increment

#     time.sleep(2)
#     try:
#         #  to make the results per page 96
#         # btn = driver.find_element(By.XPATH,'//*[@id="__next"]/div/main/div[3]/div/div[2]/div[2]/div[1]/div[1]/button[2]')
#         # btn.click()
#         links = driver.find_elements(By.TAG_NAME,'a')  # Find all anchor elements
#         def last_check(link):
#             pos = ['men','women','kids']
#             return any(link.get_attribute('href').startswith('https://www.vestiairecollective.com/'+p+'-') for p in pos) and link.get_attribute('href').endswith('.shtml')
            

#         hrefs = {link.get_attribute('href') for link in links if link.get_attribute('href') if last_check(link)}
#         all_links.update(hrefs)
#         # save all links
#         links = [{'link': eachlink } for eachlink in all_links]
#         save_as_csv(links,fnames,'links.csv')
#         print(f'From the current page {len(hrefs)} links collected. Total collected links-{len(all_links)}')
#     except:
#         print("some error happend related to network")
########### finish phase 1 scrapping ###########

#access the stored link.csv file and convert it to the list
# all_stored_link = []
# products = read_csv_data()
# failed = []

# print(len(products))
# with open('link.csv', 'r') as file:
#     csv_reader = csv.DictReader(file)
#     for row in csv_reader:
#         link = row['link']
#         all_stored_link.append(link)



########### Start phase 2 scrapping ###########
## In this phase scrap all product pages and store there product ##
for href in range(2): #all_stored_link[len(products):]
    try:
        driver.get('https://www.vestiairecollective.com/men-clothing/shirts/prada/blue-cotton-prada-shirt-42804505.shtml')
        
        change_price()
        btn = driver.find_element(By.XPATH,'//*[@id="footer"]/div[1]/div/div[2]/button')
        btn.click()
        popup_element = ww(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[6]/div/div')))
        select_element = popup_element.find_element(By.CLASS_NAME, 'currency')
        select = Select(select_element)
        select.select_by_value('GBP')
        popup_btn = popup_element.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div/div/form/div[2]/div/button')
        popup_btn.click()

        time.sleep(1)


        # this will change the price of the product

        product_detail = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul')
        var1 = find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div[1]/div/ul/li[1]/span[1]')
        var2 = find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div[1]/div/ul/li[2]/span[1]')
        var3 = find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div[1]/div/ul/li[3]/span[1]')
        var4 = find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div[1]/div/ul/li[4]/span[1]')
        var5 = find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div[1]/div/ul/li[5]/span[1]')
        var6 = find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div[1]/div/ul/li[6]/span[1]')
        var7 = find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div[1]/div/ul/li[7]/span[1]')
        var8 = find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div[1]/div/ul/li[8]/span[1]')
        var9 = find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div[1]/div/ul/li[9]/span[1]')
        var10 = find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div[1]/div/ul/li[10]/span[1]')
        var11 = find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div[1]/div/ul/li[11]/span[1]')


        fieldnames = [
            'Name', 'Price', 'price_with_discount', 'Image', 'Link','Designer:', 'Categories :', 'Sub-category:','Condition:', 'Online since:',
            'Color:', 'Material:', 'Category:','Discription', 'Location:' ,'Reference:','Size:','Measurement','Model:','Style:','Place of purchase:'
        ]


        product = {
            #//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div[1]/div/ul/li[11]/span[1]
            var1 : find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[1]/span[2]'),
            var2 : find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[2]/span[2]'),
            var3 : find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[3]/span[2]'),
            var4 : find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[4]/span[2]'),
            var5 : find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[5]/span[2]'),
            var6 : find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[6]/span[2]'),
            var7 : find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[7]/span[2]'),
            var8 : find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[8]/span[2]'),
            var9 : find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[9]/span[2]'),
           'Link': href,
        }
        if var10:
            product[var10] = find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[10]/span[2]'),
        if var11:
            product[var11] = find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[11]/span[2]')
        disc = find_element(driver,'//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[1]/p[1]')
        if disc:
            product['Discription'] = disc 
        measurement  = find_element(driver, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div[2]/div[1]/ul')
        if measurement:
            product['Measurement'] = measurement
        product['Price'] = find_element(driver, '//*[@id="__next"]/div/main/div[1]/div/div[3]/div/div[1]/div/div[2]/div/p/span[1]')
        product['price_with_discount'] = find_element(driver, '//*[@id="__next"]/div/main/div[1]/div/div[3]/div/div[1]/div/div[2]/div/p/span[2]')
        # image 
        image_element = driver.find_element(By.CLASS_NAME, 'vc-images_image__TfKYE')
        product['Image'] = image_element.get_attribute('src')
        product['Name'] = driver.title.split('-')[0]

        # products.append(product)
        # save_as_csv(products,fieldnames,'datas.csv')
    except Exception as e:
        # failed.append({'failed':href})
        # save_as_csv(failed,['failed'],'failed.csv')
        print(e)

########### finish phase 2 scrapping ###########

driver.quit()


