from django import forms


class StripeCreateProduct(forms.Form):
    """Current fields:
    product_name, product_description, product_price, product_currency, product_shippable,
    product_dim_height, product_dim_length, product_dim_width, product_dim_weight"""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "label_suffix", ""
        )  # Set the default label suffix to an empty string
        super(StripeCreateProduct, self).__init__(*args, **kwargs)

    product_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Product name", "size": 40}),
        required=True,
    )

    product_description = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Product description", "cols": 40},
        ),
        required=True,
    )

    # product_description = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={"placeholder": "Product description", "size": 40}
    #     ),
    #     required=True,
    # )

    product_price = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Product price"},
        ),
        required=True,
    )

    product_currency = forms.ChoiceField(
        choices=[
            ("jpy", "JPY"),
            ("usd", "USD"),
            ("eur", "EUR"),
        ]
    )

    product_shippable = forms.BooleanField(
        label="The product can be shipped (check = yes)",
        required=False,
    )

    product_dim_height = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Height",
                "size": "4rem",
            },
        ),
        required=False,
    )

    product_dim_length = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Length",
                "size": "4rem",
            },
        ),
        required=False,
    )

    product_dim_width = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Width",
                "size": "4rem",
            },
        ),
        required=False,
    )

    product_dim_weight = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Weight",
                "size": "4rem",
            },
        ),
        required=False,
    )


"""
STRIPE product object
{
  "id": "prod_NWjs8kKbJWmuuc",
  "object": "product",
  "active": true,
  "created": 1678833149,
  "default_price": null,
  "description": null,
  "images": [],
  "marketing_features": [],
  "livemode": false,
  "metadata": {},
  "name": "Gold Plan",
  "package_dimensions": null,
        (nullable dictionary)
        {"height": 0.0, "length": 0.0, "weight": 0.0, "width": 0.0}
        package_dimensions.heightfloat -> Height, in inches.
        package_dimensions.lengthfloat -> Length, in inches.
        package_dimensions.weightfloat -> Weight, in ounces.
        package_dimensions.widthfloat -> Width, in inches.
  "shippable": null,
  "statement_descriptor": null,
  "tax_code": null,
  "unit_label": null,
  "updated": 1678833149,
  "url": null
}
"""
