from django.contrib.auth.models import User
from django.db import models


class Executor(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.TextField(max_length=50)
    second_name = models.TextField(max_length=50, null=True, blank=True)
    last_name = models.TextField(max_length=50)
    image = models.ImageField(null=True, blank=True)
    phone = models.TextField(max_length=20)
    about = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Client(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.TextField(max_length=50)
    second_name = models.TextField(max_length=50, null=True, blank=True)
    last_name = models.TextField(max_length=50)
    image = models.ImageField(null=True, blank=True)
    phone = models.TextField(max_length=20)
    about = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Categories(models.Model):
    id = models.BigAutoField(primary_key=True)
    categoty = models.TextField(max_length=50)

    def __str__(self):
        return str(self.id)


class Trade(models.Model):
    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    about = models.TextField(max_length=250)

    def __str__(self):
        return str(self.id)


class Total_Trade(models.Model):
    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE)
    price = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    about = models.TextField(max_length=250)

    def __str__(self):
        return str(self.id)


class E_Trade(models.Model):
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return str(self.executor)


class E_Category(models.Model):
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.executor)


class Donate(models.Model):
    executor = models.ForeignKey(Executor, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return str(self.executor)
