#!/usr/bin/env python3
import json
import re
from datetime import datetime

with open("operations.json", "r", encoding = "utf-8") as read_files:
    data = json.load(read_files)

data = [trans for trans in data if trans and trans['state'] == 'EXECUTED' ] #избавляемся от пустых элементов и отменённых операций
sorted_data = sorted(data, key=lambda x:x.get('date'), reverse = True) #сортируем операции по дате и в нужном нам порядке начиная от последних

#вывод счетов
for trans in sorted_data[:5]:
    format_date = datetime.strptime(trans['date'], "%Y-%m-%dT%H:%M:%S.%f")
    format_date = format_date.strftime('%d.%m.%Y') # переводим дату нужный формат

    my_from = trans.get('from', 'not_found')
    my_to = trans.get('to', 'not_found')

    number_from = re.findall(r'\w+$', my_from) #получаем номер счета или карты
    number_to = re.findall(r'\w+$', my_to)

    score_from= re.findall(r'^\w+', my_from)#получаем первое слово счета или карты
    score_to= re.findall(r'^\w+', my_to)

    score_from =str(score_from)[2:-2]
    score_to =str(score_to)[2:-2]
   #скрываем цифры в номере карта или счета
    if score_from == "Счет":
        from_to ="Cчет " + "**" + str(number_from)[-6:-2]
    elif score_from == "not_found":
        from_to = "not_found"
    else:
        from_to = str(number_from)[2:6] + " " + str(number_from)[6:8] + "** **** " + str(number_from)[-6:-2]#заменяем номер на зашифрованый
        from_to= re.sub(str(number_from)[2:-2], str(from_to), str(my_from))

    if score_to == "Счет":
        to ="Cчет " + "**" + str(number_to)[-6:-2]
    elif score_to == "not_found":
        from_to = "not_found"
    else:
        to = str(number_to)[2:6] + " " + str(number_to)[6:8] + "** **** " + str(number_to)[-6:-2]
        to = re.sub(str(number_to)[2:-2], str(to), str(my_to))
#Вывод счета
    print('{date} {description}\n'
          '{from_to} -> {to}\n'
          '{amount} {currency} \n'.format(from_to=from_to,  date = format_date,description = trans.get("description", "not found"), to = to,
                                        amount =trans.get('operationAmount', 'not found').get('amount', 'not found') , currency = trans['operationAmount']['currency']['name'], )
          )
