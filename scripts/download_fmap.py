import os
import requests

BASE_URL      = "https://demo.borealisdata.ca"
PERSISTENT_ID = "doi:10.80240/FK2/KRFTCT"
OUTPUT_DIR    = "data"
API_TOKEN     = ""

headers = {"X-Dataverse-key": API_TOKEN} if API_TOKEN else {}

url = f"{BASE_URL}/api/datasets/:persistentId/versions/:latest/files"
files = requests.get(url, params={"persistentId": PERSISTENT_ID}, headers=headers).json()["data"]

for f in files:
    directory = f.get("directoryLabel", "")
    if "fmap" not in directory.lower():
        continue

    file_id   = f["dataFile"]["id"]
    filename  = f["dataFile"]["filename"]
    local_dir = os.path.join(OUTPUT_DIR, directory)
    local_path = os.path.join(local_dir, filename)

    os.makedirs(local_dir, exist_ok=True)
    resp = requests.get(f"{BASE_URL}/api/access/datafile/{file_id}", headers=headers, stream=True)
    with open(local_path, "wb") as fh:
        for chunk in resp.iter_content(chunk_size=8192):
            fh.write(chunk)
    print(local_path)
