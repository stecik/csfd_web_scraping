from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor


# This method is an abstract method for a web scraper.
# It defines the execute and divide_into_threads methods.
class AbcScraper(ABC):
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        self.failed = []
        self.output = dict()

    @abstractmethod
    def save_results(self, output_csv):
        pass

    @abstractmethod
    def get_all_data(self, film_list):
        pass

    @abstractmethod
    def get_films(self, input_file):
        pass

    # This function divides a list into chunks so it can be processed using threading.
    def divide_into_threads(self, number_of_threads, films_list):
        films_len = len(films_list)
        part = films_len // number_of_threads
        mod = films_len % number_of_threads
        parts = []
        for i in range(0, films_len - mod, part):
            parts.append(films_list[i : (i + part)])
        for i in range(-1, -mod - 1, -1):
            parts[i].append(films_list[i])
        return parts

    # This function executes the function get_all_data for a list of films
    # threds specifies a number of threads whitch are being executed at once
    def execute(self, threads, input_file, output_csv):
        films = self.get_films(input_file)
        number_of_threads = min(threads, len(films))
        with ThreadPoolExecutor() as executor:
            divided_list = self.divide_into_threads(number_of_threads, films)
            results = [
                executor.submit(self.get_all_data, divided_list[x])
                for x in range(len(divided_list))
            ]
        self.save_results(output_csv)
