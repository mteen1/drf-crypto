from django.db import models
from django.conf import settings
from decimal import Decimal

class TradingPair(models.Model):
    base_currency = models.CharField(max_length=10)
    quote_currency = models.CharField(max_length=10)
    min_trade_size = models.DecimalField(max_digits=20, decimal_places=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('base_currency', 'quote_currency')
        verbose_name = 'جفت ارز'
    def __str__(self):
        return f'{self.base_currency}/{self.quote_currency}'
    
class PriceHistory(models.Model):
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE, related_name='price_history')
    timestamp = models.DateTimeField(auto_now_add=True)
    open_price = models.DecimalField(max_digits=20, decimal_places=10)
    close_price = models.DecimalField(max_digits=20, decimal_places=10)
    low_price = models.DecimalField(max_digits=20, decimal_places=10)
    volume = models.DecimalField(max_digits=20, decimal_places=10)

    class Meta:
        indexes = [
            models.Index(fields=['trading_pair','timestamp']),
        ]
        verbose_name = 'تاریخچه قیمت'

class Trade(models.Model):
    PENDING = 'pending'
    FILLED = 'filled'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        [PENDING, 'در انتظار'],
        [FILLED, 'انجام شده'],
        [CANCELED, 'لغو شده'],
    ]
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE, related_name='trades')
    maker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='maker_trades')
    taker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='taker_trades')
    price = models.DecimalField(max_digits=20, decimal_places=10)
    quantity = models.DecimalField(max_digits=20, decimal_places=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return self.price * self.quantity