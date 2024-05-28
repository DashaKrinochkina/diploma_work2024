#!/usr/bin/python3

import json
import csv
import re

with open("results/<имя файла с текстами и метаданными>.json", encoding="utf-8") as f:
    data = json.load(f)

messages = data["messages"]
texts = []
for message in messages:
    if message["date"] < "2023-07-01T00:00:00":
        continue

    if "from" not in message:
        continue

    if message["from"] != data["name"]:
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

clean = []

for text in texts:
    text = re.sub("[^\x00-\x7Fа-яА-ЯЁё–]", "", text)
    clean.append(text)

with open("csvs/<имя файла для разметки>.csv", "w") as f:
    b = csv.writer(f)
    for t in clean:
        b.writerow([t])
