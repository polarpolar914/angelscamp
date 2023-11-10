from key import sk_api_key
import requests


def get_address_from_place_name(place_name, api_key):
    # 장소명으로부터 주소를 얻기 위한 T Map API 엔드포인트
    search_url = f'https://api2.sktelecom.com/tmap/pois?version=1&format=json&callback=result&searchKeyword={place_name}'

    # 요청 파라미터
    params = {
        'appKey': api_key,
        'reqCoordType': 'KATECH',  # 요청 좌표계 타입을 KATECH 설정
        'resCoordType': 'KATECH',  # 응답 좌표계 타입을 KATECH 설정
        'searchKeyword': place_name
    }

    response = requests.get(search_url, params=params)
    place_data = response.json()

    first_place_info = place_data['searchPoiInfo']['pois']['poi'][0]

    # 필요한 데이터 추출
    place_name = first_place_info['name']
    address = first_place_info['newAddressList']['newAddress'][0]['fullAddressRoad']
    latitude = first_place_info['noorLat']
    longitude = first_place_info['noorLon']
    return (place_name, address, latitude, longitude)

def get_route_coordinates(start, end, api_key):

    start = get_address_from_place_name(start, api_key)
    end = get_address_from_place_name(end, api_key)

    startX = start[3]
    startY = start[2]

    endX = end[3]
    endY = end[2]


    # T Map 경로 검색 API 엔드포인트
    route_url = 'https://api2.sktelecom.com/tmap/routes?version=1&format=json&callback=result'

    headers = {
        'appKey': api_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'startX': startX,
        'startY': startY,
        'endX': endX,
        'endY': endY,
        'reqCoordType': 'KATECH',
        'resCoordType': 'KATECH',
        'startName': '출발지',
        'endName': '도착지'
    }

    response = requests.post(route_url, json=payload, headers=headers)
    route_data = response.json()

    # 경로상의 좌표 추출
    coordinates = []
    sampling_coordinates = []
    x, y = route_data['features'][0]['geometry']['coordinates'][0], route_data['features'][0]['geometry']['coordinates'][1]
    coordinates.append([x, y])
    sampling_coordinates.append([x, y])

    for i in route_data['features']:
        if isinstance(i['geometry']['coordinates'][0], list):
            for j in i['geometry']['coordinates']:
                coordinates.append(j)
                if ((j[0] - x) ** 2) > 11560000 or ((j[1] - y) ** 2) > 11560000:
                    sampling_coordinates.append(j)
                    x, y = j[0], j[1]
        else:
            coordinates.append(i['geometry']['coordinates'])
            if ((i['geometry']['coordinates'][0] - x) ** 2) > 11560000 or ((i['geometry']['coordinates'][1] - y) ** 2) > 11560000:
                sampling_coordinates.append(i['geometry']['coordinates'])
                x, y = i['geometry']['coordinates'][0], i['geometry']['coordinates'][1]

    return coordinates[::4], sampling_coordinates

# 함수 사용 예시
# place_name_start = "서울시청"
# place_name_end = "부산타워"
# interval = 10
# api_key = 'YOUR_T_MAP_API_KEY'
# route_coordinates = get_route_coordinates(place_name_start, place_name_end, interval, api_key)

route_coordinates = get_route_coordinates("안동한일아파트", "안동한일여고",  sk_api_key)
print(route_coordinates)