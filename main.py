from UrlGetter import UrlGetter
from CsfdScraper import CsfdScraper
from datetime import datetime

if __name__ == "__main__":
    start = datetime.timestamp(datetime.now())
    url_getter = UrlGetter()
    url_getter.execute(10, "inputs/seen.txt", "outputs/seen.csv")
    csfd_scraper = CsfdScraper()
    csfd_scraper.execute(500, "outputs/seen.csv", "outputs/final_seen.csv")
    stop = datetime.timestamp(datetime.now())
    print(f"Task finished in {stop - start}s")
