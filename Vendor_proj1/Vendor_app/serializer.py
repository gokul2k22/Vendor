# Import Statements
from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

# Serializer for Vendor model
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('id', 'name', 'contact_details', 'address', 'vendor_code',
                  'on_time_delivery_rate', 'quality_rating_avg',
                  'average_response_time', 'fulfillment_rate')

# Serializer for PurchaseOrder model
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ('id', 'po_number', 'vendor', 'order_date', 'delivery_date',
                  'items', 'quantity', 'status', 'quality_rating', 'issue_date',
                  'acknowledgment_date')

# Serializer for acknowledging a PurchaseOrder
class AcknowledgePurchaseOrderSerializer(serializers.Serializer):
    acknowledgment_date = serializers.DateTimeField()

# Serializer for HistoricalPerformance model (Vendor Performance Metrics)
class VendorPerformanceSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = HistoricalPerformance
        fields = ['on_time_delivery_rate', 'date', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
