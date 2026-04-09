from django.db import models


class TeamMember(models.Model):
    """About Us sahifasida ko'rsatiladigan jamoa a'zolari (Uch tilda)."""

    greeting_uz = models.CharField(max_length=120, default='SALOM! | MEN', verbose_name='Salomlashuv (UZ)')
    greeting_ru = models.CharField(max_length=120, default='ПРИВЕТ! | Я', verbose_name='Salomlashuv (RU)')
    greeting_en = models.CharField(max_length=120, default='HELLO! | I AM', verbose_name='Salomlashuv (EN)')

    first_name_uz = models.CharField(max_length=80, verbose_name='Ism (UZ)', default="")
    first_name_ru = models.CharField(max_length=80, verbose_name='Ism (RU)', default="")
    first_name_en = models.CharField(max_length=80, verbose_name='Ism (EN)', default="")

    last_name_uz = models.CharField(max_length=80, verbose_name='Familiya (UZ)', default="")
    last_name_ru = models.CharField(max_length=80, verbose_name='Familiya (RU)', default="")
    last_name_en = models.CharField(max_length=80, verbose_name='Familiya (EN)', default="")

    role_uz = models.CharField(max_length=200, verbose_name='Lavozim (UZ)', default="")
    role_ru = models.CharField(max_length=200, verbose_name='Lavozim (RU)', default="")
    role_en = models.CharField(max_length=200, verbose_name='Lavozim (EN)', default="")

    bio_uz = models.TextField(verbose_name='Bio (UZ)', default="")
    bio_ru = models.TextField(verbose_name='Bio (RU)', default="")
    bio_en = models.TextField(verbose_name='Bio (EN)', default="")

    avatar = models.ImageField(upload_to='team/', blank=True, null=True, verbose_name='Rasm')

    cta_label_uz = models.CharField(max_length=60, default="Bog'lanish", verbose_name='Tugma matni (UZ)')
    cta_label_ru = models.CharField(max_length=60, default="Связаться", verbose_name='Tugma matni (RU)')
    cta_label_en = models.CharField(max_length=60, default="Connect", verbose_name='Tugma matni (EN)')

    cta_link = models.URLField(blank=True, verbose_name='CTA havolasi')
    telegram = models.URLField(blank=True, verbose_name='Telegram')
    instagram = models.URLField(blank=True, verbose_name='Instagram')
    github = models.URLField(blank=True, verbose_name='GitHub')
    linkedin = models.URLField(blank=True, verbose_name='LinkedIn')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Tartib raqami')
    is_active = models.BooleanField(default=True, verbose_name='Faol')

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'


class MissionSection(models.Model):
    """Maqsad (Mission) bo'limidagi logo va tavsifni boshqarish (Uch tilda)."""
    logo = models.ImageField(upload_to='mission_logos/', verbose_name='Logo')
    
    description_uz = models.TextField(verbose_name='Tavsif (UZ)', default="")
    description_ru = models.TextField(verbose_name='Tavsif (RU)', default="")
    description_en = models.TextField(verbose_name='Tavsif (EN)', default="")

    is_active = models.BooleanField(default=True, verbose_name='Faol')

    class Meta:
        verbose_name = 'Our Mission'
        verbose_name_plural = 'Our Missions'

    def __str__(self):
        return f"Our Mission - {self.id}"


class SubscriptionPlan(models.Model):
    """Pro obuna rejalari (Uch tilda va ikki valyutada)."""
    
    name_uz = models.CharField(max_length=100, verbose_name='Nomi (UZ)')
    name_ru = models.CharField(max_length=100, verbose_name='Nomi (RU)')
    name_en = models.CharField(max_length=100, verbose_name='Nomi (EN)')
    
    description_uz = models.TextField(verbose_name='Tavsif (UZ)', blank=True)
    description_ru = models.TextField(verbose_name='Tavsif (RU)', blank=True)
    description_en = models.TextField(verbose_name='Tavsif (EN)', blank=True)
    
    price_uzs = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Narxi (UZS)')
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Narxi (USD)')
    
    period_uz = models.CharField(max_length=50, verbose_name='Davr matni (UZ)', help_text="e.g. 'oyiga'")
    period_ru = models.CharField(max_length=50, verbose_name='Davr matni (RU)')
    period_en = models.CharField(max_length=50, verbose_name='Davr matni (EN)')
    
    features_uz = models.TextField(verbose_name='Xususiyatlar (UZ)', help_text="Har bir xususiyat yangi qatorda")
    features_ru = models.TextField(verbose_name='Xususiyatlar (RU)')
    features_en = models.TextField(verbose_name='Xususiyatlar (EN)')
    
    badge_text_uz = models.CharField(max_length=50, blank=True, verbose_name='Badge matni (UZ)')
    badge_text_ru = models.CharField(max_length=50, blank=True, verbose_name='Badge matni (RU)')
    badge_text_en = models.CharField(max_length=50, blank=True, verbose_name='Badge matni (EN)')
    
    button_text_uz = models.CharField(max_length=50, verbose_name='Tugma matni (UZ)')
    button_text_ru = models.CharField(max_length=50, verbose_name='Tugma matni (RU)')
    button_text_en = models.CharField(max_length=50, verbose_name='Tugma matni (EN)')
    
    is_free = models.BooleanField(default=False, verbose_name='Bepulmi?')
    is_most_popular = models.BooleanField(default=False, verbose_name='Eng mashhurmi?')
    is_recommended = models.BooleanField(default=False, verbose_name='Tavsiya etiladimi?')
    
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Tartib raqami')
    is_active = models.BooleanField(default=True, verbose_name='Faol')

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'

    def __str__(self):
        return self.name_en

    def get_features_list(self, lang='en'):
        field = f'features_{lang}'
        text = getattr(self, field, self.features_en)
        return [item.strip() for item in text.split('\n') if item.strip()]

