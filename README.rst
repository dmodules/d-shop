##########
D-Shop - Simple e-commerce platform build with Django, Django-CMS and Vue.JS
##########
Created by `D-Modules <https://www.d-modules.com>`_


Open source platform to build simple but robust e-commerce website using Python. Go to website https://d-shop-ecommerce.com

********
Demo
********
Go to https://demo.d-shop-ecommerce.com

********
Features
********

* Manage orders
* Taxs for Canada
* Inventory management
* Manage products with variants
* Dashboard with stats
* Manage content with Django CMS
* Create popup for promotions
* Create discounts by products for categories
* Payment with Stripe
* Products search


********
ENV Vars
********

* SECURE_SSL_REDIRECT = True
* CLIENT_TITLE = <client_title>
* SHOP_VENDOR_EMAIL = <vendor@example.com>
* TIME_ZONE = “America/Toronto”
* EMAIL_HOST = <email_host>
* EMAIL_PORT = <email_port>
* EMAIL_USE_TLS = <use_tls>
* EMAIL_HOST_USER = <user@example.com>
* EMAIL_HOST_PASSWORD = <password>
* DEFAULT_FROM_EMAIL = <noreply@example.com>
* DEFAULT_TO_EMAIL = <info@example.com>
* STRIPE_SECRET_KEY = <secret_key>
* STRIPE_PUBLIC_KEY = <public_key>
* STRIPE_ACCOUNT_ID = <account_id>
* MAILCHIMP_KEY = <mailchimp_key>
* MAILCHIMP_LISTID = <mailchimp_list_id>
* RECAPTCHA_PUBLIC_KEY = <key>
* RECAPTCHA_SECRET_KEY = <key>



********
Installation with Docker
********

* git clone git@github.com:dmodules/d-shop.git
* cd d-shop
* docker-compose build
* docker-compose run web python manage.py migrate
* docker-compose run web python manage.py createsuperuser
* download media for demo https://test.com/
* copy media in data/media
* import db for demo: cat demo_data.sql | docker exec -i your-db-container psql -U postgres
* install node packages: go to frontend folder: npm install
* start vue.js: npm run serve
* docker-compose up
* open http://127.0.0.1:8000/

********
Contributions
********
* How to contribute
* Code of Conduct


********
TO DO
********
* Manage international taxs
* Create PDF Invoice and Delivery PDF receipt
* Create more documentations

********
Commercial support
********

For any commercial support to install D-Shop, fix bugs or develop new features you can request for a quote https://dshop-ecommerce.com/#section-askademo
