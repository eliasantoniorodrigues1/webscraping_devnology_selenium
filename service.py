from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from operator import itemgetter
import traceback
import json
import re


class Service:
    def get_data_webscraper_io(self, url: str, query: str):
        # Headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        with webdriver.Chrome(chrome_options=chrome_options) as driver:
            try:
                driver.get(url)
                self.products = driver.find_elements_by_class_name("thumbnail")
                self.data = []
                for product in self.products:
                    self.title = product.find_element(
                        By.CSS_SELECTOR, value='a.title').text
                    self.price = product.find_element(
                        By.CSS_SELECTOR, value='h4.pull-right.price').text
                    if query in self.title.lower():
                        # Product Data:
                        notebook = {
                            "title": self.title[:-3],
                            "price": self.remove_sinais_monetarios(self.price),
                            "description": product.find_element(By.CSS_SELECTOR, value='p.description').text,
                            "review": product.find_element(By.CSS_SELECTOR, value='p.pull-right').text,
                            "rating": ''
                        }
                        self.data.append(notebook.copy())
                        notebook.clear()

                return self.sort_list(self.data)

            except Exception:
                traceback.print_exc()
                return None

    def remove_sinais_monetarios(self, string: str):
        string = re.sub(r'[^0-9.,]', '', string)
        try:
            valor = float(string)
        except Exception:
            valor = float(string.replace(',', '.'))

        return valor

    @staticmethod
    def sort_list(product_list: list):
        product_list = sorted(
            product_list, key=itemgetter('price'), reverse=False)

        # json_string = json.dumps(product_list, indent=4)
        return product_list
