##########
D-Shop - Simple e-commerce platform build with Django, Django-CMS and Vue.JS
##########
Created by `D-Modules <https://www.d-modules.com>`_


Open source platform to build simple but robust e-commerce website using Python.

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
Configurations
********

Lorem ipsum

********
Installation with Docker
********

git clone git@github.com:dmodules/d-shop.git
cd d-shop
docker-compose build
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
download media for demo https://test.com/
copy media in data/media
import db for demo: cat demo_data.sql | docker exec -i your-db-container psql -U postgres
docker-compose up
open http://127.0.0.1:8000/

********
Commercial support
********

For any commercial support to install D-Shop, fix bugs or develop new features you can request for a quote https://dshop-ecommerce.com/#section-askademo
