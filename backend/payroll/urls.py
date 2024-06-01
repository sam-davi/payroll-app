from django.urls import path, include
from rest_framework import routers

from payroll import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"employees", views.EmployeeViewSet)
router.register(r"employee-history", views.EmployeeHistoryViewSet, "employee-history")
router.register(r"taxcodes", views.TaxCodeViewSet)
router.register(r"allowances", views.AllowanceViewSet)
router.register(r"allowance-types", views.AllowanceTypeViewSet)
router.register(r"accumulators", views.AccumulatorViewSet)
# router.register(
#     r"accumulator-values", views.AccumulatorValueViewSet, "accumulator-values"
# )
router.register(r"allowance-type-accumulators", views.AllowanceTypeAccumulatorViewSet)
router.register(r"pay-groups", views.PayGroupViewSet)
router.register(r"pay-periods", views.PayPeriodViewSet)
router.register(r"rates", views.RateViewSet)
router.register(r"transactions", views.TransactionViewSet)
# router.register(
#     r"transaction-accumulators",
#     views.TransactionAccumulatorViewSet,
#     "transaction-accumulators",
# )

urlpatterns = [
    path("", include(router.urls)),
]
