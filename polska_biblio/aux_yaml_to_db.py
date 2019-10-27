#!/usr/bin/python
# -*- coding: latin-1 -*-

import yaml
import sys

from biblio.models import Book, Borrowing, LibraryUser, CATEGORY_CHOICES

import pdb

INPUT_FILE_STR = '../Katalog_2019_10_20_1_4775.yaml'
# INPUT_FILE_STR = '../Katalog_simple.yaml'
# INPUT_FILE_STR = '../Katalog_2019_10_20_2_100.yaml'
ROWS_INI = 0
ROWS_END = 20

def norm_str(value):
    return '' if value is None else value.strip()

def norm_int(value):
    if value is None:
        print('Integer is None')
        return 1

    try:
        if isinstance(int(value), int) is True:
            return int(value)
    except Exception as e:
        print(str(e).encode('utf-8'))
        print('Integer: %s' % value.encode('utf-8'))
        pdb.set_trace()
        pass

def classify_cat(cat_str):
    if cat_str is None:
        print('Category is None')
        return 'RZ'

    norm_cat = cat_str.strip().split('/', 1)[0].upper()  # primer elemento y mayuscula
    if norm_cat in dict(CATEGORY_CHOICES).keys():
        return norm_cat
    elif cat_str == 'h':
        return 'HS'
    else:
        print('Category: %s' % cat_str.encode('utf-8'))
        return 'RZ'

def classify_status(status_str):
    if isinstance(status_str, str) is True:
        return 'AVAILABLE' if 'jest' in status_str.strip() else 'NONAVAILABLE'
    else:
        print('Status: %s' % status_str)
        return 'NONAVAILABLE'

def norm_uni(value):
    # v = norm_str(value)
    return value.encode('utf-8') if isinstance(value, str) else value

def print_book(book):
    keys = ['title', 'author_name', 'author_surname', 'publisher_name', 'publisher_city', 'year_published',
            'ISBN', 'category', 'status', 'location', 'description', 'notes', ]
    for key in keys:
        print( "%-15s: %s" % ( key, norm_uni(getattr(book, key))))

def read_yaml(input_file_str):

    with open(input_file_str, 'r') as file_desc:
        yaml_data = yaml.load(file_desc, Loader=yaml.Loader)

    return yaml_data


def main(yaml_data):
    # pdb.set_trace()
    # global INPUT_FILE_STR, ROWS_INI, ROWS_END

    # with open(INPUT_FILE_STR, 'r') as file_desc:
    #     yaml_data = yaml.load(file_desc, Loader=yaml.Loader)
    # yaml_data = read_yaml(INPUT_FILE_STR)
    # pdb.set_trace()

    # yaml_entries = yaml_data[ROWS_INI:(ROWS_END+1)]

    # for yaml_book in yaml_entries:
    # for index in range(0, len(yaml_entries)):
    save = False
    for index in range(0, len(yaml_data)):
        # yaml_book = yaml_entries[index]
        yaml_book = yaml_data[index]

        try:
            # print("Iteration: %s" % (index+ROWS_INI))
            print("Iteration: %s" % yaml_book['Number'])
            title          = yaml_book['Title']
            author_name    = yaml_book['Name']
            author_surname = yaml_book['Surname']
            publisher_name = yaml_book['Publisher']
            publisher_city = yaml_book['City']
            year_published = norm_int(yaml_book['Year'])

            ISBN           = yaml_book['ISBN']
            category       = classify_cat(yaml_book['Category'])
            status         = classify_status(yaml_book['Available'])
            location       = norm_str(yaml_book['Location'])
            quantity       = norm_int(yaml_book['Amount'])

            description    = yaml_book['Description']
            notes          = yaml_book['Anotations']

            for item in range(1, quantity+1):
                #'''
                book = Book(
                    title=title,
                    author_name=author_name,
                    author_surname=author_surname,
                    publisher_name=publisher_name, 
                    publisher_city=publisher_city,
                    year_published=year_published,
                    #ISBN=ISBN,
                    category=category,
                    status=status,
                    location=location,
                    #description=description,
                    #notes=notes,
                    )
                #'''
                if ISBN is not None:
                    book.ISBN = ISBN
                if description is not None:
                    book.description = description
                if notes is not None:
                    book.notes = notes

                # save = True

                print_book(book)

                pdb.set_trace()

                if save is True:
                    book.save()

        except Exception as e:
            print(str(e).encode('utf-8'))
            pdb.set_trace()
            pass


# def process_yaml_book(yaml_book):
#     #
#     book_args = yaml_book.copy()

#     book_args['title'] = yaml_book['Title'].strip()
#     book_args['author_name'] = yaml_book['Name'].stri
#     author_surname = yaml_book['Surname']
#     publisher_name = yaml_book['Publisher']
#     publisher_city = yaml_book['City']
#     year_published = yaml_book['Year']

#     ISBN           = yaml_book['ISBN']
#     category       = classify_cat(yaml_book['Category'])
#     status         = classify_status(yaml_book['Available'])
#     location       = norm_str(yaml_book['Location'])
#     quantity       = norm_int(yaml_book['Amount'])

#     description    = yaml_book['Description']
#     notes          = yaml_book['Anotations']


# def run_yaml(yaml_data):

#     for index in range(0, len(yaml_data)):
#         #
#         yaml_book = yaml_data[index]
#         #
#         try:
#             print("Iteration: %d / %s" % (index, yaml_book['Number']))
#             book_args = process_yaml_book(yaml_book)

#             for book_no in range(1, book_args.get('quantity') + 1):
#                 print("Book: %d" % book_no)
#                 process_book(book_args)

#         except Exception as e:
#             print(str(e).encode('utf-8'))
#             pdb.set_trace()
#             pass


if __name__ == "__main__":
    sys.exit(main())
