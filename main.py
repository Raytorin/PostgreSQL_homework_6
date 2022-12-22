import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Sale, Stock, Book, Publisher, Shop


DNS = 'postgresql://postgres:postres@localhost:5432/sql_alchemy'
engine = sqlalchemy.create_engine(DNS)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


def create_insert_db():
    publisher_1 = Publisher(name='German')
    publisher_2 = Publisher(name='Пушкин')

    session.add_all([publisher_1, publisher_2])
    session.commit()

    book_1 = Book(title='Journey', publisher=publisher_1)
    book_2 = Book(title='Капитанская дочка', publisher=publisher_2)
    book_3 = Book(title='Руслан и Людмила', publisher=publisher_2)
    book_4 = Book(title='Евгений Онегин', publisher=publisher_2)

    session.add_all([book_1, book_2, book_3, book_4])
    session.commit()

    shop_1 = Shop(name='Лабиринт')
    shop_2 = Shop(name='Буквоед')
    shop_3 = Shop(name='Книжный дом')
    shop_4 = Shop(name='Coffee Station')

    session.add_all([shop_1, shop_2, shop_3, shop_4])
    session.commit()

    stock_1 = Stock(book=book_1, shop=shop_2, count=100)
    stock_2 = Stock(book=book_2, shop=shop_2, count=600)
    stock_3 = Stock(book=book_2, shop=shop_1, count=580)
    stock_4 = Stock(book=book_3, shop=shop_2, count=700)
    stock_5 = Stock(book=book_4, shop=shop_3, count=400)
    stock_6 = Stock(book=book_1, shop=shop_4, count=200)

    session.add_all([stock_1, stock_2, stock_3, stock_4, stock_5, stock_6])
    session.commit()

    sale_1 = Sale(price=600, date_sale='09-11-2022', stock=stock_2, count=10)
    sale_2 = Sale(price=500, date_sale='08-11-2022', stock=stock_4, count=1)
    sale_3 = Sale(price=580, date_sale='05-11-2022', stock=stock_1, count=2)
    sale_4 = Sale(price=490, date_sale='02-11-2022', stock=stock_5, count=5)
    sale_5 = Sale(price=600, date_sale='26-10-2022', stock=stock_2, count=3)
    sale_6 = Sale(price=300, date_sale='20-12-2022', stock=stock_6, count=2)

    session.add_all([sale_1, sale_2, sale_3, sale_4, sale_5, sale_6])
    session.commit()

    session.close()


def select_info(search_data):
    try:
        int(search_data)
        search_filter = Publisher.id
    except ValueError:
        search_filter = Publisher.name

    correct_data = session.query(
        Publisher.name, Book.title, Shop.name, Sale.price, Sale.date_sale
    ).join(
        Sale.stock
    ).join(
        Stock.shop
    ).join(
        Stock.book
    ).join(
        Book.publisher
    ).filter(search_filter == search_data).all()

    for c in correct_data:
        print(f'{c[0]} | {c[1]} | {c[2]} | {c[3]} | {c[4]}')


if __name__ == '__main__':
    create_insert_db()
    user_search = input('Введите id или имя автора: ')
    select_info(user_search)
