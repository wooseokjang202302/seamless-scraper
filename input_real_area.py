import json
import requests
import xml.etree.ElementTree as ET


def get_address_from_coordinates(x, y, client_id, client_secret):
    url = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }
    params = {
        "coords": f"{x}, {y}",
        "orders": "admcode,legalcode,addr,roadaddr"
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        root = ET.fromstring(response.text)

        do_si = root.find(".//area1/name").text
        si_gun_gu = root.find(".//area2/name").text
        dong = root.find(".//area3/name").text

        # 도로명 주소 정보 추가
        road_name_element = root.find(".//order[name='roadaddr']/land/name")
        if road_name_element is not None:
            road_name = road_name_element.text
        else:
            road_name = None

        road_number_element = root.find(
            ".//order[name='roadaddr']/land/number1")
        if road_number_element is not None:
            road_number = road_number_element.text
        else:
            road_number = None

        area_etc = f"{road_name or ''} {
            road_number or ''}".strip() if road_name or road_number else None

        return {
            "do_si": do_si,
            "si_gun_gu": si_gun_gu,
            "dong": dong,
            "area_etc": area_etc  # 나머지 주소 정보 반환
        }
    return None


# properties.json 파일에서 설정값 불러오기
with open('properties.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

client_id = config['NAVER_API_ID']
client_secret = config['NAVER_API_KEY']

# centerData.json 파일에서 데이터 불러오기
with open('centerData.json', 'r', encoding='utf-8') as f:
    centers = json.load(f)

for idx, center in enumerate(centers):
    x = center['mapx']
    y = center['mapy']

    # 주소 얻기
    address_data = get_address_from_coordinates(
        x, y, client_id, client_secret)

    if address_data:
        area_1 = address_data['do_si']
        area_2 = address_data['si_gun_gu'].split(' ')[0]
        area_3 = address_data['dong']
        area_etc = address_data['area_etc']

        # center에 새로운 주소 정보를 추가
        center['do_si'] = area_1
        center['si_gun_gu'] = area_2
        center['dong'] = area_3
        center['area_etc'] = area_etc

    else:
        center['do_si'] = None
        center['si_gun_gu'] = None
        center['dong'] = None
        center['area_etc'] = None

with open('newCenterData.json', 'w', encoding='utf-8') as f:
    json.dump(centers, f, ensure_ascii=False, indent=4)
