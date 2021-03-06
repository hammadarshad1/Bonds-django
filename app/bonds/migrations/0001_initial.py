# Generated by Django 3.2.12 on 2022-04-06 12:07

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bond',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=40, validators=[django.core.validators.MinLengthValidator(3)])),
                ('number_of_bonds', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10000), django.core.validators.MinValueValidator(1)])),
                ('selling_price', models.DecimalField(decimal_places=4, max_digits=13, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100000000.0)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('sell', 'Sell'), ('buy', 'Buy')], max_length=4)),
                ('bond', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bonds.bond')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
