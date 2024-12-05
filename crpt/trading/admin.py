from django.contrib import admin
from .models import TradingPair, PriceHistory, Trade

admin.site.register(TradingPair)
admin.site.register(PriceHistory)
admin.site.register(Trade)