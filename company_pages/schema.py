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


class Car(ObjectType):
    slug = String()
    name = String()


class PostType(ObjectType):
    id = ID()
    slug = String()
    image = String()
    title = String()
    excerpt = String()
    text = String()
    partsCategory = List(CategoryType)
    category = List(CategoryType)
    date = Date()
    author = String()
    car = List(Car)


def makePost(post):

    ret = {
        "slug": post.slug,
        "id": post.id,
        "image": post.image.url if post.image else None,
        "title": post.title,
        "excerpt": post.excerpt,
        "text": post.text,
        "date": post.date,
        "author": post.author,
        "partsCategory": [
            {
                "slug": x.slug,
                "name": x.name,
            }
            for x in post.parts_category.all()
        ],
        "category": [{"slug": x.slug, "name": x.name} for x in post.categories.all()],
        "car": [{"slug": x.slug, "name": x.name} for x in post.car.all()],
    }
    return ret


class Query(ObjectType):
    page = Field(PageType, slug=String())
    pages = List(PageType)
    post = Field(PostType, slug=String())
    posts = List(PostType)
    categories = List(CategoryType)
    postsByCategory = List(PostType, slug=String())

    def resolve_categories(self, info):
        return Categories.objects.all()

    def resolve_page(self, info, slug):
        qs = CompanyPages.objects.get(slug=slug)
        return qs

    def resolve_pages(self, info):
        qs = CompanyPages.objects.all()
        return qs

    def resolve_postsByCategory(self, info, slug):
        posts = Post.objects.filter(categories__slug=slug)
        ret = []
        for post in posts:
            ret.append(makePost(post))
        return ret

    def resolve_post(self, info, slug):
        post = Post.objects.get(slug=slug)
        print(info.context.build_absolute_uri(post.image.url))
        print(post.image.url)
        ret = makePost(post)
        return ret

    def resolve_posts(self, info):
        qs = Post.objects.all()
        posts = []
        for post in qs:
            ret = makePost(post)
            posts.append(ret)
        return posts


schema = Schema(query=Query)
