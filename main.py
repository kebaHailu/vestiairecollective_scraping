import time , csv, subprocess , sys


try:
    from selenium import webdriver as wd
    from selenium.webdriver.common.by import By 
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'selenium'])
finally:
    from selenium import webdriver as wd 
    from selenium.webdriver.common.by import By 



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
    res = body.find_elements(By.XPATH, path)
    if len(res) > 0:
        take =  res[0].text.strip()
        if take.startswith('(') and take.endswith(',)'):
            return take[1:len(take)-2]
        return take 
    return ""



###########  make the final store ###########
## after every scrapping either the links or data will be stored permanently ## 

fnames = [ 'link']
def save_as_csv(data,fieldnames,finalname):
    filename = finalname
    with open(filename, 'w',newline='',encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
###########  make the final store ###########



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
all_stored_link = []
products = []
with open('links.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        link = row['link']
        all_stored_link.append(link)



########### Start phase 2 scrapping ###########
## In this phase scrap all product pages and store there product ##
for href in all_stored_link:
    driver.get(href)
    time.sleep(1)
    try:
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

        products.append(product)
        save_as_csv(products,fieldnames,'data.csv')
    except Exception as e:
        print(e)

########### finish phase 2 scrapping ###########

driver.quit()





#  usefull elements for vestiairecollective

# link - //*[@id="product_id_42756977"]/div[3]/a[1], //*[@id="product_id_42774659"]/div[3]/a[1]

# next - //*[@id="__next"]/div/main/div[3]/div/div[2]/div[2]/div[1]/div[2]/button[9]/span[1]
# dd     //*[@id="__next"]/div/main/div[3]/div/div[2]/div[2]/div[1]/div[2]/button[10]/span[1]


# detail 
# //*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul
# //*[@id="__next"]/div/main/div[1]/div/div[3]/div/div[1]/div/div[2]/div/p/span[1] price
# //*[@id="__next"]/div/main/div[1]/div/div[3]/div/div[1]/div/div[3]/p[1] size 

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