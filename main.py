import requests,os,lxml,re,json
from bs4 import BeautifulSoup
import csv

f=open('all_urls.txt','r')
all_urls=f.read().split()

columns=[]

for every_url in all_urls[50:]:
  print(every_url)
  idd=every_url.split('/')[-1]


  Source_Website='northernsafety.com'

  #idd=30799

  url='https://www.northernsafety.com/Product/'+str(idd)
  html=requests.get(url)
  soup = BeautifulSoup(html.text, 'lxml')
  title=soup.find('h2',{'class':'material-header'}).text

  all_div=soup.find('div',{'class':'tab-pane hidden-print'})
  Shipping_Information=all_div.text.strip()
  Source_url=every_url


  scs=soup.findAll('script')
  data=scs[-4].text.strip()
  j=data[664:-616].strip()
  j='{ "product"'+j+"}"
  #print(j)
  #print(j)
  d = json.loads(j)
  #ds=[]
  Manufacturer=d['product']['brand']
  Item_Number=idd
  Product_Name=d['product']['materialName']

  Item_Detailed=d['product']['subheading']+"\n"
  for ev in d['product']['bulletPoints']:
    Item_Detailed+=ev+'\n'
  #print(Item_Detailed)
  Package_Size=d['product']['unitOfMeasure']
  Minimum_Quantity=d['product']['packaging']
  try:
    MSRP_Price=d['product']['availablePrices'][0]['pricings'][0]['price']
  except:
    MSRP_Price=d['product']['catalogHighestPrice']
  Stock=d['product']['stockStatuses'][0]['isAvailable']
  Stock='In Stock' if Stock==True else 'Out of Stock'
  #print(Stock)
  try:
    SDS=d['product']['sdsLinks'][0]['eLinkURL']
  except:
    SDS=''
  try:
    Catalog=d['product']['specSheet']['link']
  except:
    Catalog=""



  url1='https://www.northernsafety.com/Search?q='+title

  html1=requests.get(url1)
  soup1 = BeautifulSoup(html1.text, 'lxml')
  #getting category
  Category=soup1.find('div',{'class':'shop-by-category'}).find('a').find('span',{'class':'showFirstResultsText'}).text.strip()

  url2_p2=soup1.find('div',{'class':'shop-by-category'}).find('a')['href']
  url2='https://www.northernsafety.com'+url2_p2
  #print(url2)


  html2=requests.get(url2)
  soup2 = BeautifulSoup(html2.text, 'lxml')
  #getting sub category
  Sub_Category=soup2.find('div',{'class':'shop-by-category'}).find('a').find('span',{'class':'showFirstResultsText'}).text.strip()

  url3_p2=soup2.find('div',{'class':'shop-by-category'}).find('a')['href']
  url3='https://www.northernsafety.com'+url3_p2

  path="Home / "+Category+" / "+Sub_Category

  header = ['Source Website', 'Manufacturer', 'Manufacturer Number', 'Item Number', 'UPC#', 'UNSPSC#', 'Product Name', 'Item Detailed', 'Package Size', 'Minimum Quantity', 'MSRP (List) Price','Retail Price /Your Price', 'Get This Price', 'Discount You Save Amount', 'Discount You Save Percentage', 'Product Attributes Technical Specs', 'Features', 'Specification', 'Applications', 'Caution', 'In Stock','Category', 'Sub Category', 'Country Of Origin', 'Catalog', 'Guarantee Information', 'Shipping Information', 'Path', 'Source Url', 'Attribute Type 1', 'Attribute Value 1']

  column=[Source_Website,Manufacturer,'',Item_Number,'','',Product_Name,Item_Detailed.encode('utf-8'),Package_Size,Minimum_Quantity,MSRP_Price,'0','0','0','0','','','','','',Stock,Category,Sub_Category,'',Catalog,'',Shipping_Information.encode('utf-8'),path,Source_url,'SDS',SDS]
  columns.append(column)
  print("--Done--")

with open('Product_data.csv', 'a') as Top_Data_File:
  csv_writer = csv.DictWriter(Top_Data_File, fieldnames = header,lineterminator='\n')
  csv_writer.writeheader()
  writer = csv.writer(Top_Data_File,lineterminator='\n')
  writer.writerows(columns)
print('Data Saved')