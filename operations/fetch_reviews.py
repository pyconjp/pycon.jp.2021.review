from argparse import ArgumentParser
from urllib.parse import urljoin

import jsonlines
import requests

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("output", help="JSON lines file to be written reviews")
    parser.add_argument("api_root")
    parser.add_argument("api_token")
    args = parser.parse_args()

    api_url = urljoin(args.api_root, "api/v1/reviews/")

    with requests.Session() as s, jsonlines.open(
        args.output, mode="w"
    ) as writer:
        s.headers.update(
            {
                "Content-type": "application/json",
                "Authorization": f"Token {args.api_token}",
            }
        )

        while True:
            print(f"Call {api_url}")
            r = s.get(api_url)
            response = r.json()
            writer.write_all(response["results"])
            if not (api_url := response["next"]):
                break
