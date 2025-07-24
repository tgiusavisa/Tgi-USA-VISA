from django.db import models
from tinymce.models import HTMLField
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User  # Add this import



class Details(models.Model):
    title = models.CharField(max_length=200, default="Website Details" )

    class Meta:
        verbose_name = "About Us Page"
        verbose_name_plural = "About Us Page"

    def __str__(self):
        return self.title

class AboutUs(models.Model):
    details = models.ForeignKey(Details, on_delete=models.CASCADE, related_name='about_us', null=True, blank=True)
    image = models.ImageField(upload_to='about_us/,', null=True, blank=True)
    heading = models.CharField(max_length=200, default='', null=True, blank=True)
    description = HTMLField()

    class Meta:
        verbose_name_plural = "About Us"

    def __str__(self):
        return self.heading


class OurMission(models.Model):
    details = models.ForeignKey(Details, on_delete=models.CASCADE, related_name='our_mission', null=True, blank=True)
    image = models.ImageField(upload_to='our_mission/')
    heading = models.CharField(max_length=200)
    description = HTMLField()

    class Meta:
        verbose_name_plural = "Our Mission"

    def __str__(self):
        return self.heading


class OurVision(models.Model):
    details = models.ForeignKey(Details, on_delete=models.CASCADE, related_name='Our_vision', null=True, blank=True)
    image = models.ImageField(upload_to='our_vision/')
    heading = models.CharField(max_length=200)
    description = HTMLField()

    class Meta:
        verbose_name_plural = "Our Vision"

    def __str__(self):
        return self.heading


class OurGoals(models.Model):
    details = models.ForeignKey(Details, on_delete=models.CASCADE, related_name='our_goals', null=True, blank=True)
    image = models.ImageField(upload_to='our_goals/')
    heading = models.CharField(max_length=200)
    description = HTMLField()

    class Meta:
        verbose_name_plural = "Our Goals"

    def __str__(self):
        return self.heading

class Visa(models.Model):
    heading1 = models.CharField(max_length=200)
    heading2 = models.CharField(max_length=200, blank=True, null=True)
    description = HTMLField()
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    onetime_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    img = models.ImageField(upload_to='visa_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.heading1)
            slug = base_slug
            counter = 1
            while Visa.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.heading1
    
class Home(models.Model):
    title = models.CharField(max_length=200, default="Website Home Page" )

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Page"

    def __str__(self):
        return self.title

class AboutUshome(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='about_us', null=True, blank=True)
    image = models.ImageField(upload_to='about_us/')
    heading = models.CharField(max_length=200)
    description = HTMLField()

    class Meta:
        verbose_name_plural = "About Us"

    def __str__(self):
        return self.heading


class OurMissionhome(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='our_mission', null=True, blank=True)
    image = models.ImageField(upload_to='our_mission/')
    heading = models.CharField(max_length=200)
    description = HTMLField()

    class Meta:
        verbose_name_plural = "Our Mission"

    def __str__(self):
        return self.heading


class OurVisionhome(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='Our_vision', null=True, blank=True)
    image = models.ImageField(upload_to='our_vision/')
    heading = models.CharField(max_length=200)
    description = HTMLField()

    class Meta:
        verbose_name_plural = "Our Vision"

    def __str__(self):
        return self.heading


class OurGoalshome(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='our_goals', null=True, blank=True)
    image = models.ImageField(upload_to='our_goals/')
    heading = models.CharField(max_length=200)
    description = HTMLField()

    class Meta:
        verbose_name_plural = "Our Goals"

    def __str__(self):
        return self.heading

class faqshome(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='faq', null=True, blank=True)
    heading = models.CharField(max_length=200)
    description = HTMLField()

    class Meta:
        verbose_name_plural = "FAQ's"

    def __str__(self):
        return self.heading

class highlightshome(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='highlights', null=True, blank=True)
    number = models.CharField(max_length=100, default="", blank=False, null=False)
    heading = models.CharField(max_length=300, default="", blank=False, null=False)

    class Meta:
        verbose_name_plural = "Highlights"

    def __str__(self):
        return self.heading

class HeroSlider(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='hero_sliders', null=True, blank=True)
    image = models.ImageField(upload_to='hero_slider/')
    heading = models.CharField(max_length=200)
    subheading = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Hero Slider"
        verbose_name_plural = "Hero Sliders"
        ordering = ['order']
    
    def __str__(self):
        return self.heading
    
class policy(models.Model):
    heading = models.CharField(max_length=200)
    description = HTMLField()   

class Visitor(models.Model):
    count = models.PositiveIntegerField(default=0, verbose_name="Visitor Count")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Total Visitors: {self.count}"
    
    @classmethod
    def increment_count(cls):
        # Get or create the single visitor record
        visitor, created = cls.objects.get_or_create(pk=1)
        visitor.count += 1
        visitor.save()
        return visitor.count