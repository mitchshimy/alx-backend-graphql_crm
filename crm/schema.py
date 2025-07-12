import graphene
from graphene_django import DjangoObjectType
from .models import Product
from datetime import datetime

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # No arguments needed

    success = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_list = []

        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_list.append(product)

        return UpdateLowStockProducts(
            success=f"{len(updated_list)} product(s) restocked at {datetime.now()}",
            updated_products=updated_list
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
