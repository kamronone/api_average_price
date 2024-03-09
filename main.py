import requests

url = "http://<host>:<port>/property_price_percent"


data = {
    "district": "Яшнабадский район",
    "rooms": 2,
    "floor": 2,
    "floors": 4,
    "area": 30,
    "max_area": 100,
    "type_flat": "Новостройки",
    "type_build": "Кирпичный",
    "repair": "Средний",
    "layout": "Раздельная",
    "bathroom": "Раздельный",
    "furniture": "Нет",
    "price": 60000
}

response = requests.post(url, json=data)

if response.status_code == 200:
    result = response.json()
    print("Вот ваши данные:")
    print(f"Average Price: {result['price']}")
    print(f"Percent Difference: {result['percent']}%")
else:
    print(f"Ошибка: {response.status_code} - {response.text}")

