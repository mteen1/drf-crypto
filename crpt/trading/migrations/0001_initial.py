# Generated by Django 5.0.9 on 2024-12-05 10:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TradingPair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_currency', models.CharField(max_length=10)),
                ('quote_currency', models.CharField(max_length=10)),
                ('min_trade_size', models.DecimalField(decimal_places=10, max_digits=20)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'جفت ارز',
                'unique_together': {('base_currency', 'quote_currency')},
            },
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('quantity', models.DecimalField(decimal_places=10, max_digits=20)),
                ('status', models.CharField(choices=[('pending', 'در انتظار'), ('filled', 'انجام شده'), ('canceled', 'لغو شده')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('maker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maker_trades', to=settings.AUTH_USER_MODEL)),
                ('taker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taker_trades', to=settings.AUTH_USER_MODEL)),
                ('trading_pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='trading.tradingpair')),
            ],
        ),
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('open_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('close_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('low_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('volume', models.DecimalField(decimal_places=10, max_digits=20)),
                ('trading_pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_history', to='trading.tradingpair')),
            ],
            options={
                'verbose_name': 'تاریخچه قیمت',
                'indexes': [models.Index(fields=['trading_pair', 'timestamp'], name='trading_pri_trading_9ebbdb_idx')],
            },
        ),
    ]
