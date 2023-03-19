# Download img from https://everia.club/
import sys
import requests
# from bs4 import BeautifulSoup
import threading
import time
import os
import re

#Get all jpg file url using BeautifulSoup

#def downURL(url):
#   res = requests.get(url)
#   soup = BeautifulSoup(res.text,'html.parser')
#   wp_elements = soup.find_all('figure', class_='wp-block-image size-large')
#   i = 1
#   jpgs=[]
#   for element in wp_elements:
#       jpg_src = element.find('img')['data-src']
#       #command = "wget -O "+ str(i)+" "+str(jpg_src)
#       #os.system(command)
#       jpgs.append(jpg_src)
#   return jpgs

#Get all jpg file using only regex
def downURL2(url):
    res = requests.get(url)
    wp_elements = re.findall("<figure.*?</figure>", res.text)
    jpgs=[]
    for jpg_url in wp_elements:
        jpgs.append(re.findall("(?<=data-src=\").*?(?=\" alt=)",jpg_url))
    return jpgs

def download_file(url, file_name):
    res = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:
        f.write(res.content)


if __name__ == '__main__':
    # Get url
    url = sys.argv[1]
    # make dir
    os.system('mkdir '+sys.argv[2])
    path = sys.argv[2]+"/"
    
    #multi thread download
    threads = []
    for i, uri in enumerate(downURL2(url)):
        file_name = f"{i}.jpg"
        thread = threading.Thread(target=download_file, args=(uri[0],path+file_name))
        thread.start()
        threads.append(thread)
