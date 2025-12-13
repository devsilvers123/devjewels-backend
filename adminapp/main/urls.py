from django.urls import path
from .views import AnnouncementListView, BannerListView, ActiveSaleBannerView, TestimonialListView, WhatsAppLinkView, ProductListView, ProductDetailView, CategoryListView, FAQListView, SizeGuideListView, ValidatePromoCodeView
from .views import APIRootView

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('announcements/', AnnouncementListView.as_view(), name='announcement-list'),
    path('banners/', BannerListView.as_view(), name='banner-list'),
    path('sale-banner/', ActiveSaleBannerView.as_view(), name='sale-banner'),
    path('testimonials/', TestimonialListView.as_view(), name='testimonial-list'),
    path('social/whatsapp-group/', WhatsAppLinkView.as_view(), name='whatsapp-group-link'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('faqs/', FAQListView.as_view(), name='faq-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('size-guide/', SizeGuideListView.as_view(), name='size-guide'),
    path('validate-promo/', ValidatePromoCodeView.as_view(), name='validate-promo'),
]
