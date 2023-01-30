import random
import os
import time
import json
import re
from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Chrome

url = "https://kaspi.kz/shop/nur-sultan/c/notebooks/?q=%3Acategory%3ANotebooks%3ANotebooks*Storage%20media%3ASSD%3ANotebooks*Internal%20RAM%3A16%20%D0%93%D0%B1%3ANotebooks*Display%20diagonal%3A15.6%20%D0%B4%D1%8E%D0%B9%D0%BC%D0%BE%D0%B2%3ANotebooks*Display%20diagonal%3A17.3%20%D0%B4%D1%8E%D0%B9%D0%BC%D0%BE%D0%B2%3AavailableInZones%3AMagnum_ZONE1&sort=relevance&page="

headers = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36"
}

product_data_list = []

count = 0
driver = Chrome("chromedriver")

for i in range(1, 31):
    driver.get(url + str(i))
    links = []

    src = driver.page_source
    soap = BeautifulSoup(src, "lxml")

    for link in soap.find_all("a", class_="item-card__image-wrapper"):
        links.append(link.get("href"))

    counter = 0

    for link in links:
        driver.get(link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 4);")
        time.sleep(3)
        src = driver.page_source
        with open(f"htmls/{counter}.html", "w") as file:
            file.write(src)
        counter += 1

    for i in range(0, 12):
        try:
            with open(f"htmls/{i}.html") as file:
                src = file.read()
        except:
            break

        soup = BeautifulSoup(src, "lxml")
        
        try:
            find_bitchass = soup.find("span", text=re.compile("Разрешение экрана")).find_next("dd").text
            title = soup.find("h1", class_="item__heading").text
            price = soup.find("div", class_="item__price-once").text

            frequency = soup.find("span", text=re.compile("Частота обновления экрана")).find_next("dd").text

            matrix = soup.find("span", text=re.compile("Тип матрицы")).find_next("dd").text
            resolution = soup.find("span", text=re.compile("Разрешение экрана")).find_next("dd").text
            installment = soup.find("div", class_="item__price-month").text
            diagonal = soup.find("li", text=re.compile("Диагональ экрана")).text
            key, value = diagonal.split(": ")
            diagonal = value
            processor = soup.find("li", text=re.compile("Процессор")).text
            key, value = processor.split(": ")
            processor = value
            videocard = soup.find("li", text=re.compile("Видеокарта")).text
            key, value = videocard.split(": ")
            videocard = value
            ram = soup.find("li", text=re.compile("Размер оперативной памяти")).text
            key, value = ram.split(": ")
            ram = value

            hddtype = soup.find("li", text=re.compile("Тип жесткого диска")).text
            key, value = hddtype.split(": ")
            hddtype = value

            memory = soup.find("li", text=re.compile("Общий объем накопителей")).text
            key, value = memory.split(": ")
            memory = value
        except:
            with open("brokenlinks.py", "w") as file:
                file.write(f"{links[i]}, ")
            continue
            

        title = soup.find("h1", class_="item__heading").text
        price = soup.find("div", class_="item__price-once").text

        frequency = soup.find("span", text=re.compile("Частота обновления экрана")).find_next("dd").text

        matrix = soup.find("span", text=re.compile("Тип матрицы")).find_next("dd").text
        resolution = soup.find("span", text=re.compile("Разрешение экрана")).find_next("dd").text
        installment = soup.find("div", class_="item__price-month").text
        diagonal = soup.find("li", text=re.compile("Диагональ экрана")).text
        key, value = diagonal.split(": ")
        diagonal = value
        processor = soup.find("li", text=re.compile("Процессор")).text
        key, value = processor.split(": ")
        processor = value
        videocard = soup.find("li", text=re.compile("Видеокарта")).text
        key, value = videocard.split(": ")
        videocard = value
        ram = soup.find("li", text=re.compile("Размер оперативной памяти")).text
        key, value = ram.split(": ")
        ram = value

        hddtype = soup.find("li", text=re.compile("Тип жесткого диска")).text
        key, value = hddtype.split(": ")
        hddtype = value

        memory = soup.find("li", text=re.compile("Общий объем накопителей")).text
        key, value = memory.split(": ")
        memory = value

        product_data_list.append({
            "Ссылка": links[i],
            "Название": title,
            "Цена":price,
            "Рассрочка":installment,
            "Диагональ экрана":diagonal,
            "Разрешение экрана":resolution,
            "Частота обновления экрана":frequency,
            "Тип матрицы":matrix,
            "Процессор": processor,
            "Видеокарта":videocard,
            "Размер оперативной памяти":ram,
            "Тип жесткого диска":hddtype,
            "Общий объем накопителей":memory,
        })
        count+=1
        print("Added " + str(count) + " item" + title)
    for i in range(0, 12):
        os.remove(f"htmls/{i}.html")

    with open("products_data.json", "a", encoding="utf-8") as file:
        json.dump(product_data_list, file, indent=4, ensure_ascii=False)


