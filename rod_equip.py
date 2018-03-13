import requests
from bs4 import BeautifulSoup
import re
import getopt


def get_item_info(item:str)->dict:
    r = requests.get('https://rodpedia.realmsofdespair.info/index.php?title=Special%3ASearch&search={0}&go=Go'.format(item))
    print('Looking up {0}......'.format(item))
    soup = BeautifulSoup(r.text, 'html.parser')
    raw = soup.find_all('pre')
    info = ''
    for i in raw:
        info += i.text
    return {item:info}

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
        newItem = newItem.capitalize()
        cleanList.append(newItem)
    return cleanList

def create_item_list(fileName:str):
    fileName = 'items'
    try:
        with open('items', 'r') as f:
            itemList = f.read().split('\n')
            itemList = [i.strip() for i in itemList]
            return itemList
    except FileNotFoundError:
        print('No such file.')


def present_info(contents: dict):
    for k,v in contents.items():
       if v == '':
           print(k)
           print('Unable to locate item.')
       else:
            print(k)
            print(v)


# Main function to parse stuff.

if __name__ == "__main__":
    itemList = create_item_list('items')
    itemList = format_item_list(itemList)
    itemsDict = {}
    print('{0} items to be searched.'.format(len(itemList)))
    counter = len(itemList)
    for i in itemList:
        info = get_item_info(i)
        itemsDict.update(info)
        counter -= 1
        print('{0} items remain.'.format(counter))
    present_info(itemsDict)