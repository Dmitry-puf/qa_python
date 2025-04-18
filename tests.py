import pytest

from main import BooksCollector
from qa_python.config import *


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        collector = BooksCollector()
        return collector

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self, collector):
        # создаем экземпляр (объект) класса BooksCollector в фикстуре

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    @pytest.mark.parametrize('book, genre, expect',
                             [('Лунный свет', 'Фантастика', 'Фантастика'),
                              ('Песни мертвецов', 'Блокбастер', ''),
                              ('Стайка', None, '')])
    def test_set_book_genre(self, collector, book, genre, expect):
        collector.add_new_book(book)
        collector.set_book_genre(book, genre)
        new_genre = collector.get_book_genre(book)
        assert new_genre == expect


    @pytest.mark.parametrize('book, genre, expect',
                             [('Лунный свет', 'Фантастика', 'Фантастика'),
                              ('Двойная жизнь', None, '')])
    def test_get_book_genre(self, collector, book, genre, expect):
        collector.add_new_book(book)
        collector.set_book_genre(book, genre)
        new_genre = collector.get_book_genre(book)
        assert new_genre == expect


    @pytest.mark.parametrize('genre, expect_len', [('Комедии', 2), ('Блокбастер', 0), (None, 0), ('', 0)])
    def test_get_books_with_specific_genre(self, collector, genre, expect_len):
        for books, genres in BOOK_GENRE.items():
            collector.add_new_book(books)
            collector.set_book_genre(books, genres)
        assert len(collector.get_books_with_specific_genre(genre)) == expect_len


    @pytest.mark.parametrize('genre, books_genre', [(['Комедии', 'Мультфильмы'], BOOK_GENRE)])
    def test_get_books_genre(self, collector, genre, books_genre):
        for books, genres in books_genre.items():
            collector.add_new_book(books)
            collector.set_book_genre(books, genres)
        assert genre[0] in collector.get_books_genre().values() and genre[1] in collector.get_books_genre().values()


    @pytest.mark.parametrize('adult_genre, books_genre', [(BOOK_ADULT, BOOK_GENRE), (BOOK_ADULT, BOOK_ADULT)])
    def test_get_books_for_children(self, collector, adult_genre, books_genre):
        for books, genres in books_genre.items():
            collector.add_new_book(books)
            collector.set_book_genre(books, genres)
        self.children_books = collector.get_books_for_children()
        self.adult_genre = list(adult_genre.values())
        assert books_genre.get(self.adult_genre[0]) not in self.children_books and books_genre.get(
            self.adult_genre[1]) not in self.children_books


    @pytest.mark.parametrize('book_name, genre', [(BOOK_NAME, 'Комедии')])
    def test_add_book_in_favorites(self, collector, book_name, genre):
        for book in book_name:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)
        collector.add_book_in_favorites(book_name[-1])
        assert collector.get_list_of_favorites_books()[0] == book_name[-1]


    @pytest.mark.parametrize('book_name, genre', [(BOOK_NAME, 'Комедии')])
    def test_delete_book_from_favorites(self, collector, book_name, genre):
        for book in book_name:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)
            collector.add_book_in_favorites(book)
        collector.delete_book_from_favorites(book_name[1])
        assert book_name[1] not in collector.get_list_of_favorites_books()


    @pytest.mark.parametrize('book_name, genre', [(BOOK_NAME, 'Комедии')])
    def test_get_list_of_favorites_books(self, collector, book_name, genre):
        for book in book_name:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)
            collector.add_book_in_favorites(book)
        assert len(collector.get_list_of_favorites_books()) == len(book_name)
