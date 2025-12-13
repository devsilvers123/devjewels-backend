from rest_framework import generics
from .models import Announcement, Banner, SaleBanner, Testimonial, SocialLink, Product, Category, FAQCategory, SizeGuideCategory
from .serializers import CategorySerializer, ProductSerializer, SizeGuideCategorySerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import AnnouncementSerializer, BannerSerializer, SaleBannerSerializer, TestimonialSerializer, FAQCategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from .models import PromoCode
from decimal import Decimal
from rest_framework.reverse import reverse

class APIRootView(APIView):
    """
    Lists all available API endpoints.
    """
    def get(self, request, format=None):
        return Response({
            'announcements': reverse('announcement-list', request=request, format=format),
            'banners': reverse('banner-list', request=request, format=format),
            'sale-banner': reverse('sale-banner', request=request, format=format),
            'products': reverse('product-list', request=request, format=format),
            'categories': reverse('category-list', request=request, format=format),
            'testimonials': reverse('testimonial-list', request=request, format=format),
            'faqs': reverse('faq-list', request=request, format=format),
            'size-guide': reverse('size-guide', request=request, format=format),
            'whatsapp-link': reverse('whatsapp-group-link', request=request, format=format),
        })
class ValidatePromoCodeView(APIView):
    """
    Validates a promo code and calculates discount.
    POST Payload: { "code": "DEV10", "total_amount": 5000 }
    """
    def post(self, request):
        code = request.data.get('code', '').upper()
        total_amount = Decimal(str(request.data.get('total_amount', 0)))

        try:
            promo = PromoCode.objects.get(code=code)
        except PromoCode.DoesNotExist:
            return Response({"error": "Invalid promo code"}, status=status.HTTP_400_BAD_REQUEST)

        if not promo.is_valid():
            return Response({"error": "Promo code is expired or inactive"}, status=status.HTTP_400_BAD_REQUEST)

        if total_amount < promo.min_order_amount:
            return Response({
                "error": f"Minimum order amount of ₹{promo.min_order_amount} required"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Calculate Discount
        discount = Decimal(0)
        if promo.discount_type == 'percent':
            discount = total_amount * (promo.discount_value / Decimal(100))
            if promo.max_discount_amount:
                discount = min(discount, promo.max_discount_amount)
        else:
            discount = promo.discount_value

        # Ensure discount doesn't exceed total
        discount = min(discount, total_amount)

        return Response({
            "code": promo.code,
            "discount_amount": float(discount),
            "message": "Promo code applied successfully!"
        })

class AnnouncementListView(generics.ListAPIView):
    """
    Returns a list of active scrolling announcements.
    Endpoint: /api/announcements/
    """
    queryset = Announcement.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = AnnouncementSerializer

class BannerListView(generics.ListAPIView):
    """
    Returns a list of active hero banners.
    Endpoint: /api/banners/
    """
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer


class ActiveSaleBannerView(APIView):
    """
    Returns the single active sale banner that hasn't expired yet.
    Endpoint: /api/sale-banner/
    """
    def get(self, request):
        # Find the first active sale that ends in the future
        sale = SaleBanner.objects.filter(
            is_active=True,
            ends_at__gt=timezone.now()
        ).order_by('ends_at').first()  # Get the one ending soonest
        
        if sale:
            serializer = SaleBannerSerializer(sale)
            return Response(serializer.data)
        return Response(None)  # Return null if no active sale exists

class TestimonialListView(generics.ListAPIView):
    """
    Returns list of active testimonials.
    Endpoint: /api/testimonials/
    """
    queryset = Testimonial.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = TestimonialSerializer

class WhatsAppLinkView(APIView):
    """
    Returns the active WhatsApp Group link.
    Endpoint: /api/social/whatsapp-group/
    """
    def get(self, request):
        link = SocialLink.objects.filter(
            platform='whatsapp_group', 
            is_active=True
        ).order_by('-updated_at').first()
        
        if link:
            return Response({'url': link.url})
        return Response({'url': None}) # Explicitly return null if no link found
    
class ProductListView(generics.ListAPIView):
    """
    Lists products with filtering for search, category, and ordering.
    Used by: Collections.tsx
    """
    queryset = Product.objects.prefetch_related('images', 'category').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Enable filtering by fields
    filterset_fields = {
        'category__name': ['exact'],
        'price': ['gte', 'lte'],
    }
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'rating']
    ordering = ['-created_at']  # Default ordering: newest first

class ProductDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single product by slug.
    Used by: ProductDetail.tsx
    """
    queryset = Product.objects.prefetch_related('images', 'category').all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class CategoryListView(generics.ListAPIView):
    """
    Returns list of categories for filter buttons.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class FAQListView(generics.ListAPIView):
    """
    Returns list of FAQ categories with their nested active questions.
    Endpoint: /api/faqs/
    """
    # Prefetch questions to optimize database queries
    queryset = FAQCategory.objects.prefetch_related('questions').all().order_by('order')
    serializer_class = FAQCategorySerializer

class SizeGuideListView(generics.ListAPIView):
    """
    Returns all size guide categories.
    Endpoint: /api/size-guide/
    """
    queryset = SizeGuideCategory.objects.all().order_by('order')
    serializer_class = SizeGuideCategorySerializer