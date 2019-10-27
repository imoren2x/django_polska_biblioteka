
from biblio.models import Book
from time import sleep


def main():
    book_to_change = False
    for book in Book.objects.all().order_by('pk'):
        print("Book %d: %s" % (book.pk, str(book).encode('utf-8')))

        if book.title != book.title.strip():
            book_to_change = True
            book.title = book.title.strip()
            print("  Title: '%s' corrected" % book.title.encode('utf-8'))
        if book.author_name != book.author_name.strip():
            book_to_change = True
            book.author_name = book.author_name.strip()
            print("  Author name: '%s' corrected" % book.author_name.encode('utf-8'))
        if book.author_surname != book.author_surname.strip():
            book_to_change = True
            book.author_surname = book.author_surname.strip()
            print("  Author surname: '%s' corrected" % book.author_surname.encode('utf-8'))
        if book.publisher_name != book.publisher_name.strip():
            book_to_change = True
            book.publisher_name = book.publisher_name.strip()
            print("  Publisher: '%s' corrected" % book.publisher_name.encode('utf-8'))
        if book.publisher_city != book.publisher_city.strip():
            book_to_change = True
            book.publisher_city = book.publisher_city.strip()
            print("  Publisher city: '%s' corrected" % book.publisher_city.encode('utf-8'))
        if book.ISBN != book.ISBN.strip():
            book_to_change = True
            book.ISBN = book.ISBN.strip()
            print("  ISBN: '%s' corrected" % book.ISBN.encode('utf-8'))
        if book.location != book.location.strip():
            book_to_change = True
            book.location = book.location.strip()
            print("  Location: '%s' corrected" % book.location.encode('utf-8'))
        if book.description != book.description.strip():
            book_to_change = True
            book.description = book.description.strip()
            print("  Description: '%s' corrected" % book.description.encode('utf-8'))
        if book.notes != book.notes.strip():
            book_to_change = True
            book.notes = book.notes.strip()
            print("  Notes: '%s' corrected" % book.notes.encode('utf-8'))

        if book_to_change is True:
            book.save()
            sleep(2.0)
            book_to_change = False

        print("------")

