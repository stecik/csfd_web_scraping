from UrlGetter import UrlGetter
import os
import concurrent.futures


if __name__ == "__main__":
    url_getter = UrlGetter()
    films = url_getter.get_films("new.txt")
    number_of_threads = min(900, len(films))
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        divided_list = url_getter.divide_into_threads(number_of_threads, films)
        results = [
            executor.submit(url_getter.get_all_urls, divided_list[x])
            for x in range(len(divided_list))
        ]

    url_file = "urls_new.csv"
    if os.path.exists(url_file):
        with open(url_file, "a", encoding="utf-8") as f:
            for key, value in url_getter.urls.items():
                f.write(f"{key}, {value}\n")
    else:
        with open(url_file, "w", encoding="utf-8") as f:
            f.write("Název,Odkaz\n")
            for key, value in url_getter.urls.items():
                f.write(f"{key}, {value}\n")

    with open("failed.txt", "w", encoding="utf-8") as f:
        for item in url_getter.failed:
            f.write(item)
            f.write("\n")

    print("finished")
