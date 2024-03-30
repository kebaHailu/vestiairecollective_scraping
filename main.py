import time 
import csv 
from selenium import webdriver as wd 
from selenium.webdriver.common.by import By 



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



def find_element(body, path):
    res = body.find_elements(By.XPATH, path)
    if len(res) > 0:
        return res[0].text 
    return ""

def save_as_csv(data):
    fieldnames = [
        'Name',
        'onine_since',
        'Image',
        'categories',
        'Category',
        'Sub-category',
        'Designer',
        'Condition',
        'Material',
        'Color',
        'Size',
        'Location',
        'Reference',
        'Price',
        'price_with_discount',
        'Link'


        
    ]
    filename = 'data.csv'
    with open(filename, 'w',newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)


products = []


driver = wd.Chrome() 
all_links = set()
for url in urls:
    driver.get(url) 
    
    #scroll to the end to access all objects in a page
    scroll_height = 0
    viewport_height = driver.execute_script("return window.innerHeight")
    scroll_increment = viewport_height // 30  # Adjust the scroll increment as desired

    while scroll_height < driver.execute_script("return document.documentElement.scrollHeight"):
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")
        scroll_height += scroll_increment

    time.sleep(3)
    try:
        #  to make the results per page 96
        # btn = driver.find_element(By.XPATH,'//*[@id="__next"]/div/main/div[3]/div/div[2]/div[2]/div[1]/div[1]/button[2]')
        # btn.click()
        links = driver.find_elements(By.TAG_NAME,'a')  # Find all anchor elements
        def last_check(link):
            pos = ['men','women','kids']
            return any(link.get_attribute('href').startswith('https://www.vestiairecollective.com/'+p+'-') for p in pos) and link.get_attribute('href').endswith('.shtml')
            

        hrefs = {link.get_attribute('href') for link in links if link.get_attribute('href') if last_check(link)}
        all_links.update(hrefs)
        print(len(hrefs),len(all_links))
    except:
        print("some error happend related to network")


for href in all_links:

    driver.get(href)
    time.sleep(5)
    try:


        product_detail = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul')
        product = {
            'onine_since':  find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[1]/span[2]'),
            'categories':  find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[2]/span[2]'),
            'Category':  find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[3]/span[2]'),
            'Sub-category': find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[4]/span[2]'),
            'Designer':  find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[5]/span[2]'),
            'Condition': find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[6]/span[2]'),
            'Material':  find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[7]/span[2]'),
            'Color':  find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[8]/span[2]'),
            'Size': find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[9]/span[2]'),
            'Location':  find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[10]/span[2]'),
            'Reference':  find_element(product_detail, '//*[@id="__next"]/div/main/section[1]/div/div/div[2]/div[2]/div/div/ul/li[11]/span[2]'),
            'Link': href,
        }
        product['Price'] = find_element(driver, '//*[@id="__next"]/div/main/div[1]/div/div[3]/div/div[1]/div/div[2]/div/p/span[1]')
        product['price_with_discount'] = find_element(driver, '//*[@id="__next"]/div/main/div[1]/div/div[3]/div/div[1]/div/div[2]/div/p/span[2]')
        # image 
        image_element = driver.find_element(By.CLASS_NAME, 'vc-images_image__TfKYE')
        product['Image'] = image_element.get_attribute('src')
        product['Name'] = driver.title 

        products.append(product)
    except:
        print("can't create because of network!")

    save_as_csv(products)

driver.quit()


# elements 

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