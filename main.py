from bs4 import BeautifulSoup
import requests


def get_available_streaming(list_name):
    available = []
    with open(list_name, "r", encoding="utf-8") as f:
        available = [item.lower().strip() for item in f.readlines()]
    return available


def get_film_data(url):
    s = requests.Session()
    headers = {
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    s.headers = headers
    html = s.get(url)
    available_straming = get_available_streaming("available_streaming.txt")
    if html.status_code == 200:
        soup = BeautifulSoup(html.content, "html.parser")
        # get rating
        rating = soup.find("div", class_="film-rating-average").get_text().strip()
        # get streaming services
        streaming_div = soup.find("div", class_="box-film-vod-services")
        streaming_services = streaming_div.find_all("div", class_="vod-item")
        streaming_services_list = []
        for item in streaming_services:
            item = item.get_text().strip().lower()
            if item in available_straming:
                streaming_services_list.append(item)

        return (rating, streaming_services_list)
    else:
        return None


url = "https://www.csfd.cz/film/1626-harry-potter-a-kamen-mudrcu/prehled/"
data = get_film_data(url)
print(data)
