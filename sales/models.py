from django.db import models
from django.shortcuts import reverse
from django.utils.timezone import timezone
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from .utils import generate_code
# Create your models here.
class Position(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField()
    price=models.FloatField(blank=True)
    created=models.DateTimeField(blank=True)
    
    def save(self, *args, **kwargs):
        self.price =self.product.price * self.quantity
        return super(Position, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"id: {self.id} product: {self.product.name} quantity: {self.quantity}"
    
    def get_sale_id(self):
        sale_obj=self.sale_set.first()
        return sale_obj.id
class Sale(models.Model):
    transaction_id=models.CharField(max_length=12, blank=True)
    positions =models.ManyToManyField(Position)
    total_price=models.FloatField(blank=True, null=True)
    customer =models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman=models.ForeignKey(Profile, on_delete=models.CASCADE)
    created =models.DateTimeField(blank=True)
    updated =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Sales for amount: {self.total_price}"
    
    def save(self, *args, **kwargs):
        if (self.transaction_id==""):
            self.transaction_id = generate_code()
        if(self.created==""):
            self.created=timezone.now()  
        return super(Sale, self).save(*args, **kwargs)
    
    def get_postions(self):
        return self.positions.all()

    def get_absolute_url(self):
        return reverse("sales:sale-details", kwargs={"pk": self.pk})
    

class CSV(models.Model):
    file_name = models.CharField(max_length=120, null=True)
    csv_file= models.FileField(upload_to='csvs', null=True)
    created =models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file_name

    