import requests
from bs4 import BeautifulSoup


def scrape_website(url):
    URL = url
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    data_list = []
    total_len = len(soup.select('tbody tr'))

    for idx, tr in enumerate(soup.select('tbody tr')):
        tds = tr.select('td')
        if len(tds) < 5:
            continue
        name = tds[2].get_text().strip()
        address_line = [li for li in tds[3].select(
            'li') if '주소' in li.get_text()][0]
        address = address_line.get_text().replace("주소 :", "").strip()
        tel_line = [li for li in tds[3].select(
            'li') if '전화' in li.get_text()][0]
        tel = tel_line.get_text().replace("전화 :", "").strip()
        homepage_link = tds[4].find('a')
        homepage = homepage_link['href'] if homepage_link and homepage_link['href'] != '' else None

        data_list.append({
            "name": name,
            "address": address,
            "tel": tel,
            "homepage": homepage
        })

    return data_list, total_len
