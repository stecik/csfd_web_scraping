from UrlGetter import UrlGetter
from CsfdScraper import CsfdScraper
from datetime import datetime

if __name__ == "__main__":
    start = datetime.timestamp(datetime.now())

    # Get csfd urls
    try:
        print("Getting urls...")
        url_getter = UrlGetter()
        url_getter.execute(50, "inputs/serialy.txt", "outputs/serialy.csv")
    except Exception as e:
        print(e)

    # get rating and straming services
    try:
        print("Scraping data...")
        csfd_scraper = CsfdScraper()
        csfd_scraper.execute(500, "outputs/serialy.csv", "outputs/final_serialy.csv")
    except Exception as e:
        print(e)

    stop = datetime.timestamp(datetime.now())
    print(f"Task finished in {stop - start}s")
