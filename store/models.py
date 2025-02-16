import random, string
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50, blank=False)
    mobile = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=200, blank=False)
    post_code = models.CharField(max_length=10, blank=False)
    points = models.IntegerField(max_length=50, blank=True)
    voucher = models.CharField(max_length=50, blank=True)
    
    # subscription
    premium = models.BooleanField(default=False, blank=False)
    premium_issued_date = models.DateField(max_length=50, blank=True)

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

    def stock_status(self): 
        if self.amount <= 0:
            return "Unavaliable"
        else:
            return "Avaliable"
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL)
    serial_unmber = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    mobile = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=200, blank=False)
    post_code = models.CharField(max_length=10, blank=False)
    total_amount = models.FloatField(max_length=100, blank=False)
    order_status = models.Choices(max_length=5,
                                  value={0 : "canceled", 
                                         1 : "processing", 
                                         2 : "shipped", 
                                         3 : "collected"}, default=1)
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