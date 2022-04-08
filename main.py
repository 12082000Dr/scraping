from bs4 import BeautifulSoup
import requests
import lxml
import csv
import time

# headers = {
#     'Accept' : '*/*',
#     'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.5.810 Yowser/2.5 Safari/537.36'
# }

startTime = time.time()

with open('index.html', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

all_catigories_duble = soup.find_all('div', class_='catalog-card')

all_catigories_urls = ["stupeni-napolnaya-plitka", 'keramogranit']

url = []

with open('mpolis.csv', 'w', encoding='cp1251', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(
        (
            "Название",
            "Цена",
            "Ссылка"
        )
    )

for item in all_catigories_duble:
    item_href_duble = item.find('a').get('href')
    all_catigories_urls.append(item_href_duble.split('/')[-2])

for i in all_catigories_urls:
    urls = f'https://mpolis-pro.ru/catalog/{i}/'
    url.append(urls)

for ur in url:
    for i in range(1, 100):
        try:
            url_product = ur + f'?PAGEN_1={i}'
            req = requests.get(url_product, headers)
            srcs = req.text
            soups = BeautifulSoup(srcs, 'lxml')
            blok = soups.find_all('div', class_='product_card__item card_content')


            for data in blok:
                name = data.find('div', class_='wrap_1').find(class_='card_content__title').text
                price = data.find('div', class_='wrap_1').find(class_='price__value').find('span', class_='current_price').text
                href = 'https://mpolis-pro.ru' + data.find('a').get('href')
                try:

                    with open('mpolis.csv', 'a', encoding='cp1251', newline='') as file:
                        writers = csv.writer(file, delimiter=';')
                        writers.writerow(
                            (name, price, href)
                        )
                except Exception as b:
                    print(f'Карточки закончились на {name, price, href}.')
                    continue

        except Exception as a:
            print(a)
            print(f'Страницы для url: "{ur}" закончились на {i}.')
            continue

endTime = time.time() #время конца замера
totalTime = endTime - startTime #вычисляем затраченное время
print(f"Время, затраченное на выполнение данного кода = {totalTime}")