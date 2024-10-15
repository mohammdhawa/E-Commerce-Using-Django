import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from faker import Faker
import random
from products.models import (Product, ProductImages, Brand, Review)
from django.contrib.auth.models import User


def seed_users(n):
    fake = Faker()
    for _ in range(n):
        User.objects.create(
            username=fake.user_name(),
            password='MoH.1822'
        )


def seed_brand(n):
    fake = Faker()

    images = ['01.jpg', '02.jpg', '03.jpg', '04.jpg', '05.jpg',
              '06.jpg', '07.jpg', '08.jpg', '09.jpg', '10.jpg']

    for _ in range(n):
        Brand.objects.create(
            name=fake.name(),
            image=f"brands/{random.choice(images)}"
        )


def seed_product(n):
    fake = Faker()

    brands = Brand.objects.all()

    images = ['01.jpg', '02.jpg', '03.jpg', '04.jpg', '05.jpg',
              '06.jpg', '07.jpg', '08.jpg', '09.jpg', '10.jpg']
    flag_types = ['New', 'Feature', 'Sale']

    for _ in range(n):
        Product.objects.create(
            name=fake.name(),
            flag=random.choice(flag_types),
            price=round(random.uniform(1.99, 99.99), 2),
            image=f"products/{random.choice(images)}",
            quantity=random.randint(5, 20),
            sku=random.randint(111111, 999999),
            subtitle=fake.text(max_nb_chars=200),
            description=fake.text(max_nb_chars=2000),
            brand=random.choice(brands),
        )


def seed_product_images():
    images = ['01.jpg', '02.jpg', '03.jpg', '04.jpg', '05.jpg',
              '06.jpg', '07.jpg', '08.jpg', '09.jpg', '10.jpg']

    products = Product.objects.all()

    for product in products:
        for _ in range(random.randint(1, 5)):
            ProductImages.objects.create(
                product=product,
                image=f"products/{random.choice(images)}"
            )


def seed_review():
    fake = Faker()

    users = User.objects.all()
    products = Product.objects.all()

    for product in products:
        for _ in range(random.randint(1, 5)):
            Review.objects.create(
                user=random.choice(users),
                product=product,
                review=fake.text(max_nb_chars=200),
                rate=random.randint(1, 5),
                review_date=fake.date_time()
            )


# seed_users(10)
# seed_brand(50)
# seed_product(500)
# seed_product_images()
seed_review()
