from applications.user_profiles.models import CustomUser
from applications.groups.models import Group


GROUP_FORBIDDEN_MESSAGE = """<div style=\"width: 700px; margin: auto; margin-top: 50px; font-size: 24px;\" >
            <h1 style=\"font-size: 44px;\"> Access forbidden!</h1> 
            <p>You already have a group</p>
            </div>"""

GROUP_CREATION_FORBIDDEN_MESSAGE = """<div style=\"width: 700px; margin: auto; margin-top: 50px; font-size: 24px;\" >
            <h1 style=\"font-size: 44px;\"> Access forbidden!</h1> 
            <p>Only group author can create a new post.</p>
            </div>"""


def is_user_group_author(visitor: CustomUser, group: Group) -> bool:
    return group.creator.pk == visitor.pk
