from django.db.models import QuerySet

from applications.abstract_activities.models import AbstractPost
from applications.groups.models import GroupPost
from applications.user_wall.models import UserPost
from applications.user_wall.services.crud.delete import delete_tag_from_post


def update_posts_view_count(
        creator_pk: int,
        visitor_pk: int,
        posts: QuerySet[AbstractPost]
) -> None:
    if visitor_pk == creator_pk:
        return None

    for post in posts:
        if visitor_pk not in post.user_list:
            # increase counter when the appropriate page is opened
            post.view_counts += 1
            post.user_list.append(visitor_pk)
            post.save()


def is_post_changed(
        post: AbstractPost,
        new_title: str,
        new_content: str,
        new_tags: list[str | None],
        old_tags: list[str | None],
        is_published: bool,
) -> bool:
    """Check for changes in the post"""
    if ((post.title != new_title) or (post.content != new_content) or
            (post.is_published != is_published) or (set(new_tags) != set(old_tags))):
        return True

    return False


def return_new_tag_list(
        new_tags: list[str],
        old_tags: list[str],
        post: UserPost | GroupPost,
) -> list[str]:
    """
    If a set of tags was changed, the function would return a new set of tag as a list.
    Otherwise, return an old tag list.
    """
    new_tags_set = set(new_tags)
    old_tags_set = set(old_tags)
    added_tags_list = list(new_tags_set.difference(old_tags_set))

    if not added_tags_list:
        if len(old_tags) > len(new_tags):
            discarded_tags = list(old_tags_set.difference(new_tags_set))
            for tag in discarded_tags:
                delete_tag_from_post(tag_title=tag, post=post)
        return new_tags

    return added_tags_list
