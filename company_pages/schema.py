from company_pages.models import CompanyPages
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


class Query(ObjectType):
    page = Field(PageType)
    pages = List(PageType)

    def resolve_page(self, info, slug):
        qs = CompanyPages.objects.get(slug=slug)
        return qs

    def resolve_pages(self, info):
        qs = CompanyPages.objects.all()
        return qs


schema = Schema(query=Query)
