from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re
import time

class CryptoPanic:

    def GetSource(self):
        dictionary = {}
        base_url = "https://cryptopanic.com"
        driver = webdriver.Chrome('/home/ubuntu/chromedriver')
        driver.get(base_url)
        html = driver.execute_script("return document.documentElement.outerHTML")

        soup = BeautifulSoup(html, 'html.parser').findAll('div', {"class": "news-cells"})

        for soup_block in soup[1:]:
            # soup_block OK
            try:
                block_url = soup_block.find("a", {"class": "news-cell nc-date"}).get("href")
                # print(block_url) OK
                url_inner = base_url+block_url
                driver_inner = webdriver.Chrome('/home/ubuntu/chromedriver')
                driver_inner.get(url_inner)
                html_inner= driver_inner.execute_script("return document.documentElement.outerHTML")

                soup_inner = BeautifulSoup(html_inner, 'html.parser')
                i = 0
                for element in soup_inner:
                    clean = re.compile('<.*?>')

                    div_header = element.find('div', {"class": "post-header"})
                    header = str(div_header.findAll('span', {"class": "text"})).strip()[20:-8]
                    #print("HEAD: " + header)

                    time.sleep(2)
                    #print('\n')
                    div_description= None
                    try:
                        div_description = element.find('div', {"class": "description-body"})
                        if div_description is None:
                            div_description = element.find('div', {"class": "post-body"}).getText()
                        if div_description is None:
                            div_description = element.find('div', {"class": "pad"}).find('a', {"class": "reddit-url"}).get("href")
                    except:
                        span_ls = element.find('div', {"class": "reddit-container"}).findAll('span')  # .find('a', {"class": "reddit-post"}).get("href"))
                        for span in span_ls:
                            if 'class="text"' in str(span):
                                div_description = span.getText()
                                print(div_description)
                            else:
                                div_description = None
                    descriprion = re.sub(clean, '', str(div_description))
                    #print("DESCRIPTION: " + descriprion.strip())
                    time.sleep(2)
                    s = "".join({"d","f"})
                    #print('\n')

                    T = (header, descriprion,)
                    dictionary[i] = T
                    print(str(dictionary[i][0]))
                    print(str(dictionary[i][1]))
                    print('\n')#dictionary[key][tuple(0)-head, tuple(1)-description
                    i = i+1


            except:
                continue


if __name__ == "__main__":
    cryptopanic = CryptoPanic()
    cryptopanic.GetSource()