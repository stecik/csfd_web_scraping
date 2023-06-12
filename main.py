from UrlGetter import UrlGetter
from CsfdScraper import CsfdScraper
from datetime import datetime

if __name__ == "__main__":
    start = datetime.timestamp(datetime.now())

    # try:
    #     print("Getting urls...")
    #     url_getter = UrlGetter()
    #     url_getter.execute(10, "inputs/seen.txt", "outputs/seen.csv")
    # except Exception as e:
    #     print(e)

    try:
        print("Scraping data...")
        csfd_scraper = CsfdScraper()
        csfd_scraper.execute(500, "outputs/new.csv", "outputs/final_new.csv")
    except Exception as e:
        print(e)

    stop = datetime.timestamp(datetime.now())
    print(f"Task finished in {stop - start}s")
