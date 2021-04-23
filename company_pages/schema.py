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
    image = String()


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
        return Post.object.get(slug=slug)

    def resolve_posts(self, info):
        return Post.object.all()


schema = Schema(query=Query)
