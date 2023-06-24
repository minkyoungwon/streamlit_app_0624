# 폴리움을 주로 사용하는데 pydeck 찾아보니깐 좀더 다채롭게 쓸수있어서 활용


import pandas as pd
import requests
import json
import pydeck as pdk
import streamlit as st

st.write("# 민경원 서울시 따릉이 시각화 결과")

api_key = "757766614b74616c374a46696a55"
bike_dict = {"rackTotCnt":[], "stationName":[],
             "parkingBikeTotCnt":[], "shared":[],
             "latitude":[], "longitude":[]}
num = 0
while True:
    url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/bikeList/{1 + 1000 * num}/{1000 + 1000 * num}/"
    data = requests.get(url)
    result = json.loads(data.text)  # json --> dict
    for row in result["rentBikeStatus"]["row"]:
        bike_dict["rackTotCnt"].append(int(row["rackTotCnt"]))
        bike_dict["stationName"].append(row["stationName"])
        bike_dict["parkingBikeTotCnt"].append(int(row["parkingBikeTotCnt"]))
        bike_dict["shared"].append(int(row["shared"]))
        bike_dict["latitude"].append(float(row["stationLatitude"]))
        bike_dict["longitude"].append(float(row["stationLongitude"]))
    if len(result["rentBikeStatus"]["row"]) != 1000:
        break
    num += 1

df = pd.DataFrame(bike_dict)
st.write(df)

# 지도 시각화
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position=["longitude", "latitude"], # 잘 적어줘야한다고함
    get_fill_color=["255","255-shared","255-shared"],# 색깔이라고 보면됨 255 255 255 은 흰색나올꺼임 아마
    get_radius="60*shared/100",
    pickable=True # 마우스제어 컨트롤
)

# 서울시 중심 좌표값 구하기
lat_center = df["latitude"].mean()
lon_center = df["longitude"].mean()
# 카메라를 하나 만들건데
initial_camera = pdk.ViewState(latitude=lat_center, longitude=lon_center, zoom= 10) # 카메라 확대는 10이 깔끔하다

map = pdk.Deck(initial_view_state=initial_camera, layers=[layer], tooltip={"text":"대여소 : {stationName}\n현재 주차 대수 : {parkingBikeTotCnt}"})
# stationNAme은 데이터 헤드라고 보면됨
# 원래 지도 함수를 제대로 쓸려면 map.show() 나 map.to_html() 을 써야하는데
# st.pydeck_chart(map) 호환
st.pydeck_chart(map)

# 위에 대로하면 서울이 중심이 나는게 아니라 전국지도가 뜸
# 그래서 서울만 뜨게 만들려면 구글에서 검색해서 하는것도 좋지만
# 강사의 경우 모든 지표의 평균을 구해서 하는걸루 함
