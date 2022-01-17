#!/usr/local/bin/python3.7
"""
After account is created send welcome message
"""
from formulas.opensea import login, add_image, goto_add_image
from libs.scraper import Scraper
from time import sleep
from json import load, dumps
from os import listdir
from os.path import exists, isfile, join
import logging

# logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger("nft-lazy-minter")
log.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


# share single browser instance
session_id = "44bfca271f3c68211d35bd34ed5b6def"
executor_url = "http://localhost:51803"
scraper = Scraper(session_id=session_id, executor_url=executor_url)
pivot_file = "/tmp/nftuploader-pivot.txt"

collection_name = ""   # add the name of your collection
collection_description = ""  # add a description that's used for each nft

def gather_nft_info():
    root = (
        "/Users/meetri/Documents/mystuff"
    )

    output = []
    metadata = load(open(join(root, "metadata.json")))
    for ref in metadata:
        f = f"{ref}.png"
        fn = join(root, f)
        if isfile(fn):
            attr = metadata[ref]["attributes"]
            output.append({
                "properties": attr,
                "name": f"{collection_name} #{int(ref)+1}",
                "description": collection_description,
                "filename": join(root, f)
            })

    return output


def lazy_mint(data):
    goto_add_image(scraper)
    add_image(
        scraper, item_name=data["name"], filename=data["filename"],
        item_description=data["description"], properties=data["properties"]
    )



def load_pivot():
    start = 0
    if exists(pivot_file):
        with open(pivot_file, "r") as pf:
            start = int(pf.read())
    return start


def save_pivot(val):
    with open(pivot_file, "w") as pf:
        pf.write(f"{val}")


MAX_RETRIES = 5

if __name__ == "__main__":
    start = load_pivot()
    log.info(f"Starting NFT Uploader at index: {start}")
    nft_data = gather_nft_info()
    login(scraper)

    for idx, data in enumerate(nft_data[start:]):
        retries = 0
        done = False
        while not done:
            try:
                log.info(f"Working on {data['name']}/{idx+start}")
                save_pivot(idx+start)
                lazy_mint(data)
                retries = 0
                done = True
            except Exception as ex:
                if retries < MAX_RETRIES:
                    log.warning("Sleeping for 60 seconds before retry")
                    retries += 1
                    sleep(60)
                    login(scraper)
                    done = True
                else:
                    raise(ex)




