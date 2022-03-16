from statistics import median
from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=60, null=True)
    username = fields.CharField(max_length=60, null=True, unique=True)
    telegram_id = fields.CharField(max_length=60, null=True, unique=True)
    password = fields.CharField(max_length=255, null=True, blank=True)
    on_bot = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)


class Media(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, null=True)
    category = fields.CharField(max_length=60, null=True)
    url = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)


class Vote(Model):
    id = fields.BigIntField(pk=True)
    telegram_id = fields.CharField(max_length=60, null=True)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)
