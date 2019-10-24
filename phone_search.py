#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# RIP http://www.roum.ru/bases/people.html
# I loved you! <3

import sys
import urllib.parse

COUNTRY_CODES = ['+7', '8'] #IC

# INFO: Maximim words in Google request is 32 (including OR and also devided by - symbol)
# So we can search only 16 phones at once # 16 phones + 15 OR-s + 1 free word 

# TODO: Fix bugs with 4 digit city codes. For example - Bryansk (+7 48-32) 54-32-10
# You can use CC tag in format string to replace it with all country codes. 
# EX: 'CC{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}' will produce +79876543210 and 89876543210

PHONE_FORMATS_WITH_10_DIGITS = [
        '{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}',
        '({0}{1}{2}) {3}{4}{5} {6}{7} {8}{9}',
        '({0}{1}{2}) {3}{4}{5}-{6}{7}-{8}{9}',
        '({0}{1}{2}) {3}{4}{5}{6}{7}{8}{9}',
        '({0}{1}{2}){3}{4}{5} {6}{7} {8}{9}',
        '({0}{1}{2}){3}{4}{5}-{6}{7}-{8}{9}', # (987)654-32-10
        '({0}{1}{2}){3}{4}{5}{6}{7}{8}{9}',
        '{0}{1}{2} {3}{4}{5} {6}{7} {8}{9}',
        '{0}{1}{2} {3}{4}{5}-{6}{7}-{8}{9}',
        '{0}{1}{2} {3}{4}{5}{6}{7}{8}{9}'
    ]

def extract_digits(dirty_phone):
    digits = ['1','2','3','4','5','6','7','8','9','0']
    return(''.join([n for n in dirty_phone if n in digits]))

def remove_codes(phone_with_codes):
    res = phone_with_codes
    for c in COUNTRY_CODES: # Bug when, 4ex, country code is 89 and internal code is 8
        c = extract_digits(c)
        if phone_with_codes.find(c) == 0:
            res = phone_with_codes[len(c):]
    return(res)

def mutate(phone):
    res = []
    for f in PHONE_FORMATS_WITH_10_DIGITS:
        if 'CC' in f:
            for cc in COUNTRY_CODES:
                res.append(f.replace('CC', cc).format(*phone))
                continue
        else:
            res.append(f.format(*phone))
    return(res)

def generate_google_link(phones):
    google_format = 'https://www.google.com/search?q=%s'
    query = '"' + '" OR "'.join([p for p in phones]) + '"'  
    link = google_format % urllib.parse.quote_plus(query)
    return(link)

def generate_yandex_link(phones):
    yandex_format = 'https://yandex.ru/search/?text=%s'
    query = '"' + '" OR "'.join([p for p in phones]) + '"'  
    link = yandex_format % urllib.parse.quote_plus(query)
    return(link)

# Rambler uses Yandex search engine
# Bing is very bad at searching phones, because it doesn't have double quotes, so terms are separated by dashes and parenthesises

if len(sys.argv) == 2:
    req_phone = sys.argv[1].strip()
    clear_phone = remove_codes(extract_digits(req_phone))
    if len(clear_phone) != 10:
        print('Bad input. Only 10-digit phones are supporded. Contribute!')
    mutated_phones = mutate(clear_phone)
    print('\nGoogle:\n\t' + generate_google_link(mutated_phones))
    print('\nYandex:\n\t' + generate_yandex_link(mutated_phones))

else:
    print('Usage:\n\tphone_search.py +79876543210\n\tphone_search.py 987-654-32-10\n\tphone_search.py "8(987)654-3210"')

# Phone formats: 
# https://www.artlebedev.ru/kovodstvo/sections/91/
# https://besisland.livejournal.com/445281.html
