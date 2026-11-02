import argparse
import requests
parser = argparse.ArgumentParser()
parser.add_argument("--server-url", default="https://demo.borealisdata.ca")
parser.add_argument("--doi", default="doi:10.80240/FK2/KRFTCT")
parser.add_argument("--out", default="dataset.zip")
parser.add_argument("--api-token")
args = parser.parse_args()

headers = {"X-Dataverse-key": args.api_token} if args.api_token else {}

r = requests.get(
    f"{args.server_url}/api/access/dataset/:persistentId/",
    params={"persistentId": args.doi, "format": "original"},
    headers=headers,
    stream=True,
)
r.raise_for_status()

with open(args.out, "wb") as f:
    for chunk in r.iter_content(chunk_size=1024 * 1024):
        f.write(chunk)

