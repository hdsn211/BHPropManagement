PropManager: Boarding House Management System
A comprehensive, full-stack web application designed to manage boarding houses, apartments, and houses. Built with Python and Django, featuring a modern glassmorphism UI, role-based authentication, and automated tenant management.

Features
Public Storefront: Beautiful property listings and room carousels for potential tenants.
Inquiry System: Potential tenants can contact the owner directly from listings.
Admin Dashboard: Interactive charts, financial tracking, and upcoming due alerts.
Role-Based Authentication: Secure portals separated for Owners and Tenants.
Maintenance Tracker: Tenants can submit photo evidence of issues; owners can track resolution status.
Automated Billing: One-click monthly due generation for all active tenants.
Advanced Search & Filtering: Filter tenants by room, or payments by status.

Tech Stack
Backend: Python 3.13, Django 6.0
Frontend: HTML5, CSS3, JavaScript, Bootstrap 5, Font Awesome
Database: SQLite3
Architecture: 3-App Django Structure (Properties, Tenants, Payments)

Setup Instructions
Clone or Download the project folder.
Open your terminal and navigate to the project directory.
Create a virtual environment:
python -m venv venv
Activate the virtual environment:
Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate
Install dependencies:
bash

pip install -r requirements.txt
Run database migrations:
bash

python manage.py migrate
Create an Owner (Admin) account:
bash

python manage.py createsuperuser
Start the development server:
bash

python manage.py runserver
Access the app: Open http://127.0.0.1:8000/ in your browser.
Access the Admin Panel: Go to http://127.0.0.1:8000/admin/ to add dummy Properties, Rooms, and Tenants to test the system.



Integrative Programming Final Project
