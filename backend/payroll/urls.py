from django.urls import path, include
from rest_framework import routers

from payroll import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"employees", views.EmployeeViewSet)
router.register(r"employee-history", views.EmployeeHistoryViewSet, "employee-history")
router.register(r"employee-custom-fields", views.EmployeeCustomFieldViewSet)
router.register(r"employee-custom-field-values", views.EmployeeCustomFieldValueViewSet)
router.register(r"tax-codes", views.TaxCodeViewSet)
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
router.register(r"rosters", views.RosterViewSet)
router.register(r"roster-employees", views.RosterEmployeeViewSet)
router.register(r"roster-shifts", views.RosterShiftViewSet)
router.register(r"shifts", views.ShiftViewSet)
router.register(r"transactions", views.TransactionViewSet)
# router.register(
#     r"transaction-accumulators",
#     views.TransactionAccumulatorViewSet,
#     "transaction-accumulators",
# )

urlpatterns = [
    path("", include(router.urls)),
]
