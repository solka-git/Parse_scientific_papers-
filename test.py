import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# HOST = 'https://oatd.org/'
KEY_WORD = 'quantum+cryptography'
KEY_WORD_2 = 'IoT+security'
KEY_WORD_3 = 'automated+and+adaptive+networks'
URL = f'https://oatd.org/oatd/search?q={KEY_WORD}&form=basic'
URL_2 = f'https://oatd.org/oatd/search?q={KEY_WORD_2}&form=basic'
# URL_3 = f'https://oatd.org/oatd/search?q={KEY_WORD_3}&form=basic'
URL_3 = f'https://oatd.org/oatd/search?q={KEY_WORD_3}&form=basic&start=31'


def get_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        return False
    return response.text


def item_processing(item, word):
    item_ = item.replace('Subjects/Keywords:', '').replace('.', '').replace('/', '').strip().lower()
    if item_ != word and not item_.isdigit():
        return item_
    return None


def key_word_processing(file_name, key, word):
    new_list = get_file_data(file_name)
    if len(key) > 18:
        if key[0:18] == 'Subjects/Keywords:':
            ll = key.split(';')
            for i in ll:
                item = item_processing(i, word)
                if item is not None:
                    new_list.append(item)
    else:
        item = item_processing(key, word)
        if item is not None:
            new_list.append(item)
    save_to_file(new_list, file_name)


def get_file_data(file_name):
    file = open('data/' + file_name, 'r')
    data = json.loads(file.read())
    file.close()
    return data


def save_to_file(data, file_name):
    data = json.dumps(data)
    file = open('data/' + file_name, 'w')
    file.write(data)
    file.close()


def parse_page_in_json(url, filename, keyword):
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    key_words = soup.find_all('p', class_='keywords')
    for key_word in key_words:
        key_word_processing(filename, key_word.text, keyword)


def save_to_xlsx_pandas(list_):
    df = pd.DataFrame(list_)
    writer = pd.ExcelWriter("technologies.xlsx", engine='xlsxwriter')
    df.to_excel(writer, sheet_name='x1')
    writer.save()


def list_sort(list_):
    """
    :param list_: list from .json
    :return: dict('technology': quantity)
    """
    dict_ = {i: list_.count(i) for i in list_}
    sorted_dict = dict(sorted(dict_.items(), key=lambda kv: kv[1], reverse=True))
    return sorted_dict


def json_to_list(file):
    list_ = get_file_data(file)
    return list(list_sort(list_))


def main():
    parse_page_in_json(URL, "quantum_crypt.json", 'quantum cryptography')
    parse_page_in_json(URL_2, "iot_security.json", 'iot security')
    parse_page_in_json(URL_3, "auto_adapt_net.json", 'automated and adaptive networks')

    sort_list1 = json_to_list('quantum_crypt.json')
    sort_list2 = json_to_list('iot_security.json')
    sort_list3 = json_to_list('auto_adapt_net.json')

    dict_ = {
        'Quantum cryptography': sort_list1[:50],
        'IoT security': sort_list2[:50],
        'Automated and adaptive networks': sort_list3[:50]
    }
    save_to_xlsx_pandas(dict_)


if __name__ == '__main__':
    main()
