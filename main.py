import json
from naver_api_utils import get_coordinates_from_address
from web_scraper import scrape_website

# properties.json 파일에서 설정값 불러오기
with open('properties.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

client_id = config['NAVER_API_ID']
client_secret = config['NAVER_API_KEY']

data_list, total_len = scrape_website(config['CENTER_URL'])

for idx, data in enumerate(data_list):
    mapx, mapy = get_coordinates_from_address(
        data['address'], client_id, client_secret)
    data['mapx'] = mapx
    data['mapy'] = mapy
    percentage = (idx + 1) / total_len * 100
    print(f"raw data: {percentage: .2f}%")

with open('centerData.json', 'w', encoding='utf-8') as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4)
