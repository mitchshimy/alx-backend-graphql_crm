import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter
from .mutations import CreateCustomer, BulkCreateCustomers, CreateProduct, CreateOrder

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node, )

class ProductType(DjangoObjectType):  # <- FIXED
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    updated_products = graphene.List(ProductType)
    success = graphene.String()

    @staticmethod
    def mutate(root, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []

        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_products.append(product)

        return UpdateLowStockProducts(
            updated_products=updated_products,
            success=f"Restocked {len(updated_products)} products successfully"
        )

class Query(graphene.ObjectType):
    customer = graphene.relay.Node.Field(CustomerType)
    all_customers = DjangoFilterConnectionField(CustomerType)
    total_customers = graphene.Int()
    total_orders = graphene.Int()
    total_revenue = graphene.Float()

    def resolve_total_customers(root, info):
        return Customer.objects.count()

    def resolve_total_orders(root, info):
        return Order.objects.count()

    def resolve_total_revenue(root, info):
        return sum(order.total_amount for order in Order.objects.all())

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)  # <- Ensure this exists
