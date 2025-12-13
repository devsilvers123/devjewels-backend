from django.contrib import admin
from django.db import models
from .models import Announcement, Banner, SaleBanner, Testimonial, SocialLink, Product, Category, ProductImage, FAQ, FAQCategory, SizeGuideCategory, PromoCode
from django_json_widget.widgets import JSONEditorWidget
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_active', 'created_at')
    list_editable = ('is_active',)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('heading', 'order', 'is_active')
    list_editable = ('order', 'is_active')

@admin.register(SaleBanner)
class SaleBannerAdmin(admin.ModelAdmin):
    list_display = ('label', 'ends_at', 'is_active', 'is_expired_display')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')
    
    def is_expired_display(self, obj):
        return obj.is_expired
    is_expired_display.boolean = True
    is_expired_display.short_description = "Expired?"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'location', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('rating', 'is_active')

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'is_active', 'updated_at')
    list_editable = ('is_active',)
    list_filter = ('platform', 'is_active')

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_sale_active')
    list_filter = ('category', 'is_sale_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'description', 'specifications')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_percent', 'stock')
        }),
        ('Social Proof', {
            'fields': ('rating', 'reviews_count')
        }),
        ('Sale Configuration', {
            'fields': ('is_sale_active', 'sale_label', 'sale_ends_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    inlines = [FAQInline]

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('category', 'is_active')

@admin.register(SizeGuideCategory)
class SizeGuideCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'is_active', 'valid_to')
    list_filter = ('is_active', 'discount_type')
    search_fields = ('code',)