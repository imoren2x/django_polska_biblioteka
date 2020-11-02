#!/usr/bin/python

import copy
import yaml
import sys
import pdb
import logging
import openpyxl

from biblio.models import Book


KATALOG_FIELDS = ['ISBN', 'Title', 'Name', 'Surname', 'Publisher', 'City', ]  # 'Year', ]
DB_FIELDS = ['ISBN', 'title', 'author_name', 'author_surname', 'publisher_name', 'publisher_city', ]  # 'year_published', ]
ROW_KEYS_PL = ['Tytuł', 'Nazwisko', 'Imię', 'Wydawnictwo', 'Miasto', 'Rok', 'Kategoria', 'ISBN', 'Wypożyczenia', 'Dostępność', 'Litera', 'Biała kartka', 'Kolorowa kartkaRodzaj', 'Ilość', 'Oznakowanie', 'Adnotacja', 'Opis', ]
DB_ROW_KEYS = ['id', 'title', 'author_surname', 'author_name', 'publisher_name', 'publisher_city', 'year_published', 'category', 'ISBN', 'status', 'Available', 'location', 'White card', 'Book card', 'Kind', 'Amount', 'Marking', 'notes', 'description', ]

TRIVIAL_FIELDS = ['id', 'title', 'author_name', 'author_surname',
 'publisher_name', 'publisher_city', 'year_published', 'ISBN', 'location',
 'notes', 'description', ]

CATEGORY_DICT = {
    u'pw/ndż': 'PW',
    'rż/fz': 'RZ',
    'rż/psych.': 'RZ',
    'pw/kz': 'PW',
    'dz/mł/lektura': 'DZ',
    'pz/lek.': 'PZ',
    'bg': 'BG',
    'rż/rpż': 'RZ',
    'rż': 'RZ',
    'rż/prż': 'RZ',
    'pw/kp/lek.': 'PW',
    'h': 'HS',
    'dz/mł': 'DZ',
    'dz/m': 'DZ',
    'pw': 'PW',
    'dz/ml': 'DZ',
    'pz/kz': 'PZ',
    'pz': 'PZ',
    'pw/pz': 'PZ',
    'rz': 'RZ',
    'pw/ft': 'PW',
    'pw/kp': 'PW',
    'pw/lek.': 'PW',
    'rż/fel.': 'RZ',
    'pw/kr': 'PW',
    'dz/mł/lek.': 'DZ'
}


def read_excel(input_file_str):
    workbook = openpyxl.load_workbook(input_file_str)
    sheet = workbook.active

    excel_yaml = list()
    for row_index in range(2, sheet.max_row):
        row_excel = sheet[row_index]
        raw_row = [cell.value for cell in row_excel]

        row_dict = dict(zip(DB_ROW_KEYS, raw_row))
        if row_dict['id'] is None:
            return excel_yaml

        if isinstance(row_dict['id'], float):
            row_dict['id'] = int(row_dict['id'])
        if isinstance(row_dict['year_published'], float):
            row_dict['year_published'] = int(row_dict['year_published'])
        if isinstance(row_dict['Amount'], float):
            row_dict['Amount'] = int(row_dict['Amount'])

        for key, value in row_dict.items():
            if isinstance(value, str) and value != value.strip():
                row_dict[key] = value.strip()
            # if key in STR_FIELDS and value is None:
                # row_dict[key] = ''

        excel_yaml.append(row_dict)

    return excel_yaml


def read_yaml(input_file_str):
    with open(input_file_str, 'r') as file_desc:
        yaml_data = yaml.load(file_desc, Loader=yaml.Loader)
    return yaml_data


def write_yaml(yaml_data, output_file_str):
    with open(output_file_str, 'w') as file_desc:
        yaml.dump(yaml_data, file_desc, indent=4)


def __norm_katalog_book(katalog_book):

    output = list()
    global KATALOG_FIELDS

    for katalog_field in KATALOG_FIELDS:
        if (katalog_book[katalog_field] is None) or (katalog_book[katalog_field] == ''):
            output.append(None)
        else:
            output.append(katalog_book[katalog_field])

    return output


def __norm_db_book(db_book):

    output = list()
    global DB_FIELDS

    fields = db_book['fields']
    for db_field in DB_FIELDS:
        if (fields[db_field] is None) or (fields[db_field] == ''):
            output.append(None)
        else:
            output.append(fields[db_field])

    return output


def compare(db_book, katalog_book):

    norm_db_book = __norm_db_book(db_book)
    norm_katalog_book = __norm_katalog_book(katalog_book)

    result = None
    for db_field, katalog_field in zip(norm_db_book, norm_katalog_book):
        if (db_field is None) or (katalog_field is None):
            continue
        elif result is None:
            result = (db_field==katalog_field)
        else:
            result = result and (db_field==katalog_field)

    return bool(result)


def __change_pk(db_book, new_pk):
    book_fields = db_book['fields']

    db_book['pk'] = int(new_pk)

    return db_book


def _convert_fields(entry):
    output = {}
    for field in TRIVIAL_FIELDS:
        output[field] = entry[field]

    # category
    category = entry['category']
    if category in CATEGORY_DICT.keys():
        output['category'] = CATEGORY_DICT[entry['category']]
    else:
        output['category'] = entry['category']

    # status
    status = entry['status']
    if status == '' or (status is None):
        output['status'] = 'AVAILABLE'
    elif 'przez' in status:
        output['status'] = 'BORROWED'
    else:
        output['status'] = 'UNKNOWN'

    return output

def _set_book(book_args):

    book = Book(
        id=book_args['id'],
        title=book_args['title'],
        author_name=book_args['author_name'] or '',
        author_surname=book_args['author_surname'],
        publisher_name=book_args['publisher_name'] or '',
        publisher_city=book_args['publisher_city'],
        year_published=book_args['year_published'],
        #ISBN=ISBN,
        category=book_args['category'],
        status=book_args['status'],
        location=book_args['location'],
        #description=description,
        #notes=notes,
        )
    #'''
    if book_args['ISBN'] is not None:
        book.ISBN = book_args['ISBN']
    if book_args['description'] is not None:
        book.description = book_args['description']
    if book_args['notes'] is not None:
        book.notes = book_args['notes']

    return book


def save_excel_yaml_to_db(excel_yaml):

    for entry in excel_yaml:
        try:
            book_args = _convert_fields(entry)
            # book = Book(**book_args)
            book = _set_book(book_args)

            book.save()
        except Exception as e:
            print("Book %s, %s: %s" % (entry['id'], entry['title'], str(e)))
            pdb.set_trace()


# from aux_pk_refactor import KATALOG_FIELDS, DB_FIELDS, read_yaml, write_yaml, compare, main
# katalog_strip = read_yaml('Katalog_2019_10_20_1_4775_strip.yaml')
# dump_strip = read_yaml('dump_strip.yaml')
# compare(dump_strip[12], katalog_strip[1])
DEBUG = False

def compare_lists(katalog, db_yaml):
    # norm_db_yaml = db_yaml[12:3137+1]
    # gen_match_list = list()
    output_db_yaml = list()

    same_pk_number = 0
    diff_pk_number = 0
    more_than_one = 0
    not_found = 0
    null_pk = 0
    total = 0


    for db_book in db_yaml:
        if db_book['model'] != 'biblio.book':
            output_db_yaml.append(db_book)
            continue

        # match_list = list()
        # for katalog_book in katalog:
        #     if compare(db_book, katalog_book) is True:
        #         match_list.append((db_book['pk'], katalog_book['Number']))

        match_list = [(db_book['pk'], katalog_book['Number']) for katalog_book in katalog if (compare(db_book, katalog_book) is True)]

        if len(match_list) > 1:
            print("MORE THAN ONE: %s" % match_list)
            more_than_one += 1
            # pdb.set_trace()
            # pass
            # continue

        elif len(match_list) == 0:
            print("NOT FOUND: %d" % (db_book['pk']))
            not_found += 1
            # pdb.set_trace()
            # pass
            # continue

        else:
            # gen_match_list.extend(match_list)

            new_pk = match_list.pop()[1]
            if new_pk is None:
                print("NULL NEW PK: pk %d" % db_book['pk'])
                null_pk += 1
                # pdb.set_trace()
                # pass
                # continue

            elif db_book.get('pk') == new_pk:
                print("SAME pk: %d" % db_book.get('pk'))
                same_pk_number += 1
                output_db_yaml.append(db_book)
                # pdb.set_trace()
                # pass

            else:
                diff_pk_number += 1
                print("%s -> %s" % (db_book.get('pk'), new_pk))
                new_db_book = __change_pk(db_book, new_pk)
                #
                output_db_yaml.append(new_db_book)
                # pdb.set_trace()
                # pass

        total += 1

        if DEBUG is True:
            pdb.set_trace()
            pass


    print("%-15s: %d" % ('same_pk_number', same_pk_number))
    print("%-15s: %d" % ('diff_pk_number', diff_pk_number))
    print("%-15s: %d" % ('more_than_one', more_than_one))
    print("%-15s: %d" % ('not_found', not_found))
    print("%-15s: %d" % ('null_pk', null_pk))
    print("%-15s: %d" % ('total', total))

    return output_db_yaml


if __name__ == "__main__":
    """
    """
    sys.exit(main())
