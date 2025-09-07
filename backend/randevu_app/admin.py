from django.contrib import admin
from .models import (
    Randevu,
    GenelAyar,
    Personel,
    Hizmet,
    Galeri,
    IletisimBilgileri,
    SSS
)

@admin.register(Randevu)
class RandevuAdmin(admin.ModelAdmin):
    list_display = (
        'ad', 'soyad', 'telefon', 'email', 'tarih', 'seans_baslangic', 'seans_bitis',
        'hizmet_adi', 'hizmet_suresi', 'personel_adi', 'isletme',
        'sms', 'email_bilgilendirme', 'whatsapp', 'kvkk'
    )

admin.site.register(GenelAyar)
admin.site.register(Personel)
admin.site.register(Hizmet)
admin.site.register(Galeri)
admin.site.register(IletisimBilgileri)
admin.site.register(SSS)
