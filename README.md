# Inventory & Billing System (SME) — Backend API (Django REST Framework)

A real-world **Inventory + Billing + Accounting backend system** built with **Django REST Framework** for small & medium businesses (SMEs).  
This project provides a complete backend API for managing products/stock, customers/suppliers, purchase & sale invoices (nested items), payments (partial/paid/due), ledgers, and reporting dashboards.

This project was built to strengthen skills in:
- Django ORM + PostgreSQL
- DRF Serializers / ViewSets / Permissions
- Nested create workflows using transactions
- Reverse foreign key relations + aggregations
- Business logic (stock updates, due tracking, partial payments)
- JWT Authentication + role-based access

---

## 🚀 Features

### 🔐 Authentication & Roles
- JWT Login / Refresh using **SimpleJWT**
- Owner-only registration (first account only)
- Role-based access:
  - **OWNER**: full permissions
  - **STAFF**: limited permissions (configurable)

---

### 📦 Inventory Management
- Product CRUD
- SKU & validation rules
- Stock quantity tracking
- Low stock threshold alerts
- Search + ordering + filtering

---

### 👥 Customers & Suppliers
- Customer CRUD
- Supplier CRUD
- Search + ordering support
- Custom permission control (example: staff create/update, owner delete)

---

### 🧾 Billing System

#### ✅ Purchase Invoices
- Create purchase invoice with nested items
- Auto calculates total amount
- Stock increases automatically

#### ✅ Sale Invoices
- Create sale invoice with nested items
- Stock validation (prevents negative stock)
- Stock decreases automatically
- Payment status: `UNPAID / PARTIAL / PAID`

---

### 💰 Payments & Due Tracking
#### ✅ Sale Payments
- Partial payments supported
- Auto updates invoice payment_status
- Prevents overpayment (cannot exceed due)

#### ✅ Supplier Payments
- Same due logic for purchase invoices
- Supplier payable tracking

---

### 📊 Reports & Analytics
- Low Stock Products Report
- Sales Summary Report (date range)
- Top Products Report
- Profit Report (Revenue - Estimated Cost)
- Customer Ledger
- Supplier Ledger

---

## 🧰 Tech Stack
- **Python**
- **Django**
- **Django REST Framework**
- **PostgreSQL**
- **JWT Authentication** (SimpleJWT)
- **Swagger/OpenAPI Documentation** (drf-spectacular)

---

## ⚙️ Local Setup (Development)

### 1) Clone repository
```bash
git clone https://github.com/aliakbar123634/Inventory-Billing-System-SME-.git
cd Inventory-Billing-System-SME-
2) Create & activate virtual environment (Windows)
bash
Copy code
python -m venv venv
venv\Scripts\activate
3) Install dependencies
bash
Copy code
pip install -r requirements.txt
4) Configure environment variables
Create a .env file in project root:

env
Copy code
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=stockflow_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
⚠️ Never push .env to GitHub.

5) Apply migrations
bash
Copy code
python manage.py makemigrations
python manage.py migrate
6) Create admin/superuser
bash
Copy code
python manage.py createsuperuser
7) Run the server
bash
Copy code
python manage.py runserver
📌 Swagger API Documentation
After starting the server:

Swagger UI:
http://127.0.0.1:8000/api/docs/

OpenAPI Schema:
http://127.0.0.1:8000/api/schema/

🔥 Main API Endpoints (Examples)
Auth
POST /api/auth/register/ (Owner only — first user)

POST /api/auth/login/

POST /api/auth/refresh/

Inventory
/api/products/

Customers & Suppliers
/api/customers/

/api/suppliers/

Billing
/api/purchase-invoices/

/api/sale-invoices/

Payments
/api/sale-payments/

/api/supplier-payments/

Reports
/api/reports/low-stock/

/api/reports/sales-summary/?start=YYYY-MM-DD&end=YYYY-MM-DD

/api/reports/top-products/?limit=10

/api/reports/profit/?start=YYYY-MM-DD&end=YYYY-MM-DD

/api/reports/customer-ledger/?customer=1

/api/reports/supplier-ledger/?supplier=1

✅ Postman Collection
A Postman collection is included in the repository inside the Postman/ folder.

🗺️ Roadmap (Next Features)

Invoice cancel/return with stock reverse logic

Import/Export (CSV/Excel)

Deployment (Railway / Render)

Automated unit tests

👤 Author

Ali Akbar Shah
Django REST API Developer
GitHub: https://github.com/aliakbar123634/
