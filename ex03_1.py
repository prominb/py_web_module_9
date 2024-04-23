import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

# Пошук за CSS-селекторами Прості селектори
"""Прості селектори шукають елементи за ім'ям тегу, класом або ідентифікатором, за допомогою методу select.
Метод select дозволяє шукати елементи на основі CSS-селекторів.
Він приймає рядок із CSS-селектором і повертає всі елементи, що відповідають цьому селектору."""
# Знайдемо всі теги <p> на сторінці
p = soup.select("p")
# print(p)

# Знайдемо всі елементи з класом "text"
text = soup.select(".text")
# print(text)

# Знайдемо всі елементи з ідентифікатором "header". Ідентифікатор - це спеціальний атрибут тегу id.
header = soup.select("#header")
# print(header) # Як бачимо, таких елементів не існує та отримуємо порожній список. []


# Комбіновані селектори Комбіновані селектори шукають елементи, що відповідають кільком умовам.
# Наприклад, знайдемо всі елементи <a> всередині тегу <div> з класом "container":
a = soup.select("div.container a")
# print(a)


# Атрибути Можна шукати елементи за значенням атрибутів. Знайдемо всі елементи, у яких атрибут href починається з "https://"
# [<a href="https://www.goodreads.com/quotes">GoodReads.com</a>, <a href="https://scrapinghub.com">Scrapinghub</a>]
href = soup.select("[href^='https://']")
# print(href) # [<a href="https://www.goodreads.com/quotes">GoodReads.com</a>, <a class="zyte" href="https://www.zyte.com">Zyte</a>]


# Знайдемо всі елементи, у яких атрибут class містить слово "text":
ctext = soup.select("[class*='text']")
print(ctext)
