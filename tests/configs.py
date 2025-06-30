"""
結構如下：
env_config
└── 環境
    └── 頁面
        ├── url
        └── test_data
"""


env_config = {
    "prod": {
        "register": {
            "url": "http://www.acy.com/en/open-live-account",
            "test_data": {
                "valid_data":{
                    "country_of_residence": "Taiwan",
                    "country_code": "+886",
                    "first_name": "test",
                    "last_name": "testme",
                    "mobile_number": "+886 911222333",
                    "email_address": "test1234@gmail.com",
                    "create_password": "Lucky1234@"
                },
                "invalid_first_name": {
                    "country_of_residence": "Taiwan",
                    "first_name": "1234",  # 無效：姓名不能為數字
                    "last_name": "testme",
                    "country_code": "+886",
                    "mobile_number": "911222333",
                    "email_address": "test1234@gmail.com",
                    "create_password": "Lucky1234@"
                },
                "first_name_over_40_chars": {
                    "country_of_residence": "Taiwan",
                    "first_name": "testmetestmetestmetestmetestmetestmetestmetestme",  # 姓名不能超過40位
                    "last_name": "chiu",
                    "mobile_number": "+886 911222333",
                    "email_address": "test1234@gmail.com",
                    "create_password": "Lucky1234@"
                },
                "invalid_last_name": {
                    "country_of_residence": "Taiwan",
                    "first_name": "testme",
                    "last_name": "1234",  # 無效：姓氏不能為數字
                    "mobile_number": "+886 911222333",
                    "email_address": "test1234@gmail.com",
                    "create_password": "Lucky1234@"
                },
                "last_name_over_40_chars": {
                    "country_of_residence": "Taiwan",
                    "first_name": "testme",
                    "last_name": "testmetestmetestmetestmetestmetestmetestmetestme",  # 姓氏不能超過40位
                    "mobile_number": "+886 911222333",
                    "email_address": "test1234@gmail.com",
                    "create_password": "Lucky1234@"
                }
            }
        }
    }
}