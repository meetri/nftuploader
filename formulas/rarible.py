from selenium.webdriver.common.keys import Keys

def add_image(scraper):
    formula = [
        {
            "action": "waitclickable_xpath",
            "element": '//a[contains(text(),"My profile")]'
        },
        {
            "action": "get",
            "url": "https://rarible.com/create/erc-721"
        },
        {
            "action": "waitclickable_xpath",
            "element": '//span[contains(text(),"Choose File")]'
        },
        {
            "action": "upload",
            "element": {
                "type": "name",
                "key": 'primary-attachment',
                "file": '/tmp/bgtile.png'
            }
        },
        {
            "action": "click",
            "element": {
                "type": "xpath",
                "key": '//span[contains(text(),"Open for bids")]'
            }
        },
        {
            "action": "send_keys",
            "element": {
                "type": "xpath",
                "key": '//input[@data-marker="root/appPage/create/form/nameInput"]'
            },
            "keys": "Hello Moon"
        },
        {
            "action": "send_keys",
            "element": {
                "type": "xpath",
                "key": '//textarea[@data-marker="root/appPage/create/form/descriptionInput"]',
            },
            "keys": "Hello Earth"
        },
        {
            "action": "send_keys",
            "element": {
                "type": "xpath",
                "key": '//input[@data-marker="root/appPage/create/form/royaltiesInput"]',
            },
            "keys": "15"
        },
        {
            "action": "click",
            "element": {
                "type": "xpath",
                "key": '//button[contains(text(),"Show advanced settings")]'
            }
        },
        {
            "action": "send_keys",
            "element": {
                "type": "xpath",
                "key": '//input[@placeholder="e.g. Size"]',
            },
            "keys": "abc"
        },
        {
            "action": "send_tab",
        },
        {
            "action": "send_keys_direct",
            "keys": "def"
        },
        {
            "action": "send_tab",
        },
        {
            "action": "send_keys_direct",
            "keys": "ghi"
        },
        {
            "action": "send_tab",
        },
        {
            "action": "send_keys_direct",
            "keys": "jkl"
        },
        {
            "action": "click",
            "element": {
                "type": "xpath",
                "key": '//button[contains(text(),"Create item")]'
            }
        },
    ]

    res = scraper.handle(formula)
    return res


def login(scraper):
    formula = [
        {
            "action": "get",
            "url": "https://rarible.com/connect"
        }
    ]

    res = scraper.handle(formula)
    return res
    # return res.text
