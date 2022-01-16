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

# share single browser instance
session_id = "2ca8d10ae5638d5108a342877f9db07d"
executor_url = "http://localhost:60225"
scraper = Scraper(session_id=session_id, executor_url=executor_url)

collection_name = "Metamorphosis"
collection_description = "The process of Metamorphosis directly translates to the process of alchemizing thoughts, feelings, emotions, and beliefs in us humans. This collection is some visuals that tie into that story and also includes a aspect of the yin and yang thrown in."

def gather_nft_info():
    root = (
        "/Users/meetri/Documents/Adobe/"
        "Photoshop Cloud Associates/brookly's stuff/nft/output"
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

    goto_add_image(scraper)


if __name__ == "__main__":
    nft_data = gather_nft_info()
    login(scraper)
    for data in nft_data[0:5]:
        lazy_mint(data)
