import os,django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup
from faker import Faker
import random
from products.models import Product,Brand,Reviews



def seed_brand(n):
    fake=Faker()
    images=['',]
    for _ in range(n):
        Brand.objects.create(
            name=fake.name(),
            image=f"brand/{images[random.randint(0,9)]}"
        )
    print(f"{n} brands added successfully")


def seed_products(n):
    fake=Faker()
    flag_type=['new','sale','feature']
    brands=Brand.objects.all()
    images=['',]
    for _ in range(n):
        Product.objects.create(
            name=fake.name(),
            image=f"product/{images[random.randint(0,9)]}",
            flag=flag_type[random.randint(0,2)],
            price=round(random(20.99,99.99),2),
            sku=random.randint(100,1000000),
            subtitle=fake.text(max_nb_chars=450),
            description=fake.text(max_nb_chars=20000),
            brand=brands[random.randint(0,len(brands))]
        )
    print(f"{n} products added successfully")
   
def seed_reviews(n):
    pass





seed_brand(200)
seed_products(2000)