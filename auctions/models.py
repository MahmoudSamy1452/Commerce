from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):

    class Categories(models.TextChoices):
        ELECTRONICS = 'Electronics'
        TOYS = 'Toys'
        FASHION = 'Fashion'
        HOME = 'Home'
        OTHER = 'Other'

    title = models.CharField(max_length=64)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    photo = models.URLField(blank=True)
    category = models.TextField(
        choices=Categories.choices
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    closed = models.BooleanField()
    watching = models.ManyToManyField(User, blank=True, related_name="watchers")

    def __str__(self):
        return f'{self.title}: {self.description}, {self.base_price}, {self.category}'

class Bid(models.Model):
    Listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name="bidding")
    value = models.DecimalField(max_digits=10, decimal_places=2)
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    def __str__(self):
        return f'{self.Listing.title}: {self.value} by {self.User}'

class Comment(models.Model):
    Listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name="comments")
    content = models.TextField()
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor")

    def __str__(self):
        return f'{self.Listing}: {self.User} - {self.content}'