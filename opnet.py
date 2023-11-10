import requests
import json
import xmltodict
from key import opnet_api_key, sk_api_key
from route import get_route_coordinates, get_address_from_place_name


def find_oil_station(origin, dest):
    route, iter_tuples = get_route_coordinates(origin, dest, sk_api_key)

    iter_number = len(iter_tuples)
    result_list = []

    for i in range(iter_number):
        x_coordinate = iter_tuples[i][0]
        y_coordinate = iter_tuples[i][1]
        radius = 1000
        url = f"http://www.opinet.co.kr/api/aroundAll.do?code={opnet_api_key}&x={x_coordinate}&y={y_coordinate}&radius={radius}&sort=1&prodcd=B027&out=xml"
        result = xmltodict.parse(requests.get(url).content)

        if 'RESULT' in result and result['RESULT'] is not None:
            oil_stations = result['RESULT']['OIL']
            if isinstance(oil_stations, list):
                for i, oil_station in enumerate(oil_stations):
                    result_list.append(oil_station)
            elif isinstance(oil_stations, dict):
                result_list.append(oil_stations)

    keys_to_exclude = ['UNI_ID', 'POLL_DIV_CO']
    filtered_oil_stations = [
        {key: value for key, value in station.items() if key not in keys_to_exclude}
        for station in result_list
    ]
    ''' #tried solution1 !
    sorted_oil_stations = sorted(filtered_oil_stations, key=lambda x: float(x['GIS_X_COOR']))

    for i in range(len(sorted_oil_stations)):
        print(sorted_oil_stations[i])
    '''
    '''
    r_start = float(sorted_oil_stations[0]['GIS_X_COOR'])
    r_end = float(sorted_oil_stations[-1]['GIS_X_COOR'])

    print(r_start,r_end)

    left = r_start
    right = left + 100

    while right < r_end:
        x_unit = [i for i in sorted_oil_stations if left <= float(i['GIS_X_COOR']) <= right]
        x_unit = sorted(x_unit, key=lambda x: float(x['GIS_Y_COOR']))

        print(x_unit)
        left += 100
        right += 100
    '''
    filtered_result_list = []
    for i in range(len(filtered_oil_stations)):
        for k_2 in route:
            if (abs(float(k_2[0]) - float(filtered_oil_stations[i]['GIS_X_COOR'])) <= 1000 and abs(
                    float(k_2[1]) - float(filtered_oil_stations[i]['GIS_Y_COOR'])) <= 1000):
                filtered_result_list.append(filtered_oil_stations[i])

    sorted_oil_stations = sorted(filtered_result_list, key=lambda x: float(x['PRICE']))

    # JSON 형식의 문자열 생성
    json_data = json.dumps(sorted_oil_stations[0], ensure_ascii=False)
    return json_data





