import json
from argparse import ArgumentParser
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import jsonlines

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("api_root")
    parser.add_argument("api_token")
    parser.add_argument("output", help="JSON lines file to be written scores")
    args = parser.parse_args()

    api_url = urljoin(args.api_root, "api/v1/proposals/scores")
    headers = {
        "Authorization": f"Token {args.api_token}",
        "Content-type": "application/json",
    }
    request = Request(api_url, headers=headers)
    with urlopen(request) as response:
        results = json.loads(response.read())

    with jsonlines.open(args.output, "w") as writer:
        writer.write_all(results)
