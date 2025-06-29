from configs import env_config
import pytest
import requests
import time
import logging

'''
設定Logger，以便debug時，可於終端機顯示資料
'''
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
# 建立一個輸出到主控台的Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
# 建立Formatter
formatter = logging.Formatter(
    '[%(asctime)s][%(name)s][%(levelname)s]_%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# 將Formatter加到Handler
console_handler.setFormatter(formatter)
# 將Handler加到Logger
logger.addHandler(console_handler)


@pytest.mark.parametrize("page_config", ["register"], indirect=True)
def test_open_register_page(chrome_browser, page_config):
    url = page_config["url"]
    chrome_browser.get(url)
    response = requests.get(url)
    logger.info(f"已開啟註冊頁面: {url}")

    # 檢查頁面是否開啟
    assert response.status_code == 200
    assert "ACY Securities Client Portal" in chrome_browser.title
    logger.info("註冊頁面開啟成功")
    
    
