import selenium
import requests
import json
from selenium import webdriver
from itertools import cycle
driver = webdriver.Firefox()
# Getting proxies from the stated website to rotate scraping requests from
def get_proxies():
    url = 'https://www.freeproxylists.net/?c=US&pt=&pr=HTTPS&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=0'
    driver.get(url)
    #driver.get(input("Enter proxy list url: ")) #put url to scrap here
    proxies=[]
    tbody = driver.find_element_by_class_name("DataGrid") # store the table data to tbody 
    cell = tbody.find_elements_by_tag_name("tr") # find all table rows and store it
    cell.pop(0)
    for column in cell:
        try:
            column = column.text.split(" ")
            proxies.append(column[0]+":"+column[1])
        except:
            continue
        
    return proxies

# Scraping the website for price, name, manufacturer, in or out of stock
proxy_list = get_proxies()
proxy_cycle = cycle(proxy_list)
proxy = next(proxy_cycle)
requests.get('https://www.midsouthshooterssupply.com', proxies={'https': proxy})
product_link = []
for x in range(1,3):
      driver.get(f'https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage={x}')
      products = driver.find_elements_by_class_name('product')      
      for product in products:
          link = product.find_element_by_class_name('catalog-item-name')
          product_link.append(link.get_attribute("href"))
product_data_list = []
for link in product_link:
    driver.get(link)
    name = driver.find_element_by_class_name('product-name')
    infos = driver.find_element_by_class_name('product-info')
    price = infos.find_element_by_xpath("/html/body/form/main/div/section/div[1]/div[3]/div[1]/span/span")
    manufacturer = driver.find_element_by_xpath('/html/head/meta[25]')
    
    try:
       driver.find_elements_by_class_name('out-of-stock')
       stock = 'false'
    except:
        stock = 'true'
    product_data = {
        'name' : name.text,
        'price' : price.text,
        'manufacturer' : manufacturer.get_attribute("content"),
        'stock' : stock
    }
    product_data_list.append(product_data)
json_object = json.dumps(product_data_list, indent = 4)
print(json_object)
