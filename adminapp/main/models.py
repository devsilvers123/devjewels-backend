from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Announcement(models.Model):
    """
    Controls the scrolling text at the top of the site.
    React Component: ScrollingBanner
    """
    text = models.CharField(
        max_length=255, 
        help_text="The text to display in the scrolling top bar (e.g., 'Free Shipping')"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Banner(models.Model):
    """
    Controls main hero banners with Headings and Sub-headings.
    """
    heading = models.CharField(max_length=100)
    sub_heading = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='banners/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Order to display banners in")
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.heading

class SaleBanner(models.Model):
    """
    Controls the global sale countdown banner.
    React Component: SaleCountdownBanner
    """
    label = models.CharField(
        max_length=100, 
        help_text="Text to display, e.g., 'Flash Sale! 50% Off Everything'"
    )
    ends_at = models.DateTimeField(
        help_text="When the countdown timer should stop"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this banner immediately"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.label} (Ends: {self.ends_at})"

    @property
    def is_expired(self):
        return timezone.now() > self.ends_at
    
class Testimonial(models.Model):
    name = models.CharField(max_length=100, help_text="Customer's name")
    location = models.CharField(max_length=100, help_text="City or Region (e.g., Mumbai)")
    text = models.TextField(help_text="The review content")
    rating = models.PositiveIntegerField(default=5, help_text="Star rating (1-5)")
    product_name = models.CharField(max_length=200, help_text="Name of the product they purchased")
    
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True, help_text="Optional customer photo")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.rating} Stars"
    

class SocialLink(models.Model):
    """
    Manages social media links like the WhatsApp Group Invite.
    """
    PLATFORM_CHOICES = [
        ('whatsapp_group', 'WhatsApp Group'),
        # ('instagram', 'Instagram'),
        # ('facebook', 'Facebook'),
        # Add others as needed
    ]

    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField(help_text="The full URL (e.g., https://chat.whatsapp.com/...)")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0, help_text="Percentage discount (0-100)")
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)
    reviews_count = models.PositiveIntegerField(default=0)
    
    # Specifications (stored as JSON)
    # Expected format: [{"label": "Material", "value": "Silver"}, ...]
    specifications = models.JSONField(default=list, blank=True)

    # Sale Configuration
    is_sale_active = models.BooleanField(default=False)
    sale_label = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Flash Sale")
    sale_ends_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.product.name}"
    


class FAQCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g., 'Orders & Shipping'")
    order = models.PositiveIntegerField(default=0, help_text="Order to display this category")

    class Meta:
        verbose_name_plural = "FAQ Categories"
        ordering = ['order']

    def __str__(self):
        return self.name

class FAQ(models.Model):
    category = models.ForeignKey(FAQCategory, related_name='questions', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Order within the category")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['order']

    def __str__(self):
        return self.question


class SizeGuideCategory(models.Model):
    """
    Represents a tab in the Size Guide (e.g., 'Rings', 'Bracelets').
    """
    slug = models.SlugField(unique=True, help_text="e.g., 'rings', 'bracelets'")
    name = models.CharField(max_length=100, help_text="Display name e.g., 'Ring Size Chart'")
    order = models.PositiveIntegerField(default=0)
    
    # Table Columns Configuration
    # Example: ["Indian Size", "US Size", "Diameter (mm)"]
    columns = models.JSONField(default=list, help_text="List of column headers ex: ['Indian Size', 'US Size', 'UK Size', 'Diameter (mm)']")
    
    # Table Data
    # Example: [{"col1": "6", "col2": "3", "col3": "14.1"}, ...]
    data = models.JSONField(default=list, help_text="List of row objects ex: [{'Indian Size': '6', 'US Size': '3', 'UK Size': '14.1', 'Diameter (mm)':'14.1'}, ...]")
    
    # Instructions
    instruction_title = models.CharField(max_length=200, default="How to Measure", blank=True)
    instruction_text = models.TextField(blank=True, help_text="Steps or description for measuring")

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Size Guide Categories"

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
    
    # Discount Logic
    discount_type = models.CharField(
        max_length=10, 
        choices=[('percent', 'Percentage'), ('fixed', 'Fixed Amount')],
        default='percent'
    )
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=2, 
        help_text="Enter percentage (e.g. 10 for 10%) or fixed amount (e.g. 500 for ₹500)"
    )
    
    # Constraints
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        help_text="Max cap for percentage discounts (optional)"
    )
    
    # Validity
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.discount_value} ({self.get_discount_type_display()})"

    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.valid_to and now > self.valid_to:
            return False
        if now < self.valid_from:
            return False
        return True
