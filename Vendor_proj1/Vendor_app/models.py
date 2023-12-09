# Import Statements
from django.db import models
from django.utils import timezone

# Vendor Model
class Vendor(models.Model):
    # Fields representing vendor details and performance metrics
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    # Method to update the vendor's performance metrics
    def update_performance_metrics(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')

        # Calculate performance metrics similar to your VendorPerformanceView
        on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now())
        on_time_delivery_rate = (on_time_deliveries.count() / completed_pos.count()) * 100 if completed_pos.count() > 0 else 0.0

        completed_pos_with_rating = completed_pos.filter(quality_rating__isnull=False)
        total_ratings = sum([po.quality_rating for po in completed_pos_with_rating])
        quality_rating_avg = total_ratings / completed_pos_with_rating.count() if completed_pos_with_rating.count() > 0 else 0.0

        acknowledged_pos = completed_pos.filter(acknowledgment_date__isnull=False)
        response_times = [po.acknowledgment_date - po.issue_date for po in acknowledged_pos]
        average_response_time = sum(response_times, timezone.timedelta()) / len(response_times) if len(response_times) > 0 else timezone.timedelta()

        successful_fulfillments = completed_pos.filter(status__isnull=True)
        fulfillment_rate = (successful_fulfillments.count() / completed_pos.count()) * 100 if completed_pos.count() > 0 else 0.0

        # Update the Vendor's performance metrics
        self.on_time_delivery_rate = on_time_delivery_rate
        self.quality_rating_avg = quality_rating_avg
        self.average_response_time = average_response_time.total_seconds() if average_response_time else 0.0
        self.fulfillment_rate = fulfillment_rate
        self.save()

# PurchaseOrder Model
class PurchaseOrder(models.Model):
    # Fields representing purchase order details
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=50, unique=True)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

# HistoricalPerformance Model
class HistoricalPerformance(models.Model):
    # Fields representing historical performance metrics of a vendor
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)
