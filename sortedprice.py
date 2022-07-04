from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import numpy as np
import streamlit as st
# search
def searching_url(url, page):
    '''search
    return '''


# gpu 
st.write("""# price compare app for Newegg HK""")
product_name = st.text_input("what product you want to search for: \n")
search = st.button("search")
if search:
    product_name_html = product_name.replace(" ", "+")
#if "+" in product_name_html:
#    product_name_split = product_name.split(" ")
#    product_name = product_name_split[0]



    url = f"https://www.newegg.com/global/hk-en/p/pl?d={product_name_html}&N=4131"
    
    
    page = requests.get(url).text
    
    doc = BeautifulSoup(page, "html.parser")
    
    page_num = doc.find(class_="list-tool-pagination-text").strong
    
    page_num = str(page_num).replace("</strong>", "")
    
    page_num = int(page_num.split("<!-- -->")[-1])
    
    # initialization
    items_name = np.array([])
    items_prices = np.array([])
    items_links = np.array([])
    st.write(f"up to {page_num} pages")
    
    for page in range(page_num):
        url = f"https://www.newegg.com/global/hk-en/p/pl?d={product_name_html}&N=4131&page={page+1}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")
        table = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
        items = table.find_all(text=re.compile(product_name, re.I | re.S))

        df = pd.DataFrame({"item": [], "price": [], "link": []})
        for item in items:
            parent = item.parent
            link = None
            if parent.name != "a":
                continue
            link = parent['href']
            parent = item.find_parent(class_="item-container")
            if parent.name != "div":
                continue
            item_price_html = parent.find(class_="price-current").strong
            item_price = int(item_price_html.string.replace(",", ""))
            items_name = np.append(items_name, item)
            items_prices = np.append(items_prices, item_price)
            items_links = np.append(items_links, link)
    df = pd.DataFrame({"item": items_name, "price": items_prices, "link": items_links})
    df.set_index("item", inplace=True)
    df_sorted = df.sort_values('price')
    st.table(df_sorted)
            
        
