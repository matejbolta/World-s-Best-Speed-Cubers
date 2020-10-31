# Script structure:
# main(...)
#     url_to_disk(...) ok
#         url_to_content(...) ok
#         content_to_disk(...) ok
#     file_to_dict_list(...) ok
#         file_to_content(...) ok
#         content_to_blocks(...) ok
#         block_to_unified_dict(...)
#             block_to_main_dict(...)
#             block_to_competitor_dict(...)
#             block_to_competition_dict(...)
#     obj_to_json(...)
#     json_to_csv(...)
#         json_to_obj(...)
#         dicts_to_csv(...)

import csv
import datetime
import json
import os
import re
import requests
import time

# 3x3x3 bo vedno označeno kot 333, Multiple Blindfolded pa kot multi

# Konstante
data_path = 'data/'
name_html_333 = '333.html'
name_json_333 = '333.json'
name_csv_333 = '333.csv'
name_html_multi = 'multi.html'
name_json_multi = 'multi.json'
name_csv_multi = 'multi.csv'
url_wca = 'https://www.worldcubeassociation.org/'
url_333 = url_wca + f'results/rankings/333/average?show={10000}+persons'
url_multi = url_wca + f'results/rankings/333mbf/single?show={2000}+persons'


# --------------------------------------------------
# Shranjevanje html datoteke na disk
# --------------------------------------------------

# Subsidiary to url_to_disk()
def url_to_content(url):
    '''Sprejme url (niz), ter vrne vsebino pod tem url-jem kot niz'''
    # Filter za nestabilno internetno povezavo
    # (I've learned it the hard way)
    while True:
        try:
            page_content = requests.get(url) # Spletna stran object
            break
        except requests.exceptions.ConnectionError:
            print(
                f'Napaka pri povezovanju do:\n'
                f'{url}\n'
                f'Ponovni poskus čez deset sekund.'
            )
            time.sleep(10)

    if page_content.status_code == requests.codes.ok:
        return page_content.text

    # Filter za zavrnitev poizvedbe (zaradi preveč poizvedb)
    else:
        print(
            f'Napaka pri prenosu strani:\n'
            f'{url}\n'
            f'Ponovitev izvajanja čez dve minuti.'

        )
        time.sleep(120)
        return url_to_content(url)


# Subsidiary to url_to_disk()
def content_to_disk(content, directory, filename):
    '''Zapiše vsebino strani na disk pod directory/filename'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(content)
    return None


def url_to_disk(url, directory, filename):
    '''Shrani vsebino strani na povezavi url na disk pod directory/filename'''
    content = url_to_content(url)
    if content:
        content_to_disk(content, directory, filename)
        return True
    else:
        return False


# --------------------------------------------------
# Pridobivanje seznama slovarjev z vsemi podatki
# --------------------------------------------------

# TODO KOMENTAR O PRIDOBITVI PODATKOV. Čeprav večino podatkov pridobimo že z..

# Subsidiary to file_to_dict_list()
def file_to_content(directory, filename):
    '''Vrne vsebino datoteke na directory/filename'''
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as in_file:
        return in_file.read()


# Subsidiary to file_to_dict_list()
def content_to_blocks(content):
    '''Poišče posamezne ranke in vrne seznam teh rankov'''
    pattern = re.compile(
        r'<td class="pos .*?"> ' # Namesto .*? --> (tied-previous)?
        r'.*?'
        r'<!-- Extra column for .table-greedy-last-column -->',
        flags=re.DOTALL
    )
    list_of_blocks = re.findall(pattern, content)
    return list_of_blocks


# Subsidiary to block_to_unified_dict()
def block_to_main_dict(block):
    '''Vrne slovar ki vsebuje (skoraj) vse željene podatke'''
    pattern = re.compile(
        r'<td class="pos .*?"> '
        r'(?P<rank>\d+?)'
        r' </td>.*?<a href=".*?">'
        r'(?P<name>.+?)'
        r'</a> </td>.*?"result"> '
        r'(?P<result>.+?)'
        r' </td>.*?</span> '
        r'(?P<citizen_of>.+?)'
        r' </td>.*?<a href=".*?">'
        r'(?P<competition>.+?(?P<year>\d{4}))' # Grupa v grupi
        r'</a> </td>.*?-->',
        re.DOTALL
    )
    data = re.search(pattern, block)
    main_dict = data.groupdict()
    # print(block, '\n\n', main_dict)
    return main_dict


# Subsidiary to block_to_unified_dict()
def block_to_competitor_dict(block):
    '''Pridobi spletno stran tekmovalca (je ne shrani),
    ter vrne slovar z dodatnimi podatki o tekmovalcu'''
    # Htmljev ne shranjuje na disk, ker bi jih bilo skupno 2 * 10'000
    pattern_url = re.compile(
        r'<a href="/(?P<url>persons/.*?)">'
    )
    addition = re.search(pattern_url, block).group('url')
    content = url_to_content(url_wca + addition)
    pattern_comp = re.compile(
        r'WCA ID.*?</td>.*?<td>'
        r'(?P<wca_id>.*?)'
        r'</td>.*?<td>'
        r'(?P<gender>.*?)'
        r'</td>.*?<td>'
        r'(?P<attended_competitions>.*?)'
        r'</td>',
        flags=re.DOTALL
    )
    return re.search(pattern_comp, content).groupdict()


# Subsidiary to block_to_unified_dict()
def block_to_competition_dict(block):
    '''Pridobi spletno stran tekmovanja (je ne shrani),
    ter vrne slovar z dodatnimi podatki o tekmovanju'''
    # Htmljev ne shranjuje na disk, ker bi jih bilo skupno 2 * 10'000
    pattern_url = re.compile(
        r'<a href="/(?P<url>competitions/.*?)">'
    )
    addition = re.search(pattern_url, block).group('url')
    content = url_to_content(url_wca + addition)
    pattern_comp = re.compile(
        r'Competitors</dt>\n\s*?<dd>'
        r'(?P<competition_size>\d+)'
        r'</dd>'
    )
    return re.search(pattern_comp, content).groupdict()


# Subsidiary to file_to_dict_list()
def block_to_unified_dict(block):
    '''Vrne skupen slovar vseh podatkov iz bloka'''
    main_dict = block_to_main_dict(block)
    competitor_dict = block_to_competitor_dict(block)
    competition_dict = block_to_competition_dict(block)

    main_dict.update(competitor_dict)
    main_dict.update(competition_dict)

    return main_dict


def file_to_dict_list(directory, filename):
    '''Prebere datoteko ter vrne seznam slovarjev, za vsak rank svoj slovar'''
    content = file_to_content(directory, filename)
    blocks = content_to_blocks(content)
    # return [
    #     block_to_unified_dict(block) for block in blocks
    # ]

    # Tole naredi enako, plus, vmes kaže napredek:
    sez = list()
    for i, block in enumerate(blocks):
        sez.append(block_to_unified_dict(block))
        if not i % 100 and i:
            print(f'Zajetih {i} tekmovalcev')
        if not i % 500:
            print('Time:', datetime.datetime.now())
    return sez


# --------------------------------------------------
# Shranjevanje csv datoteke z vsemi podatki
# --------------------------------------------------

def obj_to_json(obj, directory, filename):
    '''Zapiše objekt na podano pot v json datoteko'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(obj, json_file, indent=2, ensure_ascii=False)


# Subsidiary to json_to_csv()
def json_to_obj(directory, filename):
    '''Vrne vsebino json datoteke pod podano potjo'''
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as json_file:
        obj = json.load(json_file)
    return obj


# Subsidiary to json_to_csv()
def dicts_to_csv(dicts, directory, filename):
    '''Zapiše seznam slovarjev na podano pot v csv datoteko'''
    path = os.path.join(directory, filename)
    fieldnames = dicts[0].keys()
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for dictionary in dicts:
            writer.writerow(dictionary)
    return None


def json_to_csv(dir_json, filename_json, dir_csv, filename_csv):
    '''Iz json datoteke na podani poti, zapiše pripadajočo csv datoteko'''
    dicts = json_to_obj(dir_json, filename_json)
    dicts_to_csv(dicts, dir_csv, filename_csv)
    return None


# --------------------------------------------------
# Glavna funkcija
# --------------------------------------------------

def main(
    redownload_333=False, reparse_333=False,
    redownload_multi=False, reparse_multi=False):
    '''Pridobi ter z vmesnimi koraki zapiše željene podatke v csv datoteke'''
    if redownload_333: # download_main_data_333
        # Na disk shrani html z 333 ranki
        # Stran zajeta dne: 2020-10-28
        url_to_disk(url_333, data_path, name_html_333)

    if reparse_333: # download_additional_data_and_reparse_333
        # Pridobi podatke iz html datoteke in dodatne podatke s spleta
        # Dodatnih html datotek ne shrani na disk (izvaja se dolgo)
        # Podatke zapiše v json in v csv datoteko
        dicts = file_to_dict_list(data_path, name_html_333)
        obj_to_json(dicts, data_path, name_json_333)
        json_to_csv(data_path, name_json_333, data_path, name_csv_333)

    if redownload_multi: # download_main_data_multi
        # Na disk shrani html z multi ranki
        # Stran zajeta dne: 2020-10-31
        url_to_disk(url_multi, data_path, name_html_multi)

    if reparse_multi: # download_additional_data_and_reparse_multi
        # Pridobi podatke iz html datoteke in dodatne podatke s spleta
        # Dodatnih html datotek ne shrani na disk (izvaja se dolgo)
        # Podatke zapiše v json in v csv datoteko
        # TODO
        pass

# Da se main() ne požene ob, denimo, importu
if __name__ == '__main__':
    main()
