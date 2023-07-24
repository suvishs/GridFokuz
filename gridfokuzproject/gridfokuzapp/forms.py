from django import forms
from .models import AddProducts
from dal import autocomplete

class AddProductForm(forms.ModelForm):
    Product_Name = forms.ModelChoiceField(
        queryset=AddProducts.objects.all().order_by('Category'),
        widget=autocomplete.ModelSelect2(url='product-autocomplete')
    )

    class Meta:
        model = AddProducts
        fields = '__all__'
