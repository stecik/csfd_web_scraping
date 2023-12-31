# Web Scraping tool for https://www.csfd.cz/
## Description
Simple web scraper that takes a list of films and return a CSV file with film name, rating, streaming service, csfd url.
## How to install
Python 3 required
- Tested using version 3.10.9
- Should work with newer versions too

Install dependencies
```
pip install -r requirements.txt
```
## How to use
- In main.py edit the input and output files
- Edit the available_streaming.txt - add your streaming services (Netflix, Hbo Max...) _Note: It is necessary to use the exact name that [csfd](https://www.csfd.cz/) uses_ 
- UrlGetter() takes TXT file with film names (each on a new line) as an input and return a CSV file with film name and csfd url
- CsfdScraper() takes a CSV file generated by UrlGetter() and returns a CSV file with film name, rating, streaming service, csfd url
- Edit the number of threads you want to use (depends on how much data you have)
```
start = datetime.timestamp(datetime.now())

# Get csfd urls
try:
    print("Getting urls...")
    url_getter = UrlGetter()
    url_getter.execute(50, "inputs/serialy.txt", "outputs/serialy.csv")
except Exception as e:
    print(e)

# Get rating and straming services
try:
    print("Scraping data...")
    csfd_scraper = CsfdScraper()
    csfd_scraper.execute(500, "outputs/serialy.csv", "outputs/final_serialy.csv")
except Exception as e:
    print(e)

stop = datetime.timestamp(datetime.now())
print(f"Task finished in {stop - start}s")
```
## Error
- If your terminal is returning code 200, then everything is working
- If you get any other code (most probably 429) then use a proxy or vpn
- All films that failed due to and error are saved in failed/failed.txt (UrlGetter) or failed/failed.csv (CsfdScraper)
- You can simply feed the failed file as a new input and it will automatically add the new results to the output file
