from datetime import datetime

from pydantic import Field

from simnet.models.base import APIModel

__all__ = ("Announcement",)


class Announcement(APIModel):
    """
    Represents an announcement.

    Attributes:
        id (int): The ID of the announcement.
        title (str): The title of the announcement.
        subtitle (str): The subtitle of the announcement.
        banner (str): The URL of the banner image for the announcement.
        content (str): The content of the announcement.

        type_label (str): The label of the announcement type.
        type (int): The type of the announcement.
        tag_icon (str): The URL of the tag icon for the announcement.

        login_alert (bool): Indicates whether the announcement is shown to logged-in users only.
        remind (bool): Indicates whether to send reminder notifications for the announcement.
        alert (bool): Indicates whether to send alert notifications for the announcement.
        remind_ver (int): The version of the reminder notification.
        extra_remind (bool): Indicates whether to send additional reminder notifications for the announcement.

        start_time (datetime): The start time of the announcement.
        end_time (datetime): The end time of the announcement.
        tag_start_time (datetime): The start time of the tag for the announcement.
        tag_end_time (datetime): The end time of the tag for the announcement.

        lang (str): The language of the announcement.
        has_content (bool): Indicates whether the announcement has content.
    """

    id: int = Field(alias="ann_id")
    title: str
    subtitle: str
    banner: str
    content: str

    type_label: str
    type: int
    tag_icon: str

    login_alert: bool
    remind: bool
    alert: bool
    remind_ver: int
    extra_remind: bool

    start_time: datetime
    end_time: datetime
    tag_start_time: datetime
    tag_end_time: datetime

    lang: str
    has_content: bool
