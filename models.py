from email.policy import default
from enum import unique
from unicodedata import category
from sqlalchemy import null
from tortoise import Model, fields
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator



class Category(Model):
    id = fields.IntField(pk=True, generated=True, index = True)
    name = fields.CharField(max_length=30, null=False, unique=True)
    slug = fields.CharField(max_length=30, null=False)
    description = fields.CharField(max_length=1000, null=False)
    parent_cat = fields.ForeignKeyField("models.Category", on_delete=fields.CASCADE, null=True)

    def __str__(self):
        return self.name

class Product(Model):
    id = fields.IntField(pk=True, generated=True, index = True)
    name = fields.CharField(max_length=30, null=False)
    slug = fields.CharField(max_length=30, null=False)
    featured_image = fields.CharField(max_length=200, null=False)
    featured_image_alt = fields.CharField(max_length=100, null=False)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    quantity = fields.IntField(default=0)
    description = fields.CharField(max_length=1000, null=False)
    product_created = fields.DatetimeField(default=datetime.utcnow)
    colors = fields.CharField(max_length=1000, null=False)
    size = fields.CharField(max_length=1000, null=False)
    category = fields.ForeignKeyField("models.Category", on_delete=fields.CASCADE)

class User(Model):
    id = fields.IntField(pk=True, generated=True, index=True)
    username = fields.CharField(max_length=20, unique=True, null=False, index=True)
    password = fields.CharField(max_length=300, null=False)
    email = fields.CharField(max_length=30, null=False, unique=True)
    joining_date = fields.DatetimeField(default=datetime.utcnow)
    is_verified = fields.BooleanField(default=False)
    contact_number = fields.CharField(max_length=20, null=False, unique=True)
    is_admin = fields.BooleanField(default=False)

class Cart(Model):
    id = fields.IntField(pk=True, generated=True, index=True)
    product = fields.ForeignKeyField("models.Product", on_delete=fields.CASCADE)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    quantity = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

product_pydantic = pydantic_model_creator(Product, name="Product")
product_pydanticIn = pydantic_model_creator(Product, name="ProductIn", exclude=("id", "slug"))

category_pydantic = pydantic_model_creator(Category, name="Category")
category_pydanticIn = pydantic_model_creator(Category, name="CategoryIn", exclude=("id", "slug"))

user_pydantic = pydantic_model_creator(User, name="User", exclude=("is_verified", ))
user_pydanticIn = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
user_pydanticOut = pydantic_model_creator(User, name="UserOut", exclude=("password", ))
