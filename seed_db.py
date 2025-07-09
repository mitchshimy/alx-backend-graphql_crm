import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')
django.setup()

from crm.models import Customer, Product, Order

# Optional: Clear existing data
print("Clearing old data...")
Order.objects.all().delete()
Customer.objects.all().delete()
Product.objects.all().delete()

print("Seeding data...")

# Create customers
customer_names = [
    ("Alice", "alice@example.com", "0712345678"),
    ("Bob", "bob@example.com", "0723456789"),
    ("Carol", "carol@example.com", "0734567890"),
    ("Dave", "dave@example.com", "0745678901"),
]

customers = []
for name, email, phone in customer_names:
    customer = Customer.objects.create(
        name=name,
        email=email,
        phone=phone
    )
    customers.append(customer)

print(f"Seeded {len(customers)} customers.")

# Create products
product_list = [
    ("Laptop", 1500.00, 10),
    ("Smartphone", 900.00, 25),
    ("Headphones", 150.00, 40),
    ("Monitor", 250.00, 15),
]

products = []
for name, price, stock in product_list:
    product = Product.objects.create(
        name=name,
        price=price,
        stock=stock
    )
    products.append(product)

print(f"Seeded {len(products)} products.")

# Create orders
for _ in range(10):
    customer = random.choice(customers)
    num_products = random.randint(1, 3)
    selected_products = random.sample(products, num_products)

    total = sum(product.price for product in selected_products)
    order = Order.objects.create(
        customer=customer,
        total_amount=total,
        order_date=timezone.now() - timedelta(days=random.randint(1, 30))
    )
    order.products.set(selected_products)

print("10 random orders created.")
print("✅ Done seeding the database.")
