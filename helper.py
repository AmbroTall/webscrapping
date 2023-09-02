# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 15:14:02 2022

@author: Asad Mehmood (asadmahmood16@hotmail.com)
"""

import logging
from datetime import datetime
import string
import usaddress
import re
import random

global dev
dev = True

TABLE_Logger = "Logger"
PUNCTUATION = string.punctuation
TRANSLATOR = str.maketrans('', '', PUNCTUATION)

US_STREET_KEYS = ['AddressNumberPrefix', 'AddressNumberSuffix', 'AddressNumber',
                  'BuildingName', 'StreetNamePreDirectional', 'StreetNamePreModifier',
                  'StreetNamePreType', 'StreetName', 'StreetNamePostDirectional',
                  'StreetNamePostModifier', 'StreetNamePostType']
US_CITY_KEYS = ['PlaceName']
REQUIRE_KEYS = US_STREET_KEYS + US_CITY_KEYS + ['StateName', 'ZipCode']

def time_elapsed_str(start, end):
    elapse = end - start
    hours, rem = divmod(elapse, 3600)
    minutes, seconds = divmod(rem, 60)
    strings = "{:0>2}:{:0>2}:{:0>2}".format(int(hours), int(minutes), int(seconds))
    if elapse < 1:
        mili = str(round(elapse, 3))
        miliseconds = mili[1:]
        strings += miliseconds
    return strings

def print_log(text, error=False):
    if dev:
        print(text)
    if error:
        logging.error(text.strip())
    else:
        logging.info(text.strip())

def RepresentsInt(s):
    isInt = True
    try:
        int(s)
    except ValueError:
        isInt = False
    return isInt

def wait_time():
    interval = random.randint(2, 5) if dev else random.randint(10, 15)
    return interval

def check_first_word_is_number(string):
    first_word = string.split()[0]
    return first_word.isnumeric()
def parse_address(address):
    print()
    zip_code = re.findall('\d{4,5}', address)
    address = str(address.split('.')[0]).strip()
    if len(zip_code) > 0 and check_first_word_is_number(address) != True:
        zip_code = zip_code[0]
    elif len(zip_code) > 0 and check_first_word_is_number(address) == True:
        zip_code = zip_code[1]

    if len(address.split(',')) > 3:
        new_add = address.split(',')[:3]
        zip_part = re.findall('\d{4,5}', " ".join(new_add[1:]))
        sec_elm = new_add[1]
        num_center = len(sec_elm.split())
        if not RepresentsInt(sec_elm) and bool(zip_part) and num_center <= 3:
            address = ",".join(new_add).strip()

    if bool(address) and any([address.startswith(p) for p in PUNCTUATION]):
        address = address[1:].strip()

    street = address.split(',')[0].strip() if len(address.split(',')) > 0 else ''
    city = address.split(',')[1].strip() if len(address.split(',')) > 1 else ''

    street = street.replace("'", "").strip().title()
    city = city.strip().title()

    # street = street.replace("'", "")
    if any(street.lower().endswith(i) for i in [" rd", " st", " ave", " dr."]):
        if street.lower().endswith(" rd"):
            street = street[:-2] + "Road"
        if street.lower().endswith(" st"):
            street = street[:-2] + "Street"
        if street.lower().endswith(" ave"):
            street = street[:-3] + "Avenue"
        if street.lower().endswith(" dr."):
            street = street[:-3] + "Drive"

    info = {
        'Street': street,
        'City': city,
        'Zip_Code': zip_code if bool(zip_code) else '',
        'Address': str(bool(address)),
    }
    return info

def gets_usaddress(text):
    ans = usaddress.parse(text)
    addr = list()
    for val in ans:
        dict_val, dict_key = val
        tupe = (dict_key, dict_val)
        addr.append(tupe)
    return addr

def parse_usaddress(address):
    dump = dict()
    scrape_info = list()
    for val in address.values():
        str_street = list()
        str_city = list()
        ZipCode = None
        for ind, i in enumerate(val.copy()):
            k, v = i
            if k in US_STREET_KEYS:
                str_street.append(v)
            if k in US_CITY_KEYS:
                str_city.append(v)

            if 'ZipCode' == k:
                ZipCode = v.strip()
                if any(ZipCode.endswith(s) for s in PUNCTUATION):
                    ZipCode = ZipCode[:-1].strip()
                for s in PUNCTUATION:
                    if s in ZipCode:
                        ZipCode = ZipCode.split(s)[0].strip()
                        break
            try:
                next_key = val[ind + 1][0]
                if next_key not in REQUIRE_KEYS:
                    break
            except IndexError:
                break

        info = dict()
        if bool(str_street) and bool(str_city):
            info_street = " ".join(str_street)
            info_city = " ".join(str_city)

            info_street = info_street.replace("'", "")
            while any(info_street.endswith(s) for s in PUNCTUATION):
                info_street = info_street[:-1].strip()

            while any(info_city.endswith(s) for s in PUNCTUATION):
                info_city = info_city[:-1].strip()

            us_street = info_street.strip().title()
            us_city = info_city.strip().title()

            if us_street.strip().lower().endswith(" rd"):
                us_street = us_street[:-2] + "Road"
            if us_street.strip().lower().endswith(" st"):
                us_street = us_street[:-2] + "Street"
            if us_street.strip().lower().endswith(" ave"):
                us_street = us_street[:-3] + "Avenue"
            if us_street.strip().lower().endswith(" dr"):
                us_street = us_street[:-2] + "Drive"

            info.update({'Street': us_street, 'City': us_city, 'Zip_Code': ''})
            if bool(ZipCode):
                info['Zip_Code'] = ZipCode

        if bool(info):
            scrape_info.append(info)
    if bool(scrape_info):
        info_list = [dict(t) for t in {tuple(d.items()) for d in scrape_info}]
        if len(info_list) > 1:
            try:
                for i, vault in enumerate(info_list.copy()):
                    if not bool(vault['Zip_Code']):
                        del info_list[i]
            except IndexError:
                info_list = scrape_info[:1].copy()

        if len(info_list) > 1:
            info_list = scrape_info[:1].copy()
        dump = info_list.pop()
        dump.update({'Address': str(bool(dump['Street']))})
    return dump

def filter_notice(notice):
    address = ''
    search_strings = ['property is more commonly known as', 'said property being known as:',
        'said property is known as', 'property known a/s', 'known as located at', 'known as address', ' k/a',
        'located at', 'property address:', 'following parcels', 'commonly known as',
        'property located at', 'street address:', 'property location:', ':property location:']
    content = notice.lower().strip()
    address_list = dict()
    us_addr_list = dict()
    for find_str in search_strings:
        if find_str in content:
            address = content.split(find_str)[1].strip()
            nr_parsed = parse_address(address)
            us_parsed = gets_usaddress(address)

            address_list[find_str] = nr_parsed
            us_addr_list[find_str] = us_parsed

    parsed_us = parse_usaddress(us_addr_list)

    parser_nr = dict()
    parse = False
    num_addresses = len(address_list)
    vals = list(address_list.values())
    if num_addresses == 1:
        parse = True
    elif num_addresses > 1:
        if not bool(parsed_us):
            parse = True
            vals = [dict(t) for t in {tuple(d.items()) for d in vals}]

    if parse:
        dump = vals.pop()
        if dump['City'] == str(datetime.today().year):
            dump['City'] = ''

        street = dump['Street']
        city = dump['City']

        if bool(street) and bool(city):
            zip_code = dump['Zip_Code']
            if zip_code == str(datetime.today().year) or street.startswith(zip_code):
                dump['Zip_Code'] = ''
                parser_nr = dump.copy()

            if len(city.split()) > 3:
                parser_nr = dict()

            if len(street.split()) > 8:
                parser_nr = dict()

    return parsed_us, parser_nr

def parse_Address(Notice, Id, State, Publisher):
    address_map = dict()
    address_us, address_nr = filter_notice(Notice)
    Notice = Notice.replace('\'', '').replace('"', '').strip()

    if bool(address_us):
        address_map.update(address_us)
    elif bool(address_nr):
        address_map.update(address_nr)
    else:
        address_map = {
        'Street': '',
        'City': '',
        'Zip_Code': '',
        'Address': str(False)
        }

    info = {
        'State': State,
        'Id': Id,
        'Notice': Notice,
        'Publisher': Publisher
    }
    address_map.update(info)
    return address_map

def start_logger(debug, limited, database, source):
    r_starts = 1
    r_finish = limited
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    where_clause = "Data_Source = '{}'".format(source)
    stmt = "SELECT Next_Starts,Next_Finish FROM {} WHERE {}".format(TABLE_Logger, where_clause)
    try:
        num = database.show_data(TABLE_Logger, stmt)
    except Exception as e:
        error_str = "{}: {}".format(str(type(e).__name__), str(e))
        print_log(error_str, True)
        print_log("ISSUE: in db.show_data", True)

    if num:
        rows = database.show_data(TABLE_Logger, stmt)
        r_starts, r_finish = list(rows).pop()
        # r_starts, r_finish = row['Next_Starts'], row['Next_Finish']
        r_starts = 1 if not bool(r_starts) else r_starts
        r_finish = limited if not bool(r_finish) else r_finish
    else:
        info = dict(Data_Source=source, Run_Time=date_now,Next_Starts=str(r_starts),Next_Finish=str(r_finish))
        columns_str = "`, `".join(info.keys())
        values = "', '".join(info.values())
        stmt = "INSERT INTO `{}` (`{}`) VALUES ('{}');".format(TABLE_Logger, columns_str, values)
        if not debug:
            try:
                database.run_query(stmt)
            except Exception as e:
                error_str = "{}: {}".format(str(type(e).__name__), str(e))
                error_sql = "SQL: '{}'".format(stmt)
                print_log(error_str, True)
                print_log(error_sql, True)
    return date_now, r_starts, r_finish

def calculate_run(urls, total_return, limited, r_starts, r_finish, full_data):
    all_pages = urls.copy()
    if total_return <= limited:
        if r_starts > 1:
            all_pages = urls[r_starts:].copy()
            if full_data and len(all_pages) <= limited and total_return <= limited:
                all_pages = urls[-limited:].copy()

        if r_starts <= total_return:
            r_starts = total_return
    else:
        if r_starts == 1:
            all_pages = urls[:limited].copy()
            r_starts = limited
        else:
            if full_data:
                all_pages = urls[r_starts:r_finish].copy()
            else:
                all_pages = urls[:limited].copy()
            r_starts += len(all_pages)

    if bool(all_pages):
        r_finish = r_starts + limited
    return all_pages, r_starts, r_finish

def update_logger(debug, database, source, date_now, limited, r_starts, r_finish, total_return, urls, full=True):
    set_equal = list()
    set_equal.append("Run_Time = '{}'".format(date_now))
    set_equal.append("Starts = {}".format(r_starts))
    set_equal.append("Finish = {}".format(r_finish))
    set_equal.append("Total_Records = {}".format(total_return))

    all_pages, r_starts, r_finish = calculate_run(urls, total_return, limited, r_starts, r_finish, full)

    n_records = len(all_pages)
    set_equal.append("Scrapped = {}".format(n_records))
    set_equal.append("Next_Starts = {}".format(r_starts))
    set_equal.append("Next_Finish = {}".format(r_finish))

    equals = ", ".join(set_equal)
    where_clause = "Data_Source = '{}'".format(source)
    stmt = """UPDATE `{}` SET {} WHERE {}""".format(TABLE_Logger, equals, where_clause)
    if not debug:
        try:
            database.run_query(stmt)
        except Exception as e:
            error_str = "{}: {}".format(str(type(e).__name__), str(e))
            error_sql = "SQL: '{}'".format(stmt)
            print_log(error_str, True)
            print_log(error_sql, True)
    return all_pages

if __name__ == "__main__":
    check = False
    total_records = 533
    limit = 200
    n_begins = 400
    n_finish = 600
    list_url = list(range(1, total_records + 1))
    if not check:
        list_url = list(range(1, limit + 1))
        if total_records > n_begins and total_records < n_finish:
            list_url = list(range(1, total_records - n_begins + 1))

    list_url, n_begins, n_finish = calculate_run(list_url, total_records, limit, n_begins, n_finish, check)
