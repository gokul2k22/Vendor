# Vendor management system

1. Introduction
-----------------
Overview
The Vendor Management System is a Django-based project designed to manage vendors and purchase orders. It includes features such as vendor CRUD operations, purchase order management, performance metrics, and purchase order acknowledgment.
Purpose
The purpose of this system is to streamline the vendor and purchase order management processes, providing a convenient API for easy integration.

2. Prerequisites
----------------
Python and Django Installation
Ensure that Python and Django are installed. 
You can install Django using:
>> pip install django 
Database Setup
Configure the database settings in settings.py. The project assumes a PostgreSQL database.

	

![Screenshot (146)](https://github.com/gokul2k22/Vendor/assets/141205539/5c44b7e8-ebd6-4218-886c-3a526f477025)

3. Project Setup
-----------------
Install Dependencies for Django rest-framework
>> pip install djangorestframework
>> pip install psycopg2
Database Migration
>>python manage.py makemigrations 
>>python manage.py migrate

4. Run the Project
------------------
Django Development Server
>>python manage.py runserver 
Visit http://localhost:8000/ in your browser to access the project.

![Screenshot (147)](https://github.com/gokul2k22/Vendor/assets/141205539/e89caf74-7e33-4bb2-8f91-0f0b47c5dcbb)


5. API Endpoints
-----------------
Vendor Management
•	List Vendors: GET /api/vendors/
•	Create Vendor: POST /api/vendors/
•	View Vendor Details: GET /api/vendors/<vendor_id>/
•	Update Vendor: PUT /api/vendors/<vendor_id>/
•	Delete Vendor: DELETE /api/vendors/<vendor_id>/
Purchase Order Management
•	Create Purchase Order: POST /api/purchase_orders/
•	List Purchase Orders: GET /api/purchase_orders/
•	View Purchase Order Details: GET /api/purchase_orders/<po_id>/
•	Update Purchase Order: PUT /api/purchase_orders/<po_id>/
•	Delete Purchase Order: DELETE /api/purchase_orders/<po_id>/
Performance Metrics
•	View Vendor Performance Metrics: GET /api/vendors/<vendor_id>/performance
Acknowledging Purchase Orders
•	Acknowledge Purchase Order: PUT /api/purchase_orders/<po_id>/acknowledge/









Vendor Management:

List Vendors:
Functionality: Display a list of all vendors in the system.
Features: Sorting, filtering, and search options for easy navigation.

Create Vendor:
Functionality: Add a new vendor to the system.
Required Information: Vendor name, contact details, address, and other relevant details.

View Vendor Details:
Functionality: Display comprehensive details of a specific vendor.
Information: Contact details, address, payment terms, performance history, etc.

Update Vendor:
Functionality: Modify information about an existing vendor.
Editing: Allow changes to contact details, address, or any other relevant information.

Delete Vendor:
Functionality: Remove a vendor from the system.
Confirmation: Require confirmation before permanently deleting a vendor.
Purchase Order Management:

Create Purchase Order:
Functionality: Generate a new purchase order for a specific vendor.
Details: Include item details, quantity, price, delivery date, and any other relevant information.


List Purchase Orders:
Functionality: Display a list of all purchase orders in the system.
Features: Sorting, filtering, and search options for efficient tracking.

View Purchase Order Details:
Functionality: Display comprehensive details of a specific purchase order.
Information: Item details, quantity, price, delivery status, and any other relevant details.

Update Purchase Order:
Functionality: Modify information about an existing purchase order.
Editing: Allow changes to quantities, delivery dates, or any other relevant details.

Delete Purchase Order:
Functionality: Remove a purchase order from the system.
Confirmation: Require confirmation before permanently deleting a purchase order.

Performance Metrics:
Functionality: Track and analyze the performance of vendors and the purchase order process.
Metrics: Vendor delivery time, order accuracy, vendor reliability, and other relevant key performance indicators (KPIs).

Acknowledge Purchase Order
The acknowledgment date of a purchase order triggers a vendor's performance metrics recalculation upon acknowledgment and handles error cases such as a non-existing purchase order.

6. Conclusion
--------------
These instructions cover the basic setup, usage, and API endpoints of the Vendor Management System. For additional details or customization, refer to the project's codebase and documentation.
________________________________________

