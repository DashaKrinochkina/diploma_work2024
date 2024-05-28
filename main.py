import re
import pymorphy2

file = "texts/all_texts.txt"
with open(file, 'rb') as f:
    q = f.read()
    text = q.decode('windows-1251')

tokens = text.split('.')
tokens = list(map(str.strip, tokens))

morph = pymorphy2.MorphAnalyzer()

morphed = []
for sentence in tokens:
    ms = []
    for i, word in enumerate(sentence.split()):
        mt = morph.parse(word)[0]
        wtn = [i, mt.word, mt.tag, mt.normal_form]
        ms.append(wtn)
    morphed.append(ms)
# print(list(morphed))

stat_strat = {}

'''def find_person(morphed, tokens):
    count = 0
    tactics = []
    for i, sentence in enumerate(morphed):
        for word in sentence:
            if {'NOUN', 'nomn'} in word[2] or {'NPRO', 'nomn', '3per'} in word[2]:
                break
            if {'VERB', 'perf', 'masc', 'sing', 'past', 'indc'} in word[2] or \
                    word[3] == 'мой' or word[3] == 'я':
                count += 1
                #print(tokens[i])
                tactics.append(tokens[i])
                break
    return count, tactics
#print('ПЕРСОНАЛИЗАЦИЯ:', find_person(morphed, tokens))'''


def find_perf(morphed, tokens):
    tactics = []
    flag = False
    for i, sentence in enumerate(morphed):
        for word in sentence:
            if {'NOUN', 'nomn'} in word[2] or {'NPRO', 'nomn', '3per'} in word[2] or {'Name'} in word[2]:
                flag = False
                break
            if {'VERB', 'perf', 'masc', 'sing', 'past', 'indc'} in word[2]:
                flag = True
        if flag:
            tactics.append(tokens[i])
            flag = False
    return tactics


def find_person(morphed, tokens):
    tactics = []
    for i, sentence in enumerate(morphed):
        for word in sentence:
            if word[3] == 'мой' or word[3] == 'я':
                #print(tokens[i])
                tactics.append(tokens[i])
                break
    result = find_perf(morphed, tokens)
    tactics.extend(result)
    tactics = list(dict.fromkeys(tactics))
    return len(tactics), tactics


def find_ident(morphed, tokens):
    count = 0
    tactics = []
    for i, sentence in enumerate(morphed):
        for word in sentence:
            #if word[3] == 'наш' or word[3] == 'мы':
            if word[3] == 'наш' and {'plur'} in word[2]:
                count += 1
                #print(tokens[i])
                tactics.append(tokens[i])
                break
    return count, tactics


def find_thanks(morphed, tokens):
    count = 0
    tactics = []
    markers = ['спасибо', 'благодарный', 'благодарить']
    for i, sentence in enumerate(morphed):
        for n, word in enumerate(sentence):
            try:
                if word[3] in markers and (sentence[n+1][3] == 'весь' or sentence[n+1][3] == 'вы'
                                           or sentence[n+1][3] == 'каждый'):
                    count += 1
                    #print(tokens[i])
                    tactics.append(tokens[i])
                    break
            except IndexError:
                break
    return count, tactics
# find_thanks(morphed, tokens)


def find_solid(morphed, tokens):
    count = 0
    tactics = []
    markers = ['дорогие', 'уважаемые', 'праздником', 'поздравляю', 'желаю', 'знаю', 'понимаю']
    for i, sentence in enumerate(morphed):
        for word in sentence:
            if word[1] in markers or word[3] == 'друг' or \
                    word[3] == 'видеть' and {'impf', 'pres', '1per'} in word[2]:
                count += 1
                #print(tokens[i])
                tactics.append(tokens[i])
                break
    result = find_thanks(morphed, tokens)
    count += result[0]
    tactics.extend(result[1])
    return count, tactics


def find_positive(morphed, tokens):
    count = 0
    tactics = []
    markers = {'noun': ['рекорд', 'достижение', 'результат', 'рост', 'признание',
                        'лидер', 'событие', 'путь', 'увеличение'],
               'exact': ['успехи', 'успех'],
               'verb': ['удалось', 'позволило', 'преодолели', 'побили',
                        'приступили', 'запустили'],
               'inf': ['увеличить', 'увеличиться', 'вырасти', 'доказать'],
               'adjv': ['рекордный']}
                #'провели', 'работу'
    for i, sentence in enumerate(morphed):
        for word in sentence:
            if {'VERB', 'futr'} in word[2]:
                break
            if word[3] in markers['noun'] or word[1] in markers['exact'] or word[1] in markers['verb'] or \
                    word[1] in markers['adjv'] or word[3] in markers['inf'] and \
                    {'VERB', 'perf', 'past', 'indc'} in word[2]:
                count += 1
                #print(tokens[i])
                tactics.append(tokens[i])
                break
    return count, tactics


def find_promise(morphed, tokens):
    count = 0
    tactics = []
    markers = ['обязательно', 'точно']
    for i, sentence in enumerate(morphed):
        flag = False
        mark_flag = False
        for word in sentence:
            if word[3] in markers:
                mark_flag = True
            if {'VERB', 'futr', '1per'} in word[2] and word[3] == 'быть':
                flag = True
                continue

            '''if {'VERB', 'futr', '1per'} in word[2]:
                count += 1
                print(tokens[i])
                break'''

            if flag and {'INFN'} in word[2] or mark_flag and {'VERB', 'futr', '1per'} in word[2]:
                count += 1
                #print(tokens[i])
                tactics.append(tokens[i])
                break
    return count, tactics


def find_emotion(morphed, tokens):
    count = 0
    tactics = []
    markers = {'noun': ['герой', 'мужество', 'подвиг', 'родина', 'единство',
                        'патриот', 'долг', 'комфорт', 'безопасность',
                        'здоровье', 'любовь', 'память', 'комфортный', 'труд', 'природа'],
               'life': ['качество', 'здоровый', 'комфортный', 'хороший']}
    for i, sentence in enumerate(morphed):
        l_flag = False
        m_flag = False
        for word in sentence:
            if word[3] == 'жизнь':
                l_flag = True
            if word[3] in markers['life']:
                m_flag = True
            if word[3] in markers['noun'] or l_flag and m_flag or word[1] == 'люди':
                count += 1
                #print(tokens[i])
                tactics.append(tokens[i])
                break
    return count, tactics


# создание словаря, где ключ -- название тактики,
# значение -- кортеж с кол-вом контекстов данной тактики и списком самих контекстов
'''stat_strat['person'] = find_person(morphed, tokens)
stat_strat['ident'] = find_ident(morphed, tokens)
stat_strat['solid'] = find_solid(morphed, tokens)
stat_strat['positive'] = find_positive(morphed, tokens)
stat_strat['promise'] = find_promise(morphed, tokens)
stat_strat['emotion'] = find_emotion(morphed, tokens)'''

# вывод контекстов для тактик по-отдельности
# print('ПЕРСОНАЛИЗАЦИЯ:', find_person(morphed, tokens))
# print('ОТОЖДЕСТВЛЕНИЕ:', find_ident(morphed, tokens))
# print('СОЛИДАРИЗАЦИЯ:', find_solid(morphed, tokens))
# print('АКЦЕНТ ПОЛОЖИТЕЛЬНОЙ ИНФОРМАЦИИ:', find_positive(morphed, tokens))
# print('ОБЕЩАНИЕ:', find_promise(morphed, tokens))
# print('ФОРМИРОВАНИЕ ЭМОЦ. НАСТРОЯ:', find_emotion(morphed, tokens))

# запись контекстов для каждой тактики в отдельный текстовый файл
'''for i in stat_strat.keys():
    with open(f'texts/{i}.txt', 'w', encoding='utf-8') as f:
        f.write('\n')
        f.write('\n\n'.join(stat_strat[i][1]))'''
