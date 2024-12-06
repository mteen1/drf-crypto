from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from crpt.trading.models import TradingPair, PriceHistory, Trade
from .serializers import TradingPairSerializer, PriceHistorySerializer, TradeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

class TradingPairViewSet(viewsets.ModelViewSet):
    queryset = TradingPair.objects.filter(is_active=True)
    serializer_class = TradingPairSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['base_currency', 'quote_currency']
    filterset_fields = ['is_active']

    @action(detail=True, methods=['get'])
    def price_history(self, request, pk=None):
        trading_pair = self.get_object()
        history = PriceHistory.objects.filter(trading_pair=trading_pair)
        serializer = PriceHistorySerializer(history, many=True)
        return Response(serializer.data)

class PriceHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PriceHistory.objects.all()
    serializer_class = PriceHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['trading_pair']

class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['trading_pair', 'status']

    def perform_create(self, serializer):
        serializer.save(maker=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        trade = self.get_object()
        if trade.maker != request.user:
            return Response(
                {'error': 'Not authorized to cancel this trade'},
                status=status.HTTP_403_FORBIDDEN
            )
        if trade.status != Trade.PENDING:
            return Response(
                {'error': 'Can only cancel pending trades'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        trade.status = Trade.CANCELED
        trade.save()
        return Response(TradeSerializer(trade).data)
    


# Sample functionalviews

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def trading_pair_list(request):
    if request.method == 'GET':
        trading_pairs = TradingPair.objects.filter(is_active=True)
        serializer = TradingPairSerializer(trading_pairs, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TradingPairSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def trading_pair_detail(request, pk):
    try:
        trading_pair = TradingPair.objects.get(pk=pk)
    except TradingPair.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TradingPairSerializer(trading_pair)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TradingPairSerializer(trading_pair, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        trading_pair.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def price_history_list(request, trading_pair_id):
    try:
        trading_pair = TradingPair.objects.get(pk=trading_pair_id)
    except TradingPair.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    history = PriceHistory.objects.filter(trading_pair=trading_pair)
    serializer = PriceHistorySerializer(history, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def trade_list(request):
    if request.method == 'GET':
        trades = Trade.objects.all()
        serializer = TradeSerializer(trades, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(maker=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def trade_detail(request, pk):
    try:
        trade = Trade.objects.get(pk=pk)
    except Trade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TradeSerializer(trade)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TradeSerializer(trade, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        trade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_trade(request, pk):
    try:
        trade = Trade.objects.get(pk=pk)
    except Trade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if trade.maker != request.user:
        return Response(
            {'error': 'Not authorized to cancel this trade'},
            status=status.HTTP_403_FORBIDDEN
        )
    if trade.status != Trade.PENDING:
        return Response(
            {'error': 'Can only cancel pending trades'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    trade.status = Trade.CANCELED
    trade.save()
    return Response(TradeSerializer(trade).data)
