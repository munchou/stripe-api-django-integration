from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import stripe

currencies_cents = ["jpy"]


def stripe_add_commas_to_num(number, currency):
    pos = 1
    result = ""
    decimals = ""
    if currency not in currencies_cents:
        number = int(number) / 100
        number, decimals = str(number).split(".")[0], str(number).split(".")[1]
        if decimals != "0" and len(decimals) == 1:
            decimals = f"{decimals}0"

    for char in str(number)[::-1]:
        if pos == 4:  # the number is read in reverse so the comma is added before
            result += f",{char}"
            pos = 1
        else:
            result += char
        pos += 1

    return (
        f"{result[::-1]}.{decimals}"
        if currency not in currencies_cents and decimals != "0"
        else result[::-1]
    )


def stripe_home(request):
    return render(request, "stripe_payment/stripe_home.html")


def stripe_customer(request):
    stripe.api_key = settings.STRIPE_SK_TEST_KEY

    products = stripe.Product.list(limit=100, active=True)
    products_prices = {}

    for product in products:
        if product.active:
            try:
                product_price = stripe.Price.retrieve(product.default_price)
                products_prices[product.id] = [
                    stripe_add_commas_to_num(
                        product_price.unit_amount, product_price.currency
                    ),
                    product_price.currency.upper(),
                ]
            except Exception as e:
                product_price = None
                products_prices[product.id] = [
                    None,
                    None,
                ]

    context = {
        "products": products,
        "products_prices": products_prices,
    }

    return render(request, "stripe_payment/stripe_customer.html", context)


def stripe_admin(request):
    from app.forms import StripeCreateProduct

    stripe.api_key = settings.STRIPE_SK_TEST_KEY

    if request.method == "POST":
        createproduct_form = StripeCreateProduct(request.POST)

        if createproduct_form.is_valid():
            if "create-product" in request.POST:
                product_name = createproduct_form.cleaned_data["product_name"]
                product_description = createproduct_form.cleaned_data[
                    "product_description"
                ]
                product_price = createproduct_form.cleaned_data["product_price"]
                product_currency = createproduct_form.cleaned_data["product_currency"]
                product_shippable = createproduct_form.cleaned_data["product_shippable"]

                product_dimensions_input = [
                    createproduct_form.cleaned_data["product_dim_height"],
                    createproduct_form.cleaned_data["product_dim_length"],
                    createproduct_form.cleaned_data["product_dim_width"],
                    createproduct_form.cleaned_data["product_dim_weight"],
                ]

                try:
                    for dim_input in product_dimensions_input:
                        dim_input = float(dim_input)
                    product_dimensions = {
                        "height": float(
                            createproduct_form.cleaned_data["product_dim_height"]
                        ),
                        "length": float(
                            createproduct_form.cleaned_data["product_dim_length"]
                        ),
                        "weight": float(
                            createproduct_form.cleaned_data["product_dim_weight"]
                        ),
                        "width": float(
                            createproduct_form.cleaned_data["product_dim_width"]
                        ),
                    }

                except Exception as e:
                    product_dimensions = None

                if (
                    "." in product_price
                    and product_price.count(".") <= 1
                    and product_currency not in currencies_cents
                ):
                    product_price = (
                        f'{product_price.split(".")[0]}{product_price.split(".")[1]}'
                    )

                if product_price.isdigit():
                    new_product = stripe.Product.create(
                        name=product_name,
                        description=product_description,
                        shippable=product_shippable,
                        package_dimensions=product_dimensions,
                        # metadata=product_metadata,
                    )

                    new_product_price = stripe.Price.create(
                        product=new_product.id,
                        unit_amount=product_price,
                        currency=product_currency,
                    )
                    stripe.Product.modify(
                        new_product.id,
                        default_price=new_product_price.id,
                    )

    balance = stripe.Balance.retrieve()
    balance_pending_amount = stripe_add_commas_to_num(
        balance["pending"][0]["amount"], "jpy"
    )
    balance_pending_currency = balance["pending"][0]["currency"].upper()
    products = stripe.Product.list(limit=100, active=True)
    products_archived = len(stripe.Product.list(limit=100, active=False))

    products_active = len(products)
    products_prices = {}

    for product in products:
        try:
            product_price = stripe.Price.retrieve(product.default_price)
            products_prices[product.id] = [
                stripe_add_commas_to_num(
                    product_price.unit_amount, product_price.currency
                ),
                product_price.currency.upper(),
            ]
        except Exception as e:
            product_price = None
            products_prices[product.id] = [
                None,
                None,
            ]

    createproduct_form = StripeCreateProduct()

    context = {
        "createproduct_form": createproduct_form,
        "balance": balance,
        "balance_pending_amount": balance_pending_amount,
        "balance_pending_currency": balance_pending_currency,
        "products": products,
        "products_prices": products_prices,
        "products_active": products_active,
        "products_archived": products_archived,
    }

    return render(request, "stripe_payment/stripe_admin.html", context)


def stripe_product_update(request, product_id):
    from app.forms import StripeCreateProduct

    stripe.api_key = settings.STRIPE_SK_TEST_KEY

    current_product = stripe.Product.retrieve(product_id)
    current_product_currency = stripe.Price.retrieve(
        current_product.default_price
    ).currency
    current_product_price = stripe.Price.retrieve(
        current_product.default_price
    ).unit_amount

    if request.method == "POST":
        createproduct_form = StripeCreateProduct(request.POST)
        if createproduct_form.is_valid():
            if "update-product" in request.POST:
                product_name = createproduct_form.cleaned_data["product_name"]
                product_description = createproduct_form.cleaned_data[
                    "product_description"
                ]
                product_price = createproduct_form.cleaned_data["product_price"]
                product_currency = createproduct_form.cleaned_data["product_currency"]
                product_shippable = createproduct_form.cleaned_data["product_shippable"]

                product_dimensions_input = [
                    createproduct_form.cleaned_data["product_dim_height"],
                    createproduct_form.cleaned_data["product_dim_length"],
                    createproduct_form.cleaned_data["product_dim_width"],
                    createproduct_form.cleaned_data["product_dim_weight"],
                ]

                try:
                    for dim_input in product_dimensions_input:
                        dim_input = float(dim_input)
                    product_dimensions = {
                        "height": float(
                            createproduct_form.cleaned_data["product_dim_height"]
                        ),
                        "length": float(
                            createproduct_form.cleaned_data["product_dim_length"]
                        ),
                        "weight": float(
                            createproduct_form.cleaned_data["product_dim_weight"]
                        ),
                        "width": float(
                            createproduct_form.cleaned_data["product_dim_width"]
                        ),
                    }

                except Exception as e:
                    product_dimensions = None

                if (
                    "." in product_price
                    and product_price.count(".") <= 1
                    and product_currency not in currencies_cents
                ):
                    product_price = (
                        f'{product_price.split(".")[0]}{product_price.split(".")[1]}'
                    )

                if product_price.isdigit():
                    updated_product = stripe.Product.modify(
                        product_id,
                        name=product_name,
                        description=product_description,
                        shippable=product_shippable,
                        package_dimensions=product_dimensions,
                    )

                    if (
                        str(current_product_price) != product_price
                        or current_product_currency != product_currency
                    ):
                        new_price = stripe.Price.create(
                            product=product_id,
                            unit_amount=product_price,
                            currency=product_currency,
                        )

                        updated_product = stripe.Product.modify(
                            product_id,
                            default_price=new_price.id,
                        )

            return redirect("stripe_product_update", product_id)

    if current_product_currency not in currencies_cents:
        current_product_price = current_product_price / 100

    if current_product.package_dimensions:
        current_product_height = current_product.package_dimensions["height"]
        current_product_length = current_product.package_dimensions["length"]
        current_product_width = current_product.package_dimensions["width"]
        current_product_weight = current_product.package_dimensions["weight"]
    else:
        current_product_height = current_product_length = current_product_width = (
            current_product_weight
        ) = None

    createproduct_form = StripeCreateProduct(
        {
            "product_name": current_product.name,
            "product_description": current_product.description,
            "product_price": current_product_price,
            "product_currency": current_product_currency,
            "product_shippable": current_product.shippable,
            "product_dim_height": current_product_height,
            "product_dim_length": current_product_length,
            "product_dim_width": current_product_width,
            "product_dim_weight": current_product_weight,
        }
    )

    context = {
        "createproduct_form": createproduct_form,
        "product_id": product_id,
    }

    return render(request, "stripe_payment/stripe_product_update.html", context)


def stripe_product_archive(request, product_id):
    stripe.api_key = settings.STRIPE_SK_TEST_KEY

    if request.method == "POST":
        action = request.POST["product"]
        if action == "archive-product":
            stripe.Product.modify(
                product_id,
                active=False,
            )

    return redirect("stripe_admin")


def stripe_checkout(request, product_id):
    stripe.api_key = settings.STRIPE_SK_TEST_KEY

    product = stripe.Product.retrieve(product_id)
    product_price_object = stripe.Price.retrieve(product.default_price)
    product_price_id = product_price_object.id
    product_price = stripe.Price.retrieve(product.default_price)

    if request.method == "GET":
        action = request.GET["product"]
        product_quantity = request.GET["product_quantity"]

        if action == "buy-product":
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": product_price_id,
                        "quantity": product_quantity,
                    }
                ],
                mode=(
                    "payment"
                    if product_price_object.type == "one_time"
                    else "subscription"
                ),
                success_url=request.build_absolute_uri(
                    reverse(
                        "stripe_success",
                        args=[
                            product.name,
                            product_quantity,
                            str(int(product_price.unit_amount) * int(product_quantity)),
                        ],
                    )
                ),
                cancel_url=request.build_absolute_uri(
                    reverse(
                        "stripe_cancel",
                        args=[
                            product.name,
                            str(int(product_price.unit_amount) * int(product_quantity)),
                        ],
                    ),
                ),
            )
            return redirect(checkout_session.url, code=303)

    return redirect("stripe_home")


def stripe_success(request, product, qty, paid_amount):
    return render(
        request,
        "stripe_payment/stripe_success.html",
        {
            "product": product,
            "quantity": qty,
            "paid_amount": paid_amount,
        },
    )


def stripe_cancel(request, product, product_amount):
    return render(
        request,
        "stripe_payment/stripe_cancel.html",
        {
            "product": product,
            "product_amount": product_amount,
        },
    )
