from django.urls import path, include
from rest_framework import routers

from payroll.views import EmployeeViewSet, TaxCodeViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"employees", EmployeeViewSet)
router.register(r"taxcodes", TaxCodeViewSet)
