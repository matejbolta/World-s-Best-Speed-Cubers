# POBIRAM:
#
# wca ranki:
# - rank
# - ime
# - rezultat
# - narodnost
# - tekmovanje
# - leto
#
# tekmovalec:
# - spol
# - št tekmovanj
# - id (leto registracije)
#
# tekmovanje:
# - število tekmovalcev
# ---------------------------------------------
#
# multi::
# wca ranki:
# - isto
#
# tekmovalec:
# - 3x3x3 avg + rank wr
# - spol, id, št tekmovanj

# vaje:
# main
#     save frontpage
#         download url to string
#         save string to file
#     ads from file
#         read file to string
#         page to ads
#         get dict from ad block
#     write ads to csv
#         write csv
#-------------------------------------------------

import datetime
import os
import re
import requests


# Konstante
url_wca = 'https://www.worldcubeassociation.org/'
url_rankings_333 = url_wca + f'results/rankings/333/average?show={10000}+persons'
path_html = 'htmls/'
name_html_333 = 'frontpage-333.html'
# name_csv_TODO = 'TODO.csv'


# --------------------------------------------------
# Shranjevanje html datoteke na disk
# --------------------------------------------------

# Subsidiary to url_to_disk()
def url_to_content(url):
    '''Sprejme url (niz), ter vrne vsebino pod tem url-jem kot niz'''
    try:
        page_content = requests.get(url) # Spletna stran object
    except requests.exceptions.ConnectionError:
        print(f'Napaka pri povezovanju do:\n{url}')
        return None

    if page_content.status_code == requests.codes.ok:
        return page_content.text
    else:
        print(f'Napaka pri prenosu strani:\n{url}')
        return None


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


# Test za en blok:
# drew_block = content_to_blocks(file_to_content(path_html, name_html_333))[8]
# [5449] --> Matej
# print(block_to_unified_dict(drew_block))


def file_to_dict_list(directory, filename):
    '''Prebere datoteko ter vrne seznam slovarjev, za vsak rank svoj slovar'''
    content = file_to_content(directory, filename)
    blocks = content_to_blocks(content)

    # To naj bi teklo med 8 (3s na blok) in 11 (4s na blok) ur,
    # če me wca vmes ne bana. Vmes bi bilo opravljenih 20 000
    # requests.get() poizvedb, ena na 1,5 oz 2 sekundi.

    # Tole naredi enako, plus, vmes kaže napredek:
    # sez = list()
    # print('Začetek:', datetime.datetime.now())
    # for i, block in enumerate(blocks):
    #     sez.append(block_to_unified_dict(block))
    #     if not i % 10:
    #         print(f'napredek: {(i + 1) / 100}%')
    # return sez
    return [
        block_to_unified_dict(block) for block in blocks
    ]


# --------------------------------------------------
# Shranjevanje csv datoteke z vsemi podatki
# --------------------------------------------------

# Subsidiary to dicts_to_csv()
def neki_kar_zapisuje_vrstice_v_csv_al_kako_ze(x):
    pass


def dicts_to_csv(dicts, directory, filename):
    
    
    
    
    pass


# TODO najprej naredi funkcijo ki ti bo sez slovarjev zapisala v json,
# TODO da bo lokalno shranjeno. in jo implementiraj.















def main(main_data=False, additional_data=False):
    '''
    '''
    if main_data:
        # Na disk shrani html z 333 ranki
        # Stran zajeta dne: 2020-10-28
        url_to_disk(url_rankings_333, path_html, name_html_333)
    
    if additional_data:
        # Pridobi podatke iz datoteke in dodatne podatke s spleta
        # Dodatnih datotek ne shrani na disk, in teče zelo dolgo
        dicts = file_to_dict_list(path_html, name_html_333)


# Da se main() ne požene ob, denimo, importu
if __name__ == '__main__':
    main()
