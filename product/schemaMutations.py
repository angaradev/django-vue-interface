from product.models.models import ProductRating, Product
from users.models import AutoUser
from graphene import String, ObjectType, Field, Boolean, Mutation, ID, Int
from .schemaTypes import AutoUserType, RatingType


class createRatingsMutation(Mutation):
    class Arguments:
        score = Int()
        productId = ID()
        userId = String()

    rating = Field(RatingType)

    def mutate(root, info, score, productId, userId):
        product = Product.objects.get(id=productId)
        rating, created = ProductRating.objects.update_or_create(
            score=score, product=product, autoUser__userId=userId
        )

        qs = ProductRating.objects.get
        return createRatingsMutation(rating=rating)


class createAutoUserMutation(Mutation):
    class Arguments:
        userId = String()

    ok = Boolean()
    user = Field(AutoUserType)

    def mutate(root, info, userId):
        print(userId)
        user, ok = AutoUser.objects.update_or_create(userId=userId)

        return createAutoUserMutation(user=user)


class Mutation(ObjectType):
    createAutoUser = createAutoUserMutation.Field()
    createRating = createRatingsMutation.Field()
