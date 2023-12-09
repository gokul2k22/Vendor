from django.urls import path
from .views import ( VendorCreate_View,VendorListView,VendorDetailView,VendorUpdate,VendorDelete,
                    PurchaseOrderList,PurchaseOrderCreate,PurchaseOrderGet,PurchaseOrderUpdate,PurchaseOrderDelete,
                    VendorPerformanceView,
                    AcknowledgePurchaseOrderView)

urlpatterns = [
    #   vendor 
    path('POST/api/vendors/', VendorCreate_View.as_view(), name='vendor-list-create'),

    path('GET/api/vendors/', VendorListView.as_view(), name='vendor-list'),
    path('GET/api/vendors/<int:vendor_id>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('PUT/api/vendors/<int:vendor_id>/', VendorUpdate.as_view(), name='vendor-Update'),
    path('DELETE/api/vendors/<int:vendor_id>/', VendorDelete.as_view(), name='vendor-DELETE'),

    #purchase order
    path('POST/api/purchase_orders/', PurchaseOrderCreate.as_view(), name='po_Create'),

    path('GET/api/purchase_orders/', PurchaseOrderList.as_view(), name='po_List'),
    path('GET/api/purchase_orders/<int:po_id>', PurchaseOrderGet.as_view(), name='po_DDetail'),
    path('PUT/api/purchase_orders/<int:po_id>', PurchaseOrderUpdate.as_view(), name='po_Update'),
    path('DELETE/api/purchase_orders/<int:po_id>', PurchaseOrderDelete.as_view(), name='po_Delete'),

    # Vendor Performance
    path('GET/api/vendors/<int:vendor_id>/performance', VendorPerformanceView.as_view(), name='vendor-performance'),

    # Acknowledge Purchase Order
    path('POST/api/purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),

]