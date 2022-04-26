
from django.db import models
from category.models import Category
from PIL import Image
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    ''' this is the product models '''
    
    product_name = models.CharField(max_length=100,unique=True)
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    slug = models.CharField(max_length=100,unique=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    description = models.TextField(max_length=500)
    image_1 = models.ImageField(upload_to='products/',max_length=500)
    image_2 = models.ImageField(upload_to='products/',max_length=500)
    image_3 = models.ImageField(upload_to='products/',max_length=500)
    image_4 = models.ImageField(upload_to='products/',max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def save(self,*args,**kargs):
        super(Product,self).save(*args,**kargs)
        image2= Image.open(self.image_2)

        if image2.height>500 or image2.width > 500:
            output_size = (500,500)
            image2.thumbnail(output_size)
            image2.save(self.image_2.path)

    def __str__(self):
        return self.product_name
    def get_url(self):
        return reverse('store:single_product',args=[self.category.category_slug,self.slug])
    
        


    class Meta:
        db_table = 'Product'
        ordering = ['-created',]
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    
