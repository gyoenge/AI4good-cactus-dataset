from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import base64
import time
import os
import uuid


def download_google_images(fileroot, search_query, num_images, color_filter=None):
    folder_name = search_query.replace(" ", "")
    directory = os.path.join(fileroot, folder_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 색상 필터링 파라미터 설정
    # color_param = f"&tbs=ic:{color_filter}" if color_filter else ""
    # search_url = f"https://www.google.com/search?q={search_query}&tbm=isch{color_param}"

    # 색상, 유형, 크기 필터링 파라미터 설정
    filters = []
    if color_filter:
        filters.append(f"ic:{color_filter}")
    filters.append("itp:lineart")
    filters.append("isz:m")
    filter_param = ",".join(filters)
    search_url = f"https://www.google.com/search?q={search_query}&tbm=isch&tbs={filter_param}"

    driver = webdriver.Chrome(
        'C:/Users/User/chromedriver-win64/chromedriver.exe')
    driver.get(search_url)

    for _ in range(10):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        # 중간중간 수동으로 더보기 버튼 클릭 필요

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    img_tags = soup.find_all("img", class_="rg_i")

    for i, img in enumerate(img_tags[:num_images]):
        try:
            img_url = img.get('src')
            if img_url.startswith('http'):
                img_data = requests.get(img_url).content
            else:
                img_data = base64.b64decode(img_url.split(",")[1])
            file_name = f"{uuid.uuid4()}.jpg"
            with open(os.path.join(directory, file_name), 'wb') as handler:
                handler.write(img_data)
        except Exception as e:
            print(f"Failed to download image : {e}")

    driver.close()


if __name__ == '__main__':
    # 저장 위치, 다운 이미지 수 수정
    IMG_ROOT_FOLDER = "dataset/info_visual_lineartfiltering/"
    IMG_SET_NUM = 500

    # 예시 검색어 목록
    search_queries = [
        'Map', 'Line Graph', 'Bar Chart', 'Pie Chart', 'Triangle Chart',
        'Exploded Chart', 'Flow Chart', 'Hierarchy Chart', 'Radial Chart', 'Pareto Chart',
        'Bubble Chart', 'Stacked Chart', 'Jagged Graph', 'Donut Chart', 'Wave Chart',
        'Venn Diagram', 'Scatter Plot', 'Spider Chart', 'Project Timeline', 'Star Graph',
        'Mind Map', 'Population Pyramids', 'Ring Charts', 'Sankey Plots', 'Area Charts'
    ]

    for query in search_queries:
        print(f"Downloading images for {query}...")
        download_google_images(IMG_ROOT_FOLDER, query, IMG_SET_NUM)
