#!/usr/local/bin/python3.7
"""
After account is created send welcome message
"""
from formulas.opensea import login, add_image
from libs.scraper import Scraper
from time import sleep


def main():
    scraper = Scraper()
    print(
        f"session_id: {scraper.session_id}, "
        f"executor_url: {scraper.executor_url}"
    )

    while True:
        sleep(5)


if __name__ == "__main__":
    main()
