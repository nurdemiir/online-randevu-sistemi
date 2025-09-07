from django.urls import path
from . import views
from .views import galeri_sira_guncelle, sss_sirala, GenelAyarSaatAPIView



urlpatterns = [
    # Randevu
    path('api/randevu-al/', views.randevu_olustur),
    path('api/randevu-olustur/', views.randevu_olustur),  # alternatif endpoint
    path('api/randevular/', views.randevu_listesi, name="randevular_tum"),
    path('api/randevu-liste/', views.randevu_listesi, name='randevular_filtreli'),
    path('api/randevu/<int:id>/', views.randevu_detay),
    path('api/randevu-guncelle/<int:id>/', views.randevu_guncelle),

    # Genel Ayarlar
    path("api/genel-ayarlar/", views.genel_ayar_kaydet, name="genel_ayar_kaydet"),
    path("api/genel-ayarlar/liste", views.genel_ayar_listesi, name="genel_ayar_listesi"),
    path("api/genel-ayarlar/saat/", GenelAyarSaatAPIView.as_view(), name="genel_ayar_saat"),

    # Galeri
    path("api/galeri-ekle/", views.galeri_foto_ekle, name="galeri_foto_ekle"),
    path("api/galeri", views.galeri_listesi, name="galeri_listesi"),
    path("api/galeri-sil/", views.galeri_foto_sil, name="galeri_foto_sil"), 
    path('api/galeri-sira-guncelle/', views.galeri_sira_guncelle),

    # Hizmet
    path("api/hizmet-ekle/", views.hizmet_ekle, name="hizmet_ekle"),
    path("api/hizmet-listesi", views.hizmet_listesi, name="hizmet_listesi"),
    path("api/hizmetler/", views.hizmet_listesi, name="hizmet_listesi"),
    path("api/hizmet-detaylari/<int:hizmet_id>/", views.hizmet_detaylari, name="hizmet_detaylari"),
    path("api/hizmet/<int:hizmet_id>/", views.hizmet_detay, name="hizmet_detay"),
    path("api/hizmet-duzenle/<int:hizmet_id>/", views.hizmet_duzenle, name="hizmet_duzenle"),
    path("api/hizmet-sira-guncelle/", views.hizmet_sira_guncelle),
    path("api/hizmet-sil/", views.hizmet_sil, name="hizmet_sil"),

    # İletişim
    path("api/iletisim-ekle/", views.iletisim_kaydet, name="iletisim_kaydet"),
    path("api/iletisim", views.iletisim_listesi, name="iletisim_listesi"),

    # SSS
    path("api/sss", views.sss_listesi, name="sss_listesi"),
    path('api/sss/ekle', views.sss_ekle, name='sss_ekle'),
    path("api/sss/sil/<int:id>", views.sss_sil, name="sss_sil"),
    path("api/sss/guncelle/<int:id>", views.sss_guncelle, name="sss_guncelle"),
    path("api/sss/sirala", views.sss_sirala, name="sss_sirala"),
    path('api/sss/guncelle/<int:id>', views.sss_guncelle),


    # Personel
    path("api/personel", views.personel_listesi, name="personel_listesi"),
    path("api/personel-ekle", views.personel_ekle, name="personel_ekle"),
    path("api/personel-sil/<int:id>/", views.personel_sil, name="personel_sil"),
    path('api/sss/sirala', sss_sirala, name='sss_sirala'),
    path("api/personel/<int:personel_id>/", views.personel_detay, name="personel_detay"),
    
    
    #Odeme
    path("api/randevu/son", views.son_randevu, name="son_randevu"),
    path("api/randevu/<int:id>/", views.randevu_detay, name="randevu_detay"),

    #ISLETME PANEL RANDEVU YONETIM
    path("api/randevu/<int:id>/durum-degistir/", views.randevu_durum_degistir, name="randevu_durum_degistir"),
    path("api/randevu/<int:id>/onayla/", views.randevu_onayla, name="randevu_onayla"),
    path("api/randevu/<int:id>/tamamla/", views.randevu_tamamla, name="randevu_tamamla"),
    path("api/randevu/<int:id>/iptal-et/", views.randevu_iptal_et, name="randevu_iptal_et"),
    
    # Ciro İstatistikleri
    path("api/ciro-istatistikleri/", views.ciro_istatistikleri, name="ciro_istatistikleri"),

    # İşletme Panel (sadece sahip erişir)
    path('isletme/<slug:isletme_slug>/', views.isletme_panel, name='isletme_panel'),

    # Slug tabanlı işletme sayfaları (public)
    path('<slug:isletme_slug>/', views.isletme_anasayfa, name='isletme_anasayfa'),
    path('<slug:isletme_slug>/randevu/', views.isletme_randevu, name='isletme_randevu'),
    path('<slug:isletme_slug>/sss/', views.isletme_sss, name='isletme_sss'),
    path('<slug:isletme_slug>/iletisim/', views.isletme_iletisim, name='isletme_iletisim'),
    path('<slug:isletme_slug>/odeme/hizmet/', views.isletme_odeme_hizmet_detaylari, name='isletme_odeme_hizmet'),
    path('<slug:isletme_slug>/odeme/tarih-saat/', views.isletme_odeme_tarih_saat, name='isletme_odeme_tarih_saat'),
    path('<slug:isletme_slug>/odeme/musteri-bilgileri/', views.isletme_odeme_musteri_bilgileri, name='isletme_odeme_musteri_bilgileri'),
    path('<slug:isletme_slug>/odeme/on-izleme/', views.isletme_odeme_on_izleme, name='isletme_odeme_on_izleme'),


]