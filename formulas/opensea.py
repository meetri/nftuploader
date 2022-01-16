from os import path
import json
from selenium.webdriver.common.keys import Keys


def xadd_image(
    scraper, collection="metamorphosis-butterfly",
    item_name="Shera", item_description="bla bla bla"
):

    driver = scraper.driver

    if path.exists("/tmp/cookies.json"):
        with open("/tmp/cookies.json", "r") as inf:
            cookies = json.loads(inf.read())
            for cookie in cookies:
                driver.add_cookie(cookie)

    driver.get(
        f"https://opensea.io/collection/{collection}/assets/create")

    cookies = driver.get_cookies()
    with open("/tmp/cookies.json", "w") as inf:
        inf.write(json.dumps(cookies))
        # print(cookies)


def goto_add_image(
    scraper, collection="metamorphosis-butterfly"
):

    formula = [
        {
            "action": "moveto",
            "element": {
                "type": "xpath",
                "key": '//img[@alt="Account"]'
            }
        },
        {
            "action": "click",
            "element": {
                "type": "xpath",
                "key": '//span[contains(text(), "My Collections")]'
            }
        },
        {"action": "sleep", "value": 1},
        {
            "action": "click",
            "element": {
                "type": "xpath",
                "key": f'//a[@href="/collection/{collection}"]'
            }
        },
        {
            "action": "waitclickable_xpath",
            "element": '//a[contains(text(), "Add item")]'
        },
        {
            "action": "click",
            "element": {
                "type": "xpath",
                "key": '//a[contains(text(), "Add item")]'
            }
        },
        {
            "action": "waitclickable_xpath",
            "element": '//input[@placeholder="Item name"]'
        },
    ]

    res = scraper.handle(formula)
    return res


def add_image(
    scraper, collection="metamorphosis-butterfly",
    item_name="Moshy", item_description="bla bla bla",
    filename="/tmp/bgtile.png", properties=[]
):

    formula = [
        {
            "action": "waitclickable_xpath",
            "element": '//input[@placeholder="Item name"]'
        },
        {
            "action": "upload",
            "element": {
                "type": "xpath",
                "key": '//input[@accept="image/*,video/*,audio/*,webgl/*,.glb,.gltf"]',
                "file": filename
            }
        },
        {
            "action": "send_keys",
            "element": {
                "type": "xpath",
                "key": '//input[@placeholder="Item name"]'
            },
            "keys": item_name
        },
        {
            "action": "send_keys",
            "element": {
                "type": "xpath",
                "key": '//textarea[@name="description"]'
            },
            "keys": item_description
        },
    ]

    res = scraper.handle(formula)

    if len(properties) > 0:
        scraper.handle([
            {
                "action": "click.perform",
                "element": {
                    "type": "xpath",
                    "key": '//button[contains(@aria-label, "Add properties")]'
                }
            }
        ])

        for prop in properties:
            res = scraper.handle([
                {
                    "action": "wait",
                    "element": {
                        "type": "xpath",
                        "key": '//button[contains(text(), "Add more")]',
                    }
                },
                {
                    "action": "click",
                    "element": {
                        "type": "xpath",
                        "key": '//button[contains(text(), "Add more")]',
                    }
                },
            ])

        res = scraper.handle([
            {
                "action": "click",
                "element": {
                    "type": "xpath",
                    "key": '//input[@placeholder="Character"]',
                }
            },
        ])

        for prop in properties:
            res = scraper.handle([
                {
                    "action": "send_keys_direct",
                    "keys": prop["trait_type"]
                },
                {
                    "action": "send_tab",
                },
                {
                    "action": "send_keys_direct",
                    "keys": prop["value"]
                },
                {
                    "action": "send_tab",
                },
            ])

        res = scraper.handle([
            {
                "action": "click",
                "element": {
                    "type": "xpath",
                    "key": '//button[contains(text(), "Save")]',
                }
            },
            {
                "action": "scroll_bottom"
            },
            {
                "action": "sleep", "value": 1
            },
            {
                "action": "click",
                "element": {
                    "type": "xpath",
                    "key": '//button[contains(text(), "Create")]',
                }
            },
            {
                "action": "waitclickable_xpath",
                "element": '//i[contains(@aria-label, "Close")]'
            },
            {
                "action": "click",
                "element": {
                    "type": "xpath",
                    "key": '//i[contains(@aria-label, "Close")]',
                }
            },
        ])

    return res


def login(scraper, collection="metamorphosis-butterfly"):
    formula = [
        {
            "action": "get",
            "url": "https://opensea.io/login"
        },
        {
            "action": "waitclickable_xpath",
            "element": '//span[contains(text(),"WalletConnect")]'
        },
        {
            "action": "click.perform",
            "element": {
                "type": "xpath",
                "key": '//span[contains(text(), "WalletConnect")]'
            }
        },
        {
            "action": "wait",
            "element": {
                "type": "xpath",
                "key": '//span[contains(text(), "Collected")]'
            }
        },
        {
            "action": "moveto",
            "element": {
                "type": "xpath",
                "key": '//img[@alt="Account"]'
            }
        },
        {
            "action": "click",
            "element": {
                "type": "xpath",
                "key": '//span[contains(text(), "My Collections")]'
            }
        },
    ]

    res = scraper.handle(formula)
    return res
    # return res.text
