import urllib.request
import re
from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError

urls = {
    '22lr': 'https://www.targetsportsusa.com/ISearch.aspx?PageNumber=0&PageSize=40&PageSort=pv.PricePerRound&ColorFilter=&SizeFilter=&PriceFilter=&TypeFilter=&ManufacturerFilter=&CategoryFilter=202&GenreFilter=&DistributorFilter=&VectorFilter=&SectionFilter=&LibraryFilter=&stockFilter=false&Filter=%',
    '9mm': 'https://www.targetsportsusa.com/ISearch.aspx?PageNumber=0&PageSize=40&PageSort=pv.PricePerRound&ColorFilter=&SizeFilter=&PriceFilter=&TypeFilter=&ManufacturerFilter=&CategoryFilter=51&GenreFilter=&DistributorFilter=&VectorFilter=&SectionFilter=&LibraryFilter=&stockFilter=false&Filter=%'
}

TO_FIND_CLASS = 'add-to-cart'
#TO_FIND_CLASS = 'add-to-cart stockNotify'

def check_ammo(url):
    with urllib.request.urlopen(url) as response:
        page = response.read()
        reo = re.compile('(<br>|<img[^>]*>|<!DOCTYPE [^>]*>)')
        page = '<?xml version="1.0"?>\n<root>\n' + reo.sub('', page.decode('utf8')) + '\n</root>\n'
        page = page.replace("&", "&amp;")
        try:
            doc = parseString(page)
        except ExpatError as e:
            print(e)
            print(f'Page {url}')
            print(page)
            raise 'Fail to parse'
        pass

    avail_ammos = []
    buttons = doc.getElementsByTagName('button')
    for e in buttons:
        if e.getAttribute('class') == TO_FIND_CLASS:
            parent = e.parentNode
            h2 = parent.getElementsByTagName('h2')[0]
            ammo_name = h2.childNodes[1].nodeValue.strip()

            divs = parent.getElementsByTagName('div')
            price_div = divs[1]
            ammo_price = price_div.childNodes[0].nodeValue.strip()
            if len(price_div.childNodes) > 1 and price_div.childNodes[1].nodeName == 'span':
                ammo_price = ammo_price + ' (' + price_div.childNodes[1].childNodes[0].nodeValue.strip() + ')'
                pass

            avail_ammos.append((ammo_name, ammo_price))
            pass
        pass
    return avail_ammos

for ammo_type, url in urls.items():
    ammos = check_ammo(url)
    if len(ammos):
        print(ammo_type + ':')
        for ammo, price in ammos:
            print(f'   {ammo} -- {price}')
            pass
        pass
    pass
