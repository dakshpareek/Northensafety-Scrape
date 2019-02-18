import requests,os,lxml,re,json
from bs4 import BeautifulSoup

'''Getting all the initial urls of category pages'''

html=requests.get('https://www.northernsafety.com/All-Categories')
soup = BeautifulSoup(html.text, 'lxml')
main_div=soup.find('div',{'id':'linksContainer'})
all_categories=main_div.findAll('ul',{'class':'list-unstyled'})
all_url_links=[]
temp='https://www.northernsafety.com/Search?i=1&m_show=96&q1={}&q2={}&sp_pr=v2&tp=json&x1=category-1&x2=category-2'
for every_category in all_categories[:-1]:
  header=every_category.find('a').text
  #print(header)
  main_urls=[i.text for i in every_category.findAll('a',{'class':'clearfix'})]
  for i in main_urls:
    i=i.replace('&','and')
    all_url_links.append(temp.format(header,i))
    break
  break

print(len(all_url_links))


def save_data(temp_data):
  f=open('all_urls.txt','a')
  f.writelines(temp_data)
  f.close()

'''Iterating Pages and Getting Every Product Url '''
#starting position
position=2

for ct,ev_url in enumerate(all_url_links[position:3]):
  all_ids_here=[]
  print("-----------Position: "+str(ct+position)+"-------------")
  chk=1
  page=1
  while chk != 0:
    print("Page="+str(page))
    t_url=ev_url+'&page='+str(page)
    html1=requests.get(t_url)
    #print(t_url)
    soup1 = BeautifulSoup(html1.text, 'lxml')
    scs=soup1.findAll('script')
    data=scs[-4].text.strip()


    data1=data.split('"materialBaseNumber":')
    dts=[]
    ck2=False
    for i in data1:
      idd=i.split('"')[1]
      if idd.isalnum():
        ck2=True
        all_ids_here.append('https://www.northernsafety.com/Product/'+str(idd)+'\n')
        #print(i.split('"')[1])
    #print("Total=",len(dts))
    if ck2==False:
      chk=0
    page+=1
    #chk=0
  print("Total=",len(all_ids_here))
  save_data(all_ids_here)


