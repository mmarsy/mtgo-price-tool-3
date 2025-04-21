import pandas as pd
import requests
import os
import json
import logging
import re


logger = logging.getLogger(__name__)


def clear_string(string, r_char='*'):
    new_str = re.sub(r'[^a-zA-Z0-9 -]', r_char, string)
    new_str = new_str.strip(r_char)
    
    return new_str.lower()



class CardCollection:
    cards: pd.DataFrame
    
    def __init__(self, src: str):
        df = pd.read_xml(src)
        self.cards = df[['CatID', 'Quantity', 'Name']]
        

class CardDatabase:
    cards = None
    
    def __init__(self, def_src:str, price_src: str):
        with open(def_src) as def_file:
            def_dict = json.loads(def_file.read())
            def_file.close()
            
        with open(price_src) as price_file:
            price_dict = json.loads(price_file.read())
            price_file.close()
            
        
        name_to_id = {}
        name_to_id_cheapest = {}
        
        for key in def_dict:
            try:
                def_dict[key]['price'] = price_dict[key]
            except KeyError as e:
                logger.info(e)
            
            del def_dict[key]['rarity']
            del def_dict[key]['foil']
            
            name = clear_string(def_dict[key]['name'])
            
            def_dict[key]['name'] = name
            if name not in name_to_id:
                name_to_id[name] = [key]
                name_to_id_cheapest[name] = key
            else:
                name_to_id[name].append(key)
                if price_dict[name_to_id_cheapest[name]] > price_dict[key]:
                    name_to_id_cheapest[name] = key
            
        del price_dict
        self.cards = def_dict
        self.name_to_id = name_to_id
        self.name_to_id_cheapest = name_to_id_cheapest
        
    def __getitem__(self, key):
        try:
            int(key)
            return self.cards[key]
        
        except ValueError:
            formated_key = clear_string(key)
            cat_id = self.name_to_id_cheapest[formated_key]
            return {'CatID': cat_id, 'price': self[cat_id]['price']}
        
            
if __name__ == '__main__':
    test_src = 'data/'
    def_src = test_src + os.listdir(test_src)[0]
    price_src = test_src + os.listdir(test_src)[2]
    
    db = CardDatabase(def_src, price_src)
    while True:
        x = input('Try it yourself. (q to quit)')
        if x == 'q':
            break
        if x == 'print':
            print(db.name_to_id)
        else:
            print(db[x])

    