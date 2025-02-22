import random, string
from datetime import date
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class Customer(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    mobile = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    post_code = models.CharField(max_length=10, blank=True)
    points = models.IntegerField(blank=True, default=0)
    voucher = models.IntegerField(blank=True, default=0)
    
    # subscription
    premium = models.BooleanField(default=False, blank=False)
    premium_issued_date = models.DateField(blank=True, null=True)

    # reserved fields for potential future expansion
    undefined_1 = models.CharField(max_length=200, blank=False)
    undefined_2 = models.CharField(max_length=200, blank=False)
    undefined_3 = models.CharField(max_length=200, blank=False)
    undefined_4 = models.CharField(max_length=200, blank=False)
    undefined_5 = models.CharField(max_length=200, blank=False)
    undefined_6 = models.CharField(max_length=200, blank=False)
    undefined_7 = models.CharField(max_length=200, blank=False)
    undefined_8 = models.CharField(max_length=200, blank=False)
    undefined_9 = models.CharField(max_length=200, blank=False)
    undefined_10 = models.CharField(max_length=200, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def count_voucher(self):
        try:
            tickets = self.points//100
            if tickets:
                self.points = self.points - tickets*100
                self.voucher += tickets
                self.save()
                return f"Current number of vouchers: {self.voucher} and current points: {self.points}"
            else:
                return f"Current points: {self.points}"
        except:
            print('points error')

    def premium_check(self):
        today = date.today()
        if self.premium_issued_date - today < 0:
            self.premium = False
            self.premium_issued_date = None
            print("updated member to be non premium member")
            return

    def save(self, *args, **kwargs):
        if self.pk is None or not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        
        elif self.pk:
            # member's premium control
            if self.premium: 
                if not self.premium_issued_date:
                    self.premium_issued_date = date.today()
                elif self.premium_issued_date:
                    if self.premium_issued_date - date.today() < 0:
                        pass
            elif not self.premium and self.premium_issued_date:
                self.premium_issued_date = None
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    brand = models.CharField(max_length=50, blank=True)
    price = models.FloatField(max_length=50, blank=False)
    cost = models.FloatField(max_length=50, blank=False)
    amount = models.CharField(max_length=50, blank=False)
    color = models.CharField(max_length=50, blank=True)
    stream = models.CharField(max_length=50, blank=True)
    section = models.CharField(max_length=50, blank=True)
    bar_code = models.CharField(max_length=50, blank=True)

    # reserved fields for potential future expansion
    undefined_1 = models.CharField(max_length=200, blank=False)
    undefined_2 = models.CharField(max_length=200, blank=False)
    undefined_3 = models.CharField(max_length=200, blank=False)
    undefined_4 = models.CharField(max_length=200, blank=False)
    undefined_5 = models.CharField(max_length=200, blank=False)
    undefined_6 = models.CharField(max_length=200, blank=False)
    undefined_7 = models.CharField(max_length=200, blank=False)
    undefined_8 = models.CharField(max_length=200, blank=False)
    undefined_9 = models.CharField(max_length=200, blank=False)
    undefined_10 = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.name

    
    def stock_status(self): 
        if self.amount <= 0:
            return "Unavaliable"
        else:
            return "Avaliable"
    
class OrderStatus(models.IntegerChoices):
    CANCELED = 0, "Canceled"
    PROCESSING = 1, "Processing"
    SHIPPED = 2, "Shipped"
    COLLECTED = 3, "Collected"

class Order(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    items = models.ForeignKey(Product, on_delete=models.CASCADE)
    serial_unmber = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    mobile = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=200, blank=False)
    post_code = models.CharField(max_length=10, blank=False)
    total_amount = models.FloatField(max_length=100, blank=False)
    order_status = models.IntegerField(choices=OrderStatus.choices, default=OrderStatus.PROCESSING)
    order_canceled = models.BooleanField(default=False, blank=False)

    # reserved fields for potential future expansion
    undefined_1 = models.CharField(max_length=200, blank=False)
    undefined_2 = models.CharField(max_length=200, blank=False)
    undefined_3 = models.CharField(max_length=200, blank=False)
    undefined_4 = models.CharField(max_length=200, blank=False)
    undefined_5 = models.CharField(max_length=200, blank=False)
    undefined_6 = models.CharField(max_length=200, blank=False)
    undefined_7 = models.CharField(max_length=200, blank=False)
    undefined_8 = models.CharField(max_length=200, blank=False)
    undefined_9 = models.CharField(max_length=200, blank=False)
    undefined_10 = models.CharField(max_length=200, blank=False)
    

    def save(self):
        if not self.serial_unmber:
            # generate new serial number
            date_part = now().strftime("%Y%m%d")
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.serial_unmber = f"CCOR-{date_part}-{random_part}"
            self.customer.points += int(self.total_amount)
            self.save()
            print(f"{self.serial_unmber}_has been placed")
            return f"Order number: {self.serial_unmber}, has been placed"

        if self.serial_unmber and self.order_canceled:
            self.customer.points -= int(self.total_amount)
            if self.customer.points < 0:
                self.customer.voucher -= 1
                self.customer.points += 100
            self.order_canceled = True
            self.order_status = 0
            self.save()
            print(f"{self.serial_unmber}_has been canceled")
            return f"Order number: {self.serial_unmber}, has been canceled"