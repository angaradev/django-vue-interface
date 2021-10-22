from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import GetStockSerializer
from product.models import Stock
from datetime import timedelta, datetime


def createResponse(stock, warehouseId):
    now = datetime.now()
    delta = timedelta(hours=2)
    mydate = now - delta

    sku = {
        "sku": stock.product.id,
        "warehouseId": warehouseId,
        "items": [
            {"type": "FIT", "count": stock.quantity, "updatedAt": mydate},
        ],
    }
    return sku


class GetStock(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        id_list = request.data.get("skus") or []
        warehouseId = request.data.get("warehouseId")
        qs = Stock.objects.filter(product__id__in=id_list)
        response = {"skus": [createResponse(x, warehouseId) for x in qs]}
        print(response)

        serializer = GetStockSerializer(response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
