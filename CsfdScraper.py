from AbcScraper import AbcScraper
from bs4 import BeautifulSoup
import requests
import os


# This class takes in a csv file with film names and links to csfd for those films
# and returns a csv with a name, rating, available streaming and link
class CsfdScraper(AbcScraper):
    def __init__(self) -> None:
        super().__init__()

    # This method gets a list of available streaming services from a file.
    def get_available_streaming(self, list_name):
        available = []
        with open(list_name, "r", encoding="utf-8") as f:
            available = [item.lower().strip() for item in f.readlines()]
        return available

    # This method gets the data for a film from the CSFD website.
    def get_film_data(self, url):
        s = requests.Session()
        # Set user-agent string
        headers = {
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        s.headers = headers
        # Create get request
        html = s.get(url)
        # Get the list of available streaming services.
        available_straming = self.get_available_streaming("available_streaming.txt")
        print(html.status_code)
        if html.status_code == 200:
            soup = BeautifulSoup(html.content, "html.parser")
            # Get the rating of the film.
            try:
                rating = (
                    soup.find("div", class_="film-rating-average").get_text().strip()
                )
                rating = rating.replace("%", "")
            except:
                raiting = None
            # Get the list of streaming services for the film.
            streaming_services_list = []
            try:
                streaming_div = soup.find("div", class_="box-film-vod-services")
                streaming_services = streaming_div.find_all("div", class_="vod-item")
                for item in streaming_services:
                    item = item.get_text().strip().lower()
                    if item in available_straming:
                        # Append available streaming services
                        streaming_services_list.append(item)
            except:
                streaming_services_list = []
            return (rating, streaming_services_list)
        return None

    # This method gets a list of films from a CSV file.
    def get_films(self, films_csv):
        films_list = []
        with open(films_csv, "r", encoding="utf-8") as f:
            file = f.readlines()
            for i in range(1, len(file)):
                film, link = list(map(str.strip, file[i].split(",")))
                films_list.append((film, link))
        return films_list

    # This method gets all of the data for the films in a list.
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

    # Converts list to plain text, replaces , with ;
    def _streaming_to_text(self, streaming):
        if streaming:
            streaming = str(streaming)
            streaming = streaming.replace("[", "")
            streaming = streaming.replace("]", "")
            streaming = streaming.replace("'", "")
            streaming = streaming.replace(",", ";")
            return streaming
        return None

    # Save results into csv file
    def save_results(self, output_csv):
        if os.path.exists(output_csv):
            with open(output_csv, "a", encoding="utf-8") as f:
                for key, value in self.output.items():
                    f.write(
                        f"{key},{value[0]},{self._streaming_to_text(value[1])},{value[2]}\n"
                    )
        else:
            with open(output_csv, "w", encoding="utf-8") as f:
                f.write("Název,Rating,Streaming,Odkaz\n")
                for key, value in self.output.items():
                    f.write(
                        f"{key},{value[0]},{self._streaming_to_text(value[1])},{value[2]}\n"
                    )

        # failed.csv contains list of films with corresponding links which failed due to an error
        # (probably 429 - to many requests). In that case use a proxy or vpn and feed the failed
        # file back to the execute method.
        with open("failed/failed.csv", "w", encoding="utf-8") as f:
            f.write("Název,Odkaz\n")
            for film in self.failed:
                f.write(f"{film[0]},{film[1]}\n")
