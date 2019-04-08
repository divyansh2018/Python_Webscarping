import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as ureq
import re



def GetProductData(product_text):
    txt=product_text.replace(',','')
    x = re.findall('?+\d+?\d+% off', txt)
    y = re.findall('?+\d+[A-Za-z]', txt)
    for p in x:
        txt=txt.replace(p,p+',')
    for p1 in y:
        txt=txt.replace(p1,p1[:-1]+','+p1[-1])
    pr_list=txt.split(',')
    
    final_list=[i.split('?') for i in pr_list if i!='']
    df=pd.DataFrame(final_list)
    df=df.iloc[:,:3]
    df.columns=['Product Name','Purchase Price','Original Price']
    df[['Discount %','Original Price']]=pd.DataFrame(df['Original Price'].apply(string).tolist(), index= df.index)


    df['Purchase Price']=df['Purchase Price'].apply(do_int)
    df=df.dropna(subset=['Purchase Price'])
    return df



def string(x):
    try:
        return [x[-7:],x[:-7]]
    except TypeError:
        return ['','']
    
    
    
def do_int(x):
    try:
        return int(x)
    except:
        return np.nan


def ProductTextData(url):
    item_html = ureq(url)
    page_html = item_html.read()
    item_html.close()
    page_soup = soup(page_html,'html.parser')
    f_containers = page_soup.find_all('div',{"class" : "_3O0U0u _288RSE"})
    new_contain_list=[]

    for contain in f_containers:
        
#         print(contain.text)
        new_contain_list.append(contain.text)
        
        
    return new_contain_list






def FlipkartProductData(pattern,page):
    flipkart_search_url = "https://www.flipkart.com/search?q="
    search = pattern.replace(" ", "%20")
    flipkart_url = flipkart_search_url+search
    flipkart_final_url = [flipkart_url+'&page='+str(i) for i in range(0,int(page))]
    
    new_contain_list=[j for i in list(map(ProductTextData,flipkart_final_url)) for j in i]
    
    f =pd.concat(list(map(GetProductData,new_contain_list)))
    return f

    
if __name__=='__main__':
    pattern = input("Please Enter your search item : ")
    page=input("No.of pages : ")
    df=FlipkartProductData(pattern,page)
    df=df.reset_index(drop=True)