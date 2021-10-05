import requests
from bs4 import BeautifulSoup
import json

# HOST = 'https://oatd.org/'
KEY_WORD = 'quantum+cryptography'
KEY_WORD_2 = 'IoT+security'
KEY_WORD_3 = 'automated+and+adaptive+networks'
URL = f'https://oatd.org/oatd/search?q={KEY_WORD}&form=basic'
URL_2 = f'https://oatd.org/oatd/search?q={KEY_WORD_2}&form=basic'
# URL_3 = f'https://oatd.org/oatd/search?q={KEY_WORD_3}&form=basic'
URL_3 = 'https://oatd.org/oatd/search?q=automated+and+adaptive+networks&form=basic&start=31'


def get_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        return False
    return response.text


def key_word_processing(file_name, key, word):

    new_list = get_file_data(file_name)
    if len(key) > 18:
        if key[0:18] == 'Subjects/Keywords:':
            ll = key.split(';')
            for i in ll:
                item = i.replace('Subjects/Keywords:', '').replace('.', '').replace('/', '').strip().lower()
                if item != word and not item.isdigit():
                    new_list.append(item)
    else:
        item = key.replace(';', '').replace('.', '').replace('/', '').lower()
        if item != word and not item.isdigit():
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


def main():
    parse_page_in_json(URL, "quantum_crypt.json", 'quantum cryptography')
    parse_page_in_json(URL_2, "iot_security.json", 'iot security')
    parse_page_in_json(URL_3, "auto_adapt_net.json", 'automated and adaptive networks')


if __name__ == '__main__':
    main()
