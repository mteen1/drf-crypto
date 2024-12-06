from rest_framework import serializers
from crpt.trading.models import TradingPair, PriceHistory, Trade

class TradingPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingPair
        fields = '__all__'

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = '__all__'

class TradeSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=18, decimal_places=8, read_only=True)
    
    class Meta:
        model = Trade
        fields = '__all__'
        read_only_fields = ('maker', 'status', 'created_at', 'updated_at')