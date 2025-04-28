import requests
from xml.etree import ElementTree as ET


if __name__ == '__main__':
    response = requests.get('https://www.mtgo.com/decklists')
    tree = ET.parse(response.text)
    root = tree.getroot()
    
    for child in root:
        print(child.tag, child.attrib)