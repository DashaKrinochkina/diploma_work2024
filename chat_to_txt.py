#!/usr/bin/python3

import json
import re

gubers = {'nikit': 'Глеб Никитин', 'moor': 'Александр Моор', 'kotyuk': 'Михаил Котюков',
          'nikol': 'Айсен Николаев, Глава Республики Саха (Якутия). Официальный канал.',
          'vorob': 'Воробьёв LIVE', 'kozhem': 'Кожемяко | официально'}
for surn in gubers.keys():
    with open(f"results/{surn}_result.json", encoding="utf-8") as f:
        messages = json.load(f)["messages"]

    texts = []
    for message in messages:
        if message["date"] < "2023-07-01T00:00:00":
            continue

        if "from" not in message:
            continue
        if message["from"] != gubers[surn]:  # change governor's name
            continue

        if type(message["text"]) == list:
            text = []

            for el in message["text"]:
                if type(el) == str:
                    text.append(el)

                if type(el) == dict:
                    if el["type"] == "bold" or el["type"] == "plain":
                        text.append(el["text"])
            texts.append(''.join(text))

        elif type(message["text"]) == str:
            texts.append(message["text"])
        else:
            continue

    texts = "\n".join(texts)
    texts = texts.lower()

    texts = re.sub("[^A-Za-zА-Яа-яЁё \n.]", "", texts)  # no punctuation marks
    texts = re.sub("[\n\r]", " ", texts)
    # print(len(texts))

    with open('texts/all_texts.txt', 'a') as f:
        f.write('\n')
        f.write(texts)
