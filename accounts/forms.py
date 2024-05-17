from django.forms import ModelForm
from .models import Customer, Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'   #for specific fields, it would be like : fields = ['customer', 'products']


