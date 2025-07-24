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
    image = models.ImageField(upload_to='about_us/')
    heading = models.CharField(max_length=200)
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

class BookingDetail(models.Model):
    full_name = models.CharField(max_length=255)
    passport_id = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    passport_image = models.ImageField(
        upload_to='passport_images/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        null=True, blank=True
    )

    def __str__(self):
        return self.full_name

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Under Process', 'Under Process'),
        ('Accepted', 'Accepted'),
        # ('Received', 'Didn\'t Receive Payment'),
    ]
    
    booking = models.OneToOneField(
        BookingDetail, 
        on_delete=models.CASCADE,
        related_name='payment',
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    payment_proof = models.ImageField(upload_to='payment_proofs/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='Under Process'
    )

    def __str__(self):
        return f"{self.full_name} - {self.payment_status}"
    
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