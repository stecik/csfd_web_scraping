from AbcScraper import AbcScraper
from bs4 import BeautifulSoup
import requests
import os


class CsfdScraper(AbcScraper):
    def __init__(self) -> None:
        super().__init__()

    def get_available_streaming(self, list_name):
        available = []
        with open(list_name, "r", encoding="utf-8") as f:
            available = [item.lower().strip() for item in f.readlines()]
        return available

    def get_film_data(self, url):
        s = requests.Session()
        headers = {
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        s.headers = headers
        html = s.get(url)
        available_straming = self.get_available_streaming("available_streaming.txt")
        if html.status_code == 200:
            soup = BeautifulSoup(html.content, "html.parser")
            # get rating
            try:
                rating = (
                    soup.find("div", class_="film-rating-average").get_text().strip()
                )
                rating = rating.replace("%", "")
            except:
                raiting = None
            # get streaming services
            streaming_services_list = []
            try:
                streaming_div = soup.find("div", class_="box-film-vod-services")
                streaming_services = streaming_div.find_all("div", class_="vod-item")
                for item in streaming_services:
                    item = item.get_text().strip().lower()
                    if item in available_straming:
                        streaming_services_list.append(item)
            except:
                streaming_services_list = []
            return (rating, streaming_services_list)
        return None

    def get_films(self, films_csv):
        films_list = []
        with open(films_csv, "r", encoding="utf-8") as f:
            file = f.readlines()
            for i in range(1, len(file)):
                film, link = list(map(str.strip, file[i].split(",")))
                films_list.append((film, link))
        return films_list

    def get_all_data(self, films_list):
        for item in films_list:
            film = item[0]
            link = item[1]
            curr_data = self.get_film_data(link)
            if curr_data:
                rating, streaming = curr_data
                data = (rating, streaming, link)
                self.output.update({film: data})
            else:
                self.failed.append((film, link))
        return True

    def save_results(self, output_csv):
        if os.path.exists(output_csv):
            with open(output_csv, "a", encoding="utf-8") as f:
                for key, value in self.output.items():
                    f.write(f"{key},{value[0]},{value[1]},{value[2]}\n")
        else:
            with open(output_csv, "w", encoding="utf-8") as f:
                f.write("Název,Rating,Streaming,Odkaz\n")
                for key, value in self.output.items():
                    f.write(
                        f"{key},{value[0]},{value[1] if value[1] else None},{value[2]}\n"
                    )
        with open("failed/failed.csv", "w", encoding="utf-8") as f:
            f.write("Název,Odkaz\n")
            for film in self.failed:
                f.write(f"{film[0]},{film[1]}\n")
