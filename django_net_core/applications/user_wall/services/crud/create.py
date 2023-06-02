from applications.user_wall import models
from applications.user_wall.services.crud import crud_utils


def create_user_post_record(title: str, content: str) -> None:
    slug = crud_utils.slugify(str_for_slugify=title)
    if not crud_utils.is_unique_slug(model=models.UserPost, slug=slug):
        slug = crud_utils.generate_unique_slug(slug)

    try:
        models.UserPost.objects.create(
            title=title,
            content=content,
            slug=slug,
        )
    except Exception as exc:
        print(exc)

# def create_contact_record(
#         user_pk: int,
#         website: str,
#         github: str,
#         twitter: str,
#         instagram: str,
#         facebook: str,
# ) -> tuple[bool, Exception | None]:
#     try:
#         models.Contact.objects.create(
#             website=website,
#             github=github,
#             twitter=twitter,
#             instagram=instagram,
#             facebook=facebook,
#             user_id=user_pk,
#         )
#         result = (True, None)
#     except Exception as exc:
#         print(exc)
#         result = (False, exc)
#
#     return result