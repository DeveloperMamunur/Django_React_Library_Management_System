from django.db import models
from branch.models import Branch


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Item(models.Model):
    ITEM_TYPES = [
        ('book', 'Book'),
        ('ebook', 'E-Book'),
        ('journal', 'Journal'),
        ('magazine', 'Magazine')
    ]
    
    CLASSIFICATION_SYSTEMS = [
        ('dewey', 'Dewey Decimal'),
        ('loc', 'Library of Congress'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500, blank=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES, default='book')
    isbn = models.CharField(max_length=20, blank=True, db_index=True)
    issn = models.CharField(max_length=20, blank=True)
    authors = models.ManyToManyField(Author, related_name='items')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    
    categories = models.ManyToManyField(Category, related_name='items')
    classification_system = models.CharField(max_length=20, choices=CLASSIFICATION_SYSTEMS, default='dewey')
    classification_number = models.CharField(max_length=50, blank=True)

    pages = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, default='English')
    cover_image = models.ImageField(upload_to='item_covers/', null=True, blank=True)

    digital_file = models.FileField(upload_to='digital_items/', null=True, blank=True)
    file_size_mb = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    description = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def available_copies(self):
        return self.copies.filter(status='available').count()


class Copy(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('checked_out', 'Checked Out'),
        ('reserved', 'Reserved'),
        ('damaged', 'Damaged'),
        ('lost', 'Lost'),
        ('in_repair', 'In Repair'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='copies')
    barcode = models.CharField(max_length=100, unique=True, db_index=True)
    rfid_tag = models.CharField(max_length=100, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=200, help_text="Shelf location")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    condition = models.CharField(max_length=100, blank=True)
    acquisition_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.item.title} - {self.barcode}"
    
    class Meta:
        verbose_name_plural = "Copies"
