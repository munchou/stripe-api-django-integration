from django.urls import path
import app.stripe_payment_api

app_name = ""

urlpatterns = [
    path(
        "stripe_payment/",
        app.stripe_payment_api.stripe_home,
        name="stripe_home",
    ),
    path(
        "stripe_customer/",
        app.stripe_payment_api.stripe_customer,
        name="stripe_customer",
    ),
    path(
        "stripe_admin/",
        app.stripe_payment_api.stripe_admin,
        name="stripe_admin",
    ),
    path(
        "stripe_product_update/<product_id>/",
        app.stripe_payment_api.stripe_product_update,
        name="stripe_product_update",
    ),
    path(
        "stripe_product_archive/<product_id>/",
        app.stripe_payment_api.stripe_product_archive,
        name="stripe_product_archive",
    ),
    path(
        "stripe_checkout/<product_id>/",
        app.stripe_payment_api.stripe_checkout,
        name="stripe_checkout",
    ),
    path(
        "stripe_payment/success/<product>/<qty>/<paid_amount>/",
        app.stripe_payment_api.stripe_success,
        name="stripe_success",
    ),
    path(
        "stripe_payment/cancel/<product>/<product_amount>/",
        app.stripe_payment_api.stripe_cancel,
        name="stripe_cancel",
    ),
]
