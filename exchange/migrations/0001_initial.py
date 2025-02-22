# Generated by Django 4.2 on 2025-02-10 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(db_index=True, max_length=20)),
                ('symbol', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('priority', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CurrencyExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valuation_date', models.DateField(db_index=True)),
                ('rate_value', models.DecimalField(decimal_places=6, max_digits=18)),
                ('exchanged_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exchange.currency')),
                ('source_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchanges', to='exchange.currency')),
            ],
        ),
    ]
