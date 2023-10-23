import json
import pymysql

# properties.json 파일에서 설정값 불러오기
with open('properties.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 데이터베이스 연결 설정
connection = pymysql.connect(
    host=config['DB_HOST'],
    port=config['DB_PORT'],
    user=config['DB_USER'],
    password=config['DB_PASSWORD'],
    db=config['DB_NAME'],
    charset='utf8mb4'
)

cursor = connection.cursor()

# JSON 파일 읽기
with open('newCenterData.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 데이터베이스에 데이터 저장
for item in data:
    sql = "INSERT INTO centers (name, address, email, tel, homepage, mapx, mapy, do_si, si_gun_gu, dong, area_etc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (item['name'], item['address'], None, item['tel'], item['homepage'],
                   item['mapx'], item['mapy'], item['do_si'], item['si_gun_gu'], item['dong'], item['area_etc']))

# 변화를 데이터베이스에 반영
connection.commit()

# 종료
cursor.close()
connection.close()
