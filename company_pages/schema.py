from company_pages.models import CompanyPages
from blog.models import Post, Categories

from graphene import (
    String,
    ObjectType,
    Date,
    ID,
    Field,
    Schema,
    List,
    Boolean,
    Int,
    DateTime,
)


class PageType(ObjectType):
    id = ID()
    slug = String()
    title = String()
    textHTML = String()
    text = String()
    author = String()


class CategoryType(ObjectType):
    slug = String()
    name = String()


class PostType(ObjectType):
    id = ID()
    slug = String()
    image = String()
    title = String()
    textHTML = String()
    text = String()
    partsCategory = List(CategoryType)
    category = List(CategoryType)


class Query(ObjectType):
    page = Field(PageType, slug=String())
    pages = List(PageType)
    post = Field(PostType, slug=String())
    posts = List(PostType)

    def resolve_page(self, info, slug):
        qs = CompanyPages.objects.get(slug=slug)
        return qs

    def resolve_pages(self, info):
        qs = CompanyPages.objects.all()
        return qs

    def resolve_post(self, info, slug):
        post = Post.objects.get(slug=slug)
        print(info.context.build_absolute_uri(post.image.url))
        print(post.image.url)
        ret = {
            "slug": post.slug,
            "id": post.id,
            "image": info.context.build_absolute_uri(post.image.url)
            if post.image
            else None,
            "title": post.title,
            "text": post.text,
            "partsCategory": [
                {
                    "slug": x.slug,
                    "name": x.name,
                }
                for x in post.parts_category.all()
            ],
            "category": [
                {"slug": x.slug, "name": x.name} for x in post.categories.all()
            ],
        }
        return ret

    def resolve_posts(self, info):
        qs = Post.objects.all()
        posts = []
        for post in qs:
            ret = {
                "slug": post.slug,
                "id": post.id,
                "image": post.image.url if post.image else None,
                "title": post.title,
                "text": post.text,
                "partsCategory": [
                    {
                        "slug": x.slug,
                        "name": x.name,
                    }
                    for x in post.parts_category.all()
                ],
                "category": [
                    {"slug": x.slug, "name": x.name} for x in post.categories.all()
                ],
            }
            posts.append(ret)
        return posts


schema = Schema(query=Query)
