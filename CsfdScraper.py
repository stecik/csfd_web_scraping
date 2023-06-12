from bs4 import BeautifulSoup
import requests
import os


class CsfdScraper:
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

    def get_all_film_data(self, films_csv):
        scraped_data = dict()
        failed = dict()
        with open(films_csv, "r", encoding="utf-8") as f:
            file = f.readlines()
            for i in range(1, len(file)):
                film, link = list(map(str.strip, file[i].split(",")))
                curr_data = self.get_film_data(link)
                if curr_data:
                    rating, streaming = curr_data
                    data = (rating, streaming, link)
                    scraped_data.update({film: data})
                else:
                    failed.update({film: link})

        output_csv = "scraped_data.csv"

        if os.path.exists(output_csv):
            with open(output_csv, "a", encoding="utf-8") as f:
                for key, value in scraped_data.items():
                    f.write(f"{key},{value[0]},{value[1]},{value[2]}\n")
        else:
            with open(output_csv, "w", encoding="utf-8") as f:
                f.write("Název,Rating,Streaming,Odkaz\n")
                for key, value in scraped_data.items():
                    f.write(
                        f"{key},{value[0]},{value[1] if value[1] else None},{value[2]}\n"
                    )

        with open("failed.csv", "w", encoding="utf-8") as f:
            f.write("Název,Odkaz\n")
            for key, value in failed.items():
                f.write(f"{key},{value}\n")
