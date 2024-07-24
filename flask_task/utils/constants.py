from enum import IntEnum, unique

RESPONSE_STATUS = "status"
RESPONSE_MSG = "msg"
API_RESPONSE_OBJ = {
    RESPONSE_STATUS: False,
    RESPONSE_MSG: "TODO",
}


@unique
class UserType(IntEnum):
    """_summary_

    Args:
        IntEnum (_type_): _description_
    """

    ADMIN = 0
    GUEST = 1
    CUSTOMER = 2
