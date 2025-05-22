import requests
from bs4 import BeautifulSoup as bs
import fake_useragent
import json

user = fake_useragent.UserAgent().random
headers = {'user-agent': user}
result = []
with open('link_parser.json', 'r', encoding='utf-8') as f:
    url_items = json.load(f)

for item in url_items:
    try:
        url = item['Ссылка']
        print(f'Обрабатываю: {url}')

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = bs(response.text, 'lxml')

        name = soup.find('span', class_='hidden').text.strip() if soup.find('span', class_='hidden') else 'Не найдено'
        price = soup.find('div', class_='product-detail__sale-price--black').text.strip() if soup.find('div', class_='product-detail__sale-price--black') \
            else soup.find('div', class_='price').text.strip()
        desc = soup.find('div', class_='ss').text.strip() if soup.find('div', class_='ss') else 'Не найдено'

        sizes = []
        try:
            # Ищем все элементы с размерами
            size_containers = soup.find_all('div', class_=lambda x: x and 'size_it' in x)

            for container in size_containers:
                # Ищем русский размер
                rus_size = container.find('span', class_='rus')
                if rus_size:
                    size_text = rus_size.text.strip()
                    if size_text:
                        # Проверяем доступность
                        if rus_size.get('data-availability') == 'Y':
                            sizes.append(size_text)
        except Exception as size_error:
            print(f'Ошибка при парсинге размеров: {size_error}')
        if not sizes:
            sizes.append('Нет в наличии')
        result.append({
            'url': url,
            'name': name,
            'price': price,
            'description': desc,
            'sizes': sizes
        })

    except KeyError:
        print(f'Ошибка: в элементе отсутствует ключ "Ссылка": {item}')
    except Exception as e:
        print(f'Ошибка при обработке {url}: {str(e)}')

with open('parsed_data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4, sort_keys=True)

print(f'Обработано {len(result)} из {len(url_items)} страниц')














