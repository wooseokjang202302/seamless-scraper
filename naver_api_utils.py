import requests


# 주소를 이용한 좌표값 구하기
def get_coordinates_from_address(address, client_id, client_secret):
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }
    params = {
        "query": address
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if 'addresses' in data and len(data['addresses']) > 0:
        x = data['addresses'][0]['x']
        y = data['addresses'][0]['y']
        return x, y
    return None, None
