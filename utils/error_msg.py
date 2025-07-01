from enum import Enum

class RegisterErrorMsg(Enum):
    INVALID_FIRST_NAME = "Please enter a valid first name"
    INVALID_LAST_NAME = "Please enter a valid last name"
    MAX_CHAR_LIMIT = "Maximum characters limit is 40"

