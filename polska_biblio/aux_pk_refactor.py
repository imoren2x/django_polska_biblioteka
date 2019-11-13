#!/usr/bin/python
# -*- coding: latin-1 -*-

import copy
import yaml
import sys
import pdb
import logging


KATALOG_FIELDS = ['ISBN', 'Title', 'Name', 'Surname', 'Publisher', 'City', ]  # 'Year', ]
DB_FIELDS = ['ISBN', 'title', 'author_name', 'author_surname', 'publisher_name', 'publisher_city', ]  # 'year_published', ]



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


# from aux_pk_refactor import KATALOG_FIELDS, DB_FIELDS, read_yaml, write_yaml, compare, main
# katalog_strip = read_yaml('Katalog_2019_10_20_1_4775_strip.yaml')
# dump_strip = read_yaml('dump_strip.yaml')
# compare(dump_strip[12], katalog_strip[1])
DEBUG = False

def main(katalog, db_yaml):
    # norm_db_yaml = db_yaml[12:3137+1]
    # gen_match_list = list()
    output_db_yaml = list()
    global DEBUG

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
