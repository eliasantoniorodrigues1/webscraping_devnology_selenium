import requests
from service import Service
import json

if __name__ == '__main__':
    url = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'
    api_url = 'http://127.0.0.1:5000/products'
    query = 'lenovo'

    # Collecting data:
    service = Service()
    data_list = service.get_data_webscraper_io(url, query)

    for item in data_list:
        # Inserting data collected:
        headers = {'content-type': 'application/json'}
        response = requests.post(
            api_url, data=json.dumps(item), headers=headers)

    # Retriving data:
    # Está apresentando erro ainda
    # response = requests.get(api_url + '/1')
    # print(response.json())

