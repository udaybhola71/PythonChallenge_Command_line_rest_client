#!/usr/bin/env python

import argparse
import csv
import json
import requests


class RestfulClient:
    BASE_URL = 'https://jsonplaceholder.typicode.com'

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Simple command-line REST client for JSONPlaceholder')
        self.parser.add_argument('METHOD', choices=['get', 'post'], help='Request method')
        self.parser.add_argument('endpoint', help='Request endpoint URI fragment')
        self.parser.add_argument('-d', '--data', help='Data to send with request')
        self.parser.add_argument('-o', '--output', help='Output to .json or .csv file (default: dump to stdout)')

    def run(self):
        args = self.parser.parse_args()
        method = args.METHOD.lower()
        endpoint = args.endpoint
        output_file = args.output

        if method == 'get':
            response = self.get_request(endpoint)
        elif method == 'post':
            data = json.loads(args.data) if args.data else {}
            response = self.post_request(endpoint, data)

        self.handle_response(response, output_file)

    def get_request(self, endpoint):
        url = f"{self.BASE_URL}{endpoint}"
        return requests.get(url)

    def post_request(self, endpoint, data):
        url = f"{self.BASE_URL}{endpoint}"
        return requests.post(url, json=data)

    def handle_response(self, response, output_file):
        if response.status_code // 100 != 2:  # if code is b/w 200 to 299
            print(f"Error: HTTP Status Code {response.status_code}")
            exit(1)

        if output_file:
            if output_file.endswith('.json'):
                with open(output_file, 'w') as file:
                    json.dump(response.json(), file, indent=2)
            elif output_file.endswith('.csv'):
                self.write_to_csv(output_file, response.json())
            else:
                print(response.json())  # If file format not recognized, print to stdout
        else:
            print(response.json())

    def write_to_csv(self, output_file, data):
        keys = data[0].keys() if isinstance(data, list) and len(data) > 0 else []
        with open(output_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            if isinstance(data, list):
                writer.writerows(data)
            else:
                writer.writerow(data)


if __name__ == '__main__':
    client = RestfulClient()
    client.run()

# to use script in linux or git bash
# chmod +x restful.py (then use all commands)
# ./restful.py -h


