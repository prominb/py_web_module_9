import requests
from bs4 import BeautifulSoup
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from model import Book, Base


def parse_data():  # Отримуємо дані для книги
    rate_to_number = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    url = 'http://books.toscrape.com/'
    store_ = []  # зберігатимемо отримані дані
    html_doc = requests.get(url)  # виконуємо запит до сайту

    if html_doc.status_code == 200:
        soup = BeautifulSoup(html_doc.content, 'html.parser')  # Виконуємо парсинг даних з HTML коду.
        books = soup.select('section')[0].find_all('article', attrs={'class': 'product_pod'})  # Знаходимо всі книги запитом.
        for book in books:  # в циклі із картки кожної книги починаємо діставати інформацію.
            img_url = f"{url}{book.find('img')['src']}"  # Обкладинку книги дістаємо з атрибуту src тегу img. Варто зауважити, що шлях до обкладинки книги всередині тегу src - відносний media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg. Щоб він був функціональним, необхідно перетворити його на абсолютний шлях. Для цього потрібно підставити на початку шляху значення змінної url.
            rating = rate_to_number.get(book.find('p', attrs={'class': 'star-rating'})['class'][1])  # Рейтинг книги знаходиться як назва класу у тезі p. Але зберігати в базі даних (БД) краще числове значення рейтингу. Для цього ми ввели словник Який і буде перетворювати ім'я класу в число
            title = book.find('h3').find('a')['title']  # Назву книги ми отримуємо з атрибуту title тегу a. Оскільки всередині картки книги два теги a, ми конкретизуємо пошук.
            price = float(book.find('p', attrs={'class': 'price_color'}).text[1:])  # І останнім ми отримуємо ціну книги. Видаляємо префікс £ з ціни і приводимо її до числа.
            store_.append({
                'img_url': img_url,
                'rating': rating,
                'title': title,
                'price': price
            })  # Останній етап - поміщаємо словник із даними книги у список store_.

    return store_


if __name__ == '__main__':
    store = parse_data()
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    Session = sessionmaker(bind=engine)
    session = Session()
    for el in store:
        book = Book(img_url=el.get('img_url'), rating=el.get('rating'), title=el.get('title'), price=el.get('price'))
        session.add(book)
    session.commit()
    books = session.query(Book).all()
    for b in books:
        print(vars(b))
    session.close()
