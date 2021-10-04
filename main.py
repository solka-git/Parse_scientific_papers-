import json
import pandas as pd


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


def save_to_xlsx_pandas(list_):
    df = pd.DataFrame(list_)
    writer = pd.ExcelWriter("crypto.xlsx", engine='xlsxwriter')
    df.to_excel(writer, sheet_name='x1')
    writer.save()


def list_count(list_):
    dict_ = {i: list_.count(i) for i in list_}
    sorted_dict = dict(sorted(dict_.items(), key=lambda kv: kv[1], reverse=True))
    return sorted_dict


file_name = 'keyword.json'
list_ = get_file_data(file_name)

dict_list = list_count(list_)
print(list(dict_list))

dict = {
    'Quantum cryptography': list_[:50]
}
save_to_xlsx_pandas(dict)







# file_name = "keyword.json"
# new_list = get_file_data(file_name)
#
# if key[0:18] != 'Subjects/Keywords:':
#     new_list.append(key.replace(';', ''))
# else:
#     ll = key.split(';')
#     for i in ll:
#         new_list.append(i.replace('Subjects/Keywords:', '').strip().lower())
#
# save_to_file(new_list, file_name)
