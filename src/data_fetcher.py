

import pandas as pd
import os
import time
import requests
from tqdm import tqdm
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


df_train = pd.read_csv(ROOT_DIR/"data"/"raw"/'train(1).csv',usecols=["id","lat","long"])
df_train





MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
if MAPBOX_TOKEN is None:
    raise ValueError("MAPBOX_TOKEN environment variable not set") 


IMAGE_SIZE = "256x256"     
ZOOM = 18                 
STYLE = "satellite-v9"     



SAVE_DIR = ROOT_DIR / "data" / "images" / "train"

SAVE_DIR.mkdir(parents=True, exist_ok=True)
def get_mapbox_center_url(lat, lon):
    return (
        f"https://api.mapbox.com/styles/v1/mapbox/{STYLE}/static/"
        f"{lon},{lat},{ZOOM}/"
        f"{IMAGE_SIZE}"
        f"?access_token={MAPBOX_TOKEN}"
    )





image_paths = []

for _, row in tqdm(df.iterrows(), total=len(df)):
    lat = row["lat"]
    lon = row["long"]
    pid = row["id"]

    url = get_mapbox_center_url(lat, lon)
    out_path = SAVE_DIR / f"{pid}.jpeg"


    if out_path.exists():
        image_paths.append(str(out_path))
        continue

    try:
        r = requests.get(url, timeout=10)

        if r.status_code == 200 and "image" in r.headers.get("Content-Type", ""):
            with open(out_path, "wb") as f:
                f.write(r.content)
            image_paths.append(str(out_path))
        else:
            image_paths.append(None)

    except Exception as e:
        image_paths.append(None)

    time.sleep(0.05)  






df_test=pd.read_csv(ROOT_DIR/"data"/"raw"/'test2.csv',usecols=['id','lat','long'])
df_test





MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
if MAPBOX_TOKEN is None:
    raise RuntimeError("MAPBOX_TOKEN environment variable not set")

IMAGE_SIZE = "256x256"
ZOOM = 18
STYLE = "satellite-v9"


SAVE_DIR1 = ROOT_DIR / "data" / "images" / "test"
SAVE_DIR1.mkdir(parents=True, exist_ok=True)

def get_mapbox_center_url(lat, lon):
    return (
        f"https://api.mapbox.com/styles/v1/mapbox/{STYLE}/static/"
        f"{lon},{lat},{ZOOM}/"
        f"{IMAGE_SIZE}"
        f"?access_token={MAPBOX_TOKEN}"
    )





def download_test_images(df):
    saved = 0
    failed = 0

    for _, row in tqdm(df.iterrows(), total=len(df)):
        lat = row["lat"]
        lon = row["long"]
        pid = row["id"]

        out_path = SAVE_DIR1 / f"{pid}.jpeg"


        if out_path.exists():
            saved += 1
            continue

        try:
            r = requests.get(get_mapbox_center_url(lat, lon), timeout=10)

            if r.status_code == 200 and "image" in r.headers.get("Content-Type", ""):
                with open(out_path, "wb") as f:
                    f.write(r.content)
                saved += 1
            else:
                failed += 1

        except Exception:
            failed += 1

        time.sleep(0.05)

    print("Saved:", saved)
    print("Failed:", failed)

