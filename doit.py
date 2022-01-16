#!/usr/local/bin/python3.7
"""
After account is created send welcome message
"""
from formulas.opensea import login, add_image, goto_add_image
from libs.scraper import Scraper
from time import sleep

# share single browser instance
session_id = "2ca8d10ae5638d5108a342877f9db07d"
executor_url = "http://localhost:60225"

def main():
    scraper = Scraper(session_id=session_id, executor_url=executor_url)
    print("logging in")
    res = login(scraper)

    print("go to add to collection")
    res = goto_add_image(scraper)

    print("add png to collection")
    res = add_image(
        scraper, item_name="Sigi Pattern", filename="/tmp/sigi.png",
        item_description="out of this world"
    )
    print(res)
    print("go back to add to collection")
    res = goto_add_image(scraper)


if __name__ == "__main__":
    main()
