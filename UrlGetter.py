import requests
from bs4 import BeautifulSoup
from AbcScraper import AbcScraper
import os


class UrlGetter(AbcScraper):
    def __init__(self) -> None:
        super().__init__()

    def get_films(self, films_txt):
        films = []
        with open(films_txt, "r", encoding="utf-8") as f:
            films = [item.lower().strip() for item in f.readlines()]
        return films

    def get_url(self, film_name):
        film_name = film_name.replace(" ", "+")
        url = f"https://www.google.cz/search?q={film_name}+csfd"
        s = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Cookie": "euconsent-v2=CPtCwQAPtCwQAAHABBENDHCgAP_AAEPAAATII2IBJC5kBSFCAGJoYtkQIAAGxxAAICACABAAgAAAABoAIAwAAAAwAAQABAAAABAAIEIAAABACEBAAAAAQAAAAQAAAEAQAAAAIQIAAAAAAiBACAAAAABAAAAAAABAQAAAgAAAAAIAQAAAAAEAgAAAAAAAAAAABBAAAQgAAAAAAAAAAAAAAAAAAAAAAAAAABBA1OBUABUAC4AGQAOAAgABkADQAHMARABFACYAE8AKoAXAAxABmADaAH4AQkAiACJAEcAKUAWIAywBmwDuAO8AfsBBwEIAIsASYAuoBgQDWAG0AOoAkEBNoC1AFuALzAZIA0oBqYAgaADAAEEvBEAGAAIJeCoAMAAQS8GQAYAAgl4A.f_gACHgAAAAA; __gfp_64b=C_t3IReX0vcf6xtULGnbX9BieqDMmqYIhqHr_erZ3nX.V7^|1686247087; _ga=GA1.1.1743777893.1686304508; mid=10887570730085911055; _tz_d=RXVyb3BlL1ByYWd1ZTo3OC44MC45Ni4xNTU^%^3D; cto_bundle=ZRJgqF9mekJtU3NhYlBsQ2hTTVpZMGlvd3M0UllnTXpsOTg2QU1YeU9Mcm9nN1EyNmN2JTJGSE93ZnhhQUxJRXhjZ1glMkZFUFBDcnFCWFg3MjR4RzlibElqSmwwMmEzZHMzblBmJTJGVmx0OXVtZ2R0UHglMkZKUnluTHNOaUFqVldBOU00bE1JbElIUTVMdHJVeDUyMGgyR3lxZmtzJTJGbndnJTNEJTNE; hdyuz48=7; __gads=ID=6abcc17ccd102159-2269b30355e1008a:T=1686304511:RT=1686468297:S=ALNI_MahPoXM8b4DL79Qtpikg7HDOL5tLQ; __gpi=UID=00000c45f7ce3d64:T=1686304511:RT=1686468297:S=ALNI_MYoZP4deS3HZHPGwB4CV41nIIHZ3g; _ga_C98FX2HV16=GS1.1.1686468279.4.1.1686468347.57.0.0; _ga_CD0K5K18SG=GS1.1.1686468279.4.1.1686468347.60.0.0",
        }
        s.headers = headers
        html = s.get(url)
        print(html.status_code)
        if html.status_code == 200:
            soup = BeautifulSoup(html.content, "html.parser")
            link_elements = soup.find_all("a", href=True)
            for link in link_elements:
                if "www.csfd.cz" in link["href"]:
                    return link["href"]
            return None
        return None

    def get_all_data(self, films_list):
        for film in films_list:
            url = self.get_url(film)
            if url:
                self.output.update({film: url})
            else:
                self.failed.append(film)
        return True

    def save_results(self, output_csv):
        if os.path.exists(output_csv):
            with open(output_csv, "a", encoding="utf-8") as f:
                for key, value in self.output.items():
                    f.write(f"{key},{value}\n")
        else:
            with open(output_csv, "w", encoding="utf-8") as f:
                f.write("Název,Odkaz\n")
                for key, value in self.output.items():
                    f.write(f"{key},{value}\n")

        with open("failed/failed.txt", "w", encoding="utf-8") as f:
            for item in self.failed:
                f.write(item)
                f.write("\n")
