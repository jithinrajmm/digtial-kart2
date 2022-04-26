from django.db import models
from category.models import Category
from store.models import Product
import datetime
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class Admin(models.Model):
    
    admin_name = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    is_logedinn = models.BooleanField(default=False)

    @property
    def loginornot(self):
        return self.is_logedin


    def admin_authenticate(self,name,password):
        if self.admin_name == name and self.password == password:
            self.is_logedinn = True
            return True
        else:
            return False

    def admin_logout(self):
        self.is_logedin = False
    
    def __str__(self):
        return self.admin_name


# category offer
class CategoryOffer(models.Model):

    now = datetime.date.today()

    category = models.OneToOneField(Category,related_name='catoffer',on_delete=models.CASCADE)
    offer_percentage = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(50)])
    valid_from = models.DateField()
    valid_to = models.DateField()
    active = models.BooleanField(blank=True,null=True)

    def __str__(self):
        return self.category.category_name


    @property
    def category_offer_check(self):

        if self.valid_from < self.now and self.valid_to >self.now and self.active == True  :
            return True
        else:
            return False
    def category_offer_price(self,product):

        if self.category_offer_check:
            return (product.price) - (product.price) * (self.offer_percentage /100)
        else:
            return (product.price)


class ProductOffer(models.Model):

    now = datetime.date.today()

    product = models.OneToOneField(Product,related_name='product_off',on_delete=models.CASCADE)
    offer_percentage = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(50)])
    valid_from = models.DateField()
    valid_to = models.DateField()
    active = models.BooleanField(blank=True,null=True)

    def __str__(self):
        return self.product.product_name

    @property
    def product_offer_check(self):

        if self.valid_from < self.now and self.valid_to >self.now and self.active == True :
            return True
        else:
            return False

    def product_offer_price(self,product):

        if self.product_offer_check:
            return (product.price) - (product.price) * (self.offer_percentage /100)
        else:
            return (product.price)




