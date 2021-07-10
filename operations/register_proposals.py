import json
import time
from argparse import ArgumentParser
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import jsonlines


def create_api_post_func(api_root, api_token):
    api_url = urljoin(api_root, "api/v1/proposals/")
    headers = {
        "Authorization": f"Token {api_token}",
        "Content-type": "application/json",
    }

    def wrapper(data):
        time.sleep(0.5)
        request = Request(api_url, json.dumps(data).encode(), headers)
        try:
            with urlopen(request) as response:
                result = json.loads(response.read())
        except HTTPError as e:
            return {
                "result": False,
                "sessionize_id": data["sessionize_id"],
                "error": str(e),
                "detail": e.read().decode(),
            }
        return {"result": True, "sessionize_id": result["sessionize_id"]}

    return wrapper


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input", help="JSON lines file as proposal data")
    parser.add_argument("output", help="JSON lines file to be written results")
    parser.add_argument("api_root")
    parser.add_argument("api_token")
    args = parser.parse_args()

    api_post_func = create_api_post_func(args.api_root, args.api_token)

    with jsonlines.open(args.input) as reader, jsonlines.open(
        args.output, mode="w"
    ) as writer:
        writer.write_all(api_post_func(data) for data in reader)
