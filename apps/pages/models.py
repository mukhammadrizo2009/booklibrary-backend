from django.db import models


class TeamMember(models.Model):
    """About Us sahifasida ko'rsatiladigan jamoa a'zolari."""

    greeting   = models.CharField(max_length=120, default='SALOM! | MEN', verbose_name='Salomlashuv')
    first_name = models.CharField(max_length=80, verbose_name='Ism')
    last_name  = models.CharField(max_length=80, verbose_name='Familiya')
    role       = models.CharField(max_length=200, verbose_name='Lavozim / Texnologiyalar')
    bio        = models.TextField(verbose_name='Bio / Tavsif')
    avatar     = models.ImageField(upload_to='team/', blank=True, null=True, verbose_name='Rasm')
    cta_label  = models.CharField(max_length=60, default="Bog'lanish", verbose_name='CTA tugma matni')
    cta_link   = models.URLField(blank=True, verbose_name='CTA havolasi')
    telegram   = models.URLField(blank=True, verbose_name='Telegram')
    instagram  = models.URLField(blank=True, verbose_name='Instagram')
    github     = models.URLField(blank=True, verbose_name='GitHub')
    linkedin   = models.URLField(blank=True, verbose_name='LinkedIn')
    order      = models.PositiveSmallIntegerField(default=0, verbose_name='Tartib raqami')
    is_active  = models.BooleanField(default=True, verbose_name='Faol')

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Jamoa a\'zosi'
        verbose_name_plural = 'Jamoa a\'zolari'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
