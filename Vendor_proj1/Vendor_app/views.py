# Import Statements
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializer import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer, AcknowledgePurchaseOrderSerializer
from django.views import View
from rest_framework.views import APIView
from rest_framework import generics
from django.http import Http404
from django.utils import timezone
from rest_framework.exceptions import NotFound

# Vendor Management Views
class VendorListView(generics.ListAPIView):
    # View for listing all vendors
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorCreate_View(generics.CreateAPIView):
    # View for creating a new vendor
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorDetailView(generics.RetrieveAPIView):
    # View for retrieving details of a specific vendor
    serializer_class = VendorSerializer
    lookup_field = 'vendor_id'

    def get_object(self):
        vendor_id = self.kwargs.get('vendor_id')
        try:
            return Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            raise NotFound("Vendor not found.")

class VendorUpdate(generics.RetrieveUpdateAPIView):
    # View for updating a specific vendor
    serializer_class = VendorSerializer
    lookup_field = 'vendor_id'

    def get_object(self):
        vendor_id = self.kwargs.get('vendor_id')
        try:
            return Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            raise NotFound("Vendor not found.")

class VendorDelete(generics.RetrieveDestroyAPIView):
    # View for deleting a specific vendor
    serializer_class = VendorSerializer
    lookup_field = 'vendor_id'

    def get_object(self):
        vendor_id = self.kwargs.get('vendor_id')
        try:
            return Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            raise NotFound("Vendor not found.")

# Purchase Order Views
class PurchaseOrderList(generics.ListAPIView):
    # View for listing all purchase orders
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderCreate(generics.CreateAPIView):
    # View for creating a new purchase order
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderGet(generics.RetrieveAPIView):
    # View for retrieving details of a specific purchase order
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'po_id'

    def get_object(self):
        po_id = self.kwargs.get('po_id')
        try:
            return PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            raise NotFound("PO Not Found.")

class PurchaseOrderUpdate(generics.RetrieveUpdateAPIView):
    # View for updating a specific purchase order
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'po_id'

    def get_object(self):
        po_id = self.kwargs.get('po_id')
        try:
            return PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            raise NotFound('PO not found')

class PurchaseOrderDelete(generics.RetrieveDestroyAPIView):
    # View for deleting a specific purchase order
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'po_id'

    def get_object(self):
        po_id = self.kwargs.get('po_id')
        try:
            return PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            raise NotFound('PO not found')

# Vendor Performance View
class VendorPerformanceView(generics.RetrieveAPIView):
    # View for retrieving historical performance metrics for a specific vendor
    serializer_class = VendorPerformanceSerializer

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        return HistoricalPerformance.objects.filter(vendor__id=vendor_id)

    def retrieve(self, request, *args, **kwargs):
        vendor_id = self.kwargs['vendor_id']
        try:
            # Attempt to get the vendor
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            # If the vendor does not exist, raise a NotFound exception
            raise NotFound("Data not found.")
        queryset = self.get_queryset()
        instance = queryset.last()  # Get the latest historical performance for the vendor

        # Calculate performance metrics directly in the view
        vendor = Vendor.objects.get(pk=vendor_id)
        completed_pos = vendor.purchaseorder_set.filter(status='completed')

        # On-Time Delivery Rate
        on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now())
        on_time_delivery_rate = (on_time_deliveries.count() / completed_pos.count()) * 100 if completed_pos.count() > 0 else 0.0

        # Quality Rating Average
        completed_pos_with_rating = completed_pos.filter(quality_rating__isnull=False)
        total_ratings = sum([po.quality_rating for po in completed_pos_with_rating])
        quality_rating_avg = total_ratings / completed_pos_with_rating.count() if completed_pos_with_rating.count() > 0 else 0.0

        # Average Response Time
        acknowledged_pos = completed_pos.filter(acknowledgment_date__isnull=False)
        response_times = [po.acknowledgment_date - po.issue_date for po in acknowledged_pos]
        average_response_time = sum(response_times, timezone.timedelta()) / len(response_times) if len(response_times) > 0 else timezone.timedelta()

        # Fulfillment Rate
        successful_fulfillments = completed_pos.filter(status__isnull=True)
        fulfillment_rate = (successful_fulfillments.count() / completed_pos.count()) * 100 if completed_pos.count() > 0 else 0.0

        # Update or create a new HistoricalPerformance entry
        if not instance or completed_pos.last().delivery_date > instance.date:
            HistoricalPerformance.objects.create(
                vendor=vendor,
                date=timezone.now(),
                on_time_delivery_rate=on_time_delivery_rate,
                quality_rating_avg=quality_rating_avg,
                average_response_time=average_response_time.total_seconds(),  # convert timedelta to seconds
                fulfillment_rate=fulfillment_rate
            )

        # Return the latest historical performance
        instance = HistoricalPerformance.objects.filter(vendor=vendor).last()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# Acknowledge Purchase Order View
class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    # View for acknowledging a purchase order
    queryset = PurchaseOrder.objects.all()
    serializer_class = AcknowledgePurchaseOrderSerializer
    lookup_field = 'po_id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        purchase_order_id = self.kwargs.get(self.lookup_field)

        try:
            # Attempt to get the purchase order
            purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)
        except PurchaseOrder.DoesNotExist:
            # If the purchase order does not exist, return a 404 response
            return Response({"detail": "Purchase Order not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(purchase_order, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Acknowledge the purchase order
        purchase_order.acknowledgment_date = serializer.validated_data['acknowledgment_date']
        purchase_order.save()

        # Trigger recalculation of average_response_time
        purchase_order.vendor.update_performance_metrics()

        return Response(serializer.data)
