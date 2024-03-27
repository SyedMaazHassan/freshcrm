import requests
from bs4 import BeautifulSoup as bs
import csv
import json
import os
from django.conf import settings

class HKTDC:
    def __init__(self, products_source=None):
        base_dir = settings.BASE_DIR
        if not products_source:
            products_source = os.path.join(base_dir, "products.csv")

        self.products_source = products_source
        self.base_url = 'https://sourcing.hktdc.com'
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    def collect_main_categories(self):
        #function to collect main categories and save as csv
        url=self.base_url+"/en/Categories" 
        r = requests.get(url,headers=self.headers)
        soup=bs(r.text,'html.parser')
        links=soup.find_all('a',class_='category-table-link-to')
        
        links= [(link.text,self.base_url+link['href']) for link in links if link['href']!="#"]
        with open("category.csv","w",newline="") as f:
            writer= csv.writer(f)
            writer.writerows(links)
    
    # def get_cate

    def collect_sub_categories(self):
        #function to collect sub categories and save as csv
        csvfile = self.products_source
        category={}
        count=0
        item_list=[]
        with open(csvfile) as f:
            reader=csv.reader(f)
            
            for row in reader:
                url=row[1]
                
                main_category=row[0]
                category[main_category]=[]
                r = requests.get(url,headers=self.headers)
                
                soup=bs(r.text,'html.parser')
                cat2items=soup.find_all('div',class_='category-level2_container')
                tempcat2={}
                cat_list2=[]
                for cat2item in cat2items:
                    temp=[]    
                    temp.append(main_category)
                    temp.extend([url])
                    
                    text,link=cat2item.find("a").text,cat2item.find("a")['href']
                    tempcat2[text]=link                 
                    level3=cat2item.find("div",class_="category-level3_container")
                    items=level3.find_all("a")
                    tempcat3={}
                    cat_list3=[]
                    temp.extend([text])
                    temp.extend([self.base_url+link])
                    for item in items:
                        temp2=[]
                        temp.extend([item.text])
                        temp.extend([self.base_url+item['href']])
                        tempcat3[item.text]=item['href']
                        
                    cat_list3.append(tempcat3)
                    #items=dict([(item.find("a").text,item.find("a")['href']) for  item in cat2] )
                    item_list.append(temp)
                    
                cat_list2.append(tempcat2)
                #print(items)
                category[main_category].append(cat_list2)
        with open(self.products_source,"w",newline="") as f:
            writer= csv.writer(f)
            writer.writerows(item_list)
        
    def save_source(self,source,category):
        #helper function to save source
        with open('hktdc_'+category+'.html','w',encoding='utf-8') as f:
            f.write(source) 

    def get_json(self,item_name,item,page):
        #this function is to get json data from the page
        
        item= json.loads(item.text)
        datalist=item['props']['pageProps']['result']['dataList']
        result=[]
        for item in datalist[str(page)]:
                temp={}
                company_info=item['companyInfo']
                #company_info=item['companyInfo']   
                temp["name"]=company_info['name']
                
                temp["urn"]=company_info['urn']
                temp["country"]=company_info['countryAndRegion']
                temp["products"]=";".join(list(set(company_info['productNames'])))
                temp["brandame"]=";".join(company_info['brandName']) if company_info['brandName'] else ""
                result.append(temp)
                
        flname=f"{item_name}.csv"    
        write_header=False
        if not os.path.exists(flname):
            write_header=True
        
        with open(f"{item_name}.csv","a",newline="",encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=["name","urn","country","products","brandame"])
            if write_header:
                writer.writeheader()
            writer.writerows(result)    
        
    
    def get_product_suppliers(self,item_name,product_url):
        #function loop through each produc_url and collects the supplier data
        
        r = requests.get(product_url,headers=self.headers)
        
        soup=bs(r.text,'html.parser')
        records=soup.find("span",class_="search-result-total").text
        item=soup.find("script",attrs={"id":"__NEXT_DATA__"})
        if item:
            self.get_json(item_name,item,page=1)
        else:
            print("No item found")
            return    
        if records:
            records=records.split(":")[-1].strip()
            records=int(records)
            pages,rem= divmod(records,24)
            if rem>0:
                pages+=1
            
            if pages>0:
                for page in range(2,pages+1):
                    url=product_url+f"?page={page}"
                    r = requests.get(url,headers=self.headers)
                    soup=bs(r.text,'html.parser')
                    item=soup.find("script",attrs={"id":"__NEXT_DATA__"})
                    if item:
                        self.get_json(item_name,item,page)
                    
        else:
            print("No more pages found")
        
    def get_item_list(self):
        #function to get item list from csv which is saved from collect_sub_categories
        #and to pass each product_url to get_product_suppliers and save the data as csv
        csvfile = self.products_source
        item_list=[]
        with open(csvfile) as f:
            reader=csv.reader(f)
            for row in reader:
                item_list.append(row)
        return item_list

    def get_item_list_json(self):
        return json.dumps(self.get_item_list_dict())

    def get_item_list_dict(self):
        data = self.get_item_list()
        json_data = {}
        
        for i in range(len(data)):
            row = data[i]
            category_name = ""
            sub_category_name = ""
            for j in range(0, len(row), 2):
                first_index = row[j]
                second_index = row[j+1]

                if j == 0:
                    data_type = "Category"
                    category_name = first_index
                    if category_name not in json_data:
                        json_data[category_name] = {}
                elif j == 2:
                    data_type = "Sub Category"
                    sub_category_name = first_index
                    if sub_category_name not in json_data[category_name]:
                        json_data[category_name][sub_category_name] = []
                    
                else:
                    data_type = "Product"
                    if first_index and second_index:
                        json_data[category_name][sub_category_name].append({
                            'item_name': first_index,
                            'item_url': second_index
                        })

                # if first_index and second_index:
                #     print(data_type, first_index, second_index)

        
        return json_data


# if __name__ == '__main__':
#     products_source_path = "products.csv"
#     hktdc= HKTDC(products_source = products_source_path)
#     #hktdc.collect_main_categories()
#     #hktdc.collect_sub_categories()
#     #hktdc.get_hktdc('')
#     items=hktdc.get_item_list()
#     print(items)
#     for item in items:
#         index= item.index("")
#         item = item[2:index]
#         data=[ (item[i],item[i+1]) for i in range(0,len(item),2) if item[i]!="" ]
#         for item_data in data:
            
#             item_name=item_data[0]          
#             link=item_data[1]   
#             if link == "":
#                 continue
                
#             print(link)
#             link = link.replace("Product-Catalog","Suppliers")
            
#             hktdc.get_product_suppliers(item_name,link)
            
            
    
    
