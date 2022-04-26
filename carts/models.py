
from django.db import models
from store.models import Product
from accounts.models import Account
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.cart_id

class CartItems(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.product_name
    def total_price(self):
        return self.product.price * self.quantity
    def coupon_offer(self,coupon):
        return (self.product.price * self.quantity)-(self.product.price * self.quantity)*(coupon.discount/100)
    def deducted_amount(self,coupon):
        return (self.product.price * self.quantity)*(coupon.discount/100)


class Wishlist(models.Model):
    prouduct = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)

    def __str__(self):
        return self.prouduct.product_name

class Coupon(models.Model):
    ''' this model is used to genarate the coupon based on the date'''
    coupon_code = models.CharField(max_length=50,unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(50)])
    
    active = models.BooleanField()

    def __str__(self):
        return self.coupon_code
    class  Meta:
        ordering = ['-valid_to',]
        



class CouponUsedUsers(models.Model):
    coupon = models.CharField(max_length=50)
    count = models.IntegerField()
    user = models.ForeignKey(Account,on_delete=models.CASCADE)


    def __str__(self):
        return self.coupon
