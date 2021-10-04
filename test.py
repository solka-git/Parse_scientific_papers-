import requests
from bs4 import BeautifulSoup
import json

# HOST = 'https://oatd.org/'
KEY_WORD = 'quantum+cryptography'
URL = f'https://oatd.org/oatd/search?q={KEY_WORD}&form=basic'

list = []


def get_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        return False
    return response.text


def key_word_processing(key):
    file_name = "keyword.json"
    new_list = get_file_data(file_name)
    if len(key) > 18:
        if key[0:18] == 'Subjects/Keywords:':
            ll = key.split(';')
            for i in ll:
                new_list.append(i.replace('Subjects/Keywords:', '').strip().lower())
    else:
        new_list.append(key.replace(';', ''))
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


def main():
    html = get_html(URL)
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    key_words = soup.find_all('p', class_='keywords')
    for key_word in key_words:
        key_word_processing(key_word.text)


if __name__ == '__main__':
    main()
