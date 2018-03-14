#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re
import ast

'''
This currently only works with rodpedia, the file must be named items and in the same
directory as the script.



todo:
add support for selecting a file from the command line.
add support for searching for items that don't immediately pop on rodpedia
add threading to speed up the searching
'''



def get_web_item_info(item:str)->dict:
    r = requests.get('https://rodpedia.realmsofdespair.info/index.php?title=Special%3ASearch&search={0}&go=Go'.format(item))
    print('Looking up {0}......'.format(item))
    soup = BeautifulSoup(r.text, 'html.parser')
    raw = soup.find_all('pre')
    info = ''
    if not raw:
        info = 'Item not found.\n'
    else:
        for i in raw:
            info += i.text
    return {item: info}

def format_item_list(items:list)->list:
    '''
    Clear the excess nonsense, number of items etc.
    :param items: item list
    :return: clean item list
    '''
    cleanList = []
    for i in items:
        newItem = re.sub("[\(\[].*?[\)\]]", "", i)
        newItem = newItem.strip()
        newItem = newItem.lower()
        cleanList.append(newItem)
    return cleanList

def create_item_list(fileName:str):
    try:
        with open(fileName, 'r') as f:
            itemList = f.read().split('\n')
            itemList = [i.strip() for i in itemList]
            return itemList
    except FileNotFoundError:
        print('No such file.')


def present_info(contents: dict):
    for k,v in contents.items():
        if v == '':
            print(k)
            print('Present info unable to locate item.')
            print('')
        else:
            print(k)
            print(v)


def write_dict(itemsDict:dict):
    with open('./data/database.dict', 'w') as f:
        f.write(str(itemsDict))


def read_dict():
    try:
        with open('./data/database.dict', 'r') as f:
                currentDB = ast.literal_eval(f.read())
                return currentDB
    except FileNotFoundError:
        print('No dict file exists.')


def database_has_data()->bool:
    try:
        with open('./data/database.dict', 'r') as f:
            f.seek(0)  # ensure you're at the start of the file..
            first_char = f.read(1)
            if not first_char:
                return False
            else:
                return True
    except FileNotFoundError:
        print('No dict file exists.')


def get_database_items():
    if database_has_data():
        return read_dict()
    else:
        return {}


# Main function to parse stuff.

if __name__ == "__main__":

    itemList = create_item_list('items')
    itemList = format_item_list(itemList)

    print('{0} items to be searched.'.format(len(itemList)))
    counter = len(itemList)

    # Check our dict file first.
    cachedInfo = get_database_items()
    selectedInfo = {}
    newItemList = []

    print('Checking cache...')
    for i in itemList:
        if i in cachedInfo.keys():
            selectedInfo[i] = cachedInfo[i]
            counter -= 1
        else:
            newItemList.append(i)
    print('{0} items remain.\n'.format(counter))

    itemsDict = {}
    if not newItemList:
        present_info(selectedInfo)
        exit(0)
    else:
        for i in newItemList:
            info = get_web_item_info(i)
            itemsDict.update(info)
            counter -= 1
            print('{0} web checks remain.'.format(counter))

        itemsDict.update(cachedInfo)
        present_info(itemsDict)
        write_dict(itemsDict)
        exit(0)
