from rest_framework import serializers
from .models import Announcement, Banner, SaleBanner, Testimonial, SocialLink, Product, Category, ProductImage, FAQ, FAQCategory, SizeGuideCategory

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'text']

class BannerSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
#comment
    class Meta:
        model = Banner
        fields = ['id', 'heading', 'sub_heading', 'image_url', 'order']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
        # build_absolute_uri creates a full URL including domain/port
            return request.build_absolute_uri(obj.image.url)
        return None

class SaleBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleBanner
        fields = ['id', 'label', 'ends_at', 'is_active']

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'location', 'text', 'rating', 'product_name']

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductSerializer(serializers.ModelSerializer):
    # Flatten images to a list of URLs
    images = serializers.SerializerMethodField()
    category = serializers.CharField(source='category.name')
    sale = serializers.SerializerMethodField()
    reviews = serializers.IntegerField(source='reviews_count')

    class Meta:
        model = Product
        fields = [
            'id', 'slug', 'name', 'description', 'price', 
            'discount_percent', 'images', 'category', 
            'rating', 'reviews', 'stock', 'sale', 'specifications'
        ]

    def get_images(self, obj):
        # Return a list of absolute URLs
        request = self.context.get('request')
        images = obj.images.all()
        urls = []
        for img in images:
            if img.image:
                if request:
                    urls.append(request.build_absolute_uri(img.image.url))
                else:
                    urls.append(img.image.url)
        return urls
    
    def get_sale(self, obj):
        if obj.is_sale_active:
            return {
                "enabled": True,
                "label": obj.sale_label,
                "endsAt": obj.sale_ends_at
            }
        return None

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class FAQQuestionSerializer(serializers.ModelSerializer):
    # Rename fields to match your frontend expectations (q, a)
    q = serializers.CharField(source='question')
    a = serializers.CharField(source='answer')

    class Meta:
        model = FAQ
        fields = ['q', 'a']

class FAQCategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='name')
    questions = serializers.SerializerMethodField()

    class Meta:
        model = FAQCategory
        fields = ['category', 'questions']

    def get_questions(self, obj):
        # Only return active questions
        questions = obj.questions.filter(is_active=True).order_by('order')
        return FAQQuestionSerializer(questions, many=True).data
    
class SizeGuideCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeGuideCategory
        fields = ['slug', 'name', 'columns', 'data', 'instruction_title', 'instruction_text']