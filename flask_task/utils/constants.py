from enum import IntEnum, unique

RESPONSE_STATUS = "status"
RESPONSE_MSG = "msg"
API_RESPONSE_OBJ = {
    RESPONSE_STATUS: False,
    RESPONSE_MSG: "TODO",
}


@unique
class UserType(IntEnum):
    """
    Enumeration of different user types.
    Parameters:
        - None
    Returns:
        - UserType: Enumeration values representing different user types.
    function(UserType.ADMIN) -> 0
        - This example demonstrates retrieving the enumeration value for
        an ADMIN user type, which outputs 0.
    """

    ADMIN = 0
    GUEST = 1
    CUSTOMER = 2


@unique
class TaskType(IntEnum):
    """
    Enumeration for different task types.
    This class defines three different task types using an integer enumeration.
    Attributes:
        - INITIATED (int): Represents the initiated state of a task.
        - REVIEW (int): Represents the review state of a task.
        - PUBLISHED (int): Represents the published state of a task.
    Examples:
        TaskType.INITIATED -> 0
        TaskType.REVIEW -> 1
        TaskType.PUBLISHED -> 2
    """

    INITIATED = 0
    REVIEW = 1
    PUBLISHED = 2
