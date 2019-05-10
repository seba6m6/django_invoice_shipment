# django_invoice_shipment
A Django App for issuing invoices and shipments

It's a simple app which as an aim has to help small businesses to issue invoices and managed their shipments.
You can easily implement it by hosting on platform like pythonanywhere.com or for example on your own ubuntu server (DigitalOcean, Alibaba cloud etc.)

## Main functions of this app:
- issuing invoices to our clients
- issuing a shipments which are connected to the invoice items (invoice items can be shipped in one or more shipments - depending on the situation of our stock)
- managing the state of our invoices (paid, unpaid, paid in %)
- while issuing a shipment one can only choose an item from the invoice that was already registered as paid (which prevents a user from sending an item which was not paid for)

## Instalation

#### 1. create an virtual env
#### 2. install the required packages from requirememnts.txt `` pip install -r requirments.txt ``
 This app is using a package called WeasyPrint, it enables us to generate a pdf from our invoice template.In order to use it on your machine you will need to install some pre-required packages on your computer (in case you are on Windows machine it might be a bit tricky) Please check out this documentation to see what you have to do step by step https://weasyprint.readthedocs.io/en/stable/index.html 
#### 3. Please create standard settings.py file and add the modules that we installed in the step 2 to our INSTALLED_APPS
#### 4. You can do a standard ``python manage.py makemigrations `` and ``python manage.py migrate`` to make sure that all of the tables in our db got created, you can also create a superuser by ``python manage.py createsuperuser`` so that you can access admin page

#### Feel free to contact me by email batianm@outlook.com. I already apologize in advance if i won't be able to respond to you in a timely manner.
