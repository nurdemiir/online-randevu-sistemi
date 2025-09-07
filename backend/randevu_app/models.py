from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User

# Randevu modeli
class Randevu(models.Model):
    ad = models.CharField(max_length=100)
    soyad = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20)
    email = models.EmailField()
    
    tarih = models.DateField(null=True, blank=True)
    seans_baslangic = models.TimeField(null=True, blank=True)
    seans_bitis = models.TimeField(null=True, blank=True)

    hizmet_adi = models.CharField(max_length=100)
    hizmet_suresi = models.IntegerField(help_text="Dakika cinsinden")
    
    personel_adi = models.CharField(max_length=100)
    isletme = models.CharField(max_length=100)
    hizmet_fiyat = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # İletişim tercihleri ve KVKK
    sms = models.BooleanField(default=False)
    email_bilgilendirme = models.BooleanField(default=False)
    whatsapp = models.BooleanField(default=False)
    kvkk = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ad} {self.soyad} - {self.tarih} {self.seans_baslangic} / {self.hizmet_adi}"
    
    DURUM_CHOICES = [
        ('bekleyen', 'Bekleyen'),
        ('onaylandi', 'Onaylandı'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal', 'İptal Edildi'),
    ]
    
    durum = models.CharField(
        max_length=10,
        choices=DURUM_CHOICES,
        default='bekleyen',
        verbose_name="Durum"
    )

# Genel Ayarlar
class GenelAyar(models.Model):
    isletme_adi = models.CharField(max_length=100)
    aciklama = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='logolar/', blank=True)
    acilis_saati = models.TimeField(null=True, blank=True) 
    kapanis_saati = models.TimeField(null=True, blank=True)
    guncellenme = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    yayinla = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='isletmeler', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.isletme_adi)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.isletme_adi


# Personel
class Personel(models.Model):
    ad = models.CharField(max_length=100)
    hizmetler = models.TextField()  # Virgülle ayrılmış hizmet isimleri saklanabilir
    isletme_adi = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.ad

# Hizmet
class Hizmet(models.Model):
    hizmet_adi = models.CharField(max_length=100)
    aciklama = models.TextField()
    detayli_aciklama = models.TextField()
    seans_suresi = models.IntegerField(help_text="Dakika cinsinden")
    fiyat = models.DecimalField(max_digits=8, decimal_places=2)
    hizmet_fotografi = models.ImageField(upload_to='hizmet_fotograflari/')
    acilis_saati = models.TimeField(null=True, blank=True)
    kapanis_saati = models.TimeField(null=True, blank=True)
    sira = models.PositiveIntegerField(default=0)
    isletme_adi = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.hizmet_adi

# Galeri
class Galeri(models.Model):
    isletme_adi = models.CharField(max_length=100)  # hangi işletmenin galerisi
    resim = models.ImageField(upload_to='galeri/')
    aciklama = models.CharField(max_length=255, blank=True, null=True)
    sira = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.isletme_adi} - {self.resim.url}"

    class Meta:
        ordering = ['sira']  # ✅ Galeri otomatik sıralı gelsin
        
        
# İletişim Bilgileri
class IletisimBilgileri(models.Model):
    telefon = models.CharField(max_length=20)
    il = models.CharField(max_length=50)
    ilce = models.CharField(max_length=50)
    mahalle = models.CharField(max_length=100)
    no = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.il}, {self.ilce} ({self.telefon})"

# SSS
class SSS(models.Model):
    soru = models.CharField(max_length=255)
    cevap = models.TextField()
    siralama = models.IntegerField(default=0)  # Sıralama için alan

    class Meta:
        ordering = ['siralama']  # Veritabanından çekilirken sıralı gelsin

    def __str__(self):
        return self.soru
