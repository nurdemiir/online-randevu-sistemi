from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import (
    Randevu, GenelAyar, Personel, Hizmet, Galeri,
    IletisimBilgileri, SSS
)
import json
from .serializers import GenelAyarSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from django.db.models import Sum, Count
from django.utils import timezone
import calendar
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# ------------------------- RANDEVU -------------------------
@csrf_exempt
def randevu_olustur(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # 1. Hizmet ID ile eşleş
            hizmet_id = data.get('hizmet_id')
            if not hizmet_id:
                return JsonResponse({'error': 'hizmet_id eksik'}, status=400)

            try:
                hizmet_obj = Hizmet.objects.get(id=hizmet_id)
            except Hizmet.DoesNotExist:
                return JsonResponse({'error': 'Hizmet ID eşleşmedi, sistemde kayıtlı olmayabilir.'}, status=400)

            # 2. Diğer verileri al
            hizmet_suresi = int(hizmet_obj.seans_suresi)

            r = Randevu.objects.create(
                ad=data.get('ad'),
                soyad=data.get('soyad'),
                telefon=data.get('telefon'),
                email=data.get('email'),
                tarih=data.get('tarih'),
                seans_baslangic=data.get('seans_baslangic'),
                seans_bitis=data.get('seans_bitis'),
                hizmet_adi=hizmet_obj.hizmet_adi,           # DB'den gelen temiz ad
                hizmet_suresi=hizmet_suresi,
                personel_adi=data.get('personel_adi'),
                isletme=data.get('isletme', ''),
                sms=data.get('sms', False),
                email_bilgilendirme=data.get('email_bilgilendirme', False),
                whatsapp=data.get('whatsapp', False),
                kvkk=data.get('kvkk', False),
                hizmet_fiyat=hizmet_obj.fiyat
            )

            return JsonResponse({'status': 'ok', 'id': r.id})
        except Exception as e:
            return JsonResponse({'error': f'Randevu oluşturulurken hata: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Sadece POST destekleniyor'}, status=405)


def randevu_listesi(request):
    try:
        isletme_adi = request.GET.get('isletme_adi')

        if isletme_adi:
            randevular = Randevu.objects.filter(isletme=isletme_adi).order_by('-tarih', '-seans_baslangic')
        else:
            randevular = Randevu.objects.all().order_by('-tarih', '-seans_baslangic')

        data = []
        for r in randevular:
            hizmet = Hizmet.objects.filter(hizmet_adi__iexact=r.hizmet_adi.strip()).first()
            hizmet_fiyat = str(hizmet.fiyat) if hizmet else ""

            data.append({
                "id": r.id,
                "ad": r.ad,
                "soyad": r.soyad,
                "telefon": r.telefon,
                "email": r.email,
                "tarih": r.tarih.strftime('%Y-%m-%d'),
                "seans_baslangic": r.seans_baslangic.strftime('%H:%M'),
                "seans_bitis": r.seans_bitis.strftime('%H:%M'),
                "hizmet_adi": r.hizmet_adi,
                "hizmet_suresi": r.hizmet_suresi,
                "personel_adi": r.personel_adi,
                "isletme": r.isletme,
                "durum": getattr(r, "durum", "bekleyen"),  # ileride modelde eklersen hazır
                "sms": r.sms,
                "email_bilgilendirme": r.email_bilgilendirme,
                "whatsapp": r.whatsapp,
                "kvkk": r.kvkk,
                "hizmet_fiyat": hizmet_fiyat,
                "fiyat": r.hizmet_fiyat if hasattr(r, 'hizmet_fiyat') else ""

            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({'error': f'Randevular alınırken hata: {str(e)}'}, status=500)


def randevu_detay(request, id):
    try:
        r = Randevu.objects.get(id=id)

        # Hizmet fiyatı alınsın
        hizmet = None
        hizmet_fiyat = ""
        if r.hizmet_adi:
            hizmet = Hizmet.objects.filter(hizmet_adi__iexact=r.hizmet_adi.strip()).first()
            if hizmet:
                hizmet_fiyat = str(hizmet.fiyat)

        return JsonResponse({
            "id": r.id,
            "ad": r.ad,
            "soyad": r.soyad,
            "telefon": r.telefon,
            "email": r.email,
            "tarih": str(r.tarih) if r.tarih else "",
            "seans_baslangic": r.seans_baslangic.strftime('%H:%M') if r.seans_baslangic else "",
            "seans_bitis": r.seans_bitis.strftime('%H:%M') if r.seans_bitis else "",
            "hizmet_adi": r.hizmet_adi,
            "hizmet_suresi": r.hizmet_suresi,
            "personel_adi": r.personel_adi,
            "sms": r.sms,
            "email_bilgilendirme": r.email_bilgilendirme,
            "whatsapp": r.whatsapp,
            "kvkk": r.kvkk,
            "isletme": r.isletme,
            "hizmet_fiyat": hizmet_fiyat,
            "hizmet_id": hizmet.id if hizmet else None,
        })

    except Randevu.DoesNotExist:
        return JsonResponse({"error": "Randevu bulunamadı"}, status=404)

    except Exception as e:
        return JsonResponse({"error": f"Beklenmeyen bir hata oluştu: {str(e)}"}, status=500)

@csrf_exempt
def randevu_guncelle(request, id):
    try:
        r = Randevu.objects.get(id=id)

        if request.method in ['POST', 'PUT']:
            data = json.loads(request.body)

            r.tarih = data.get("tarih", r.tarih)
            r.seans_baslangic = data.get("seans_baslangic", r.seans_baslangic)
            r.seans_bitis = data.get("seans_bitis", r.seans_bitis)
            r.ad = data.get("ad", r.ad)
            r.soyad = data.get("soyad", r.soyad)
            r.telefon = data.get("telefon", r.telefon)
            r.email = data.get("email", r.email)

            r.sms = data.get("sms", r.sms)
            r.email_bilgilendirme = data.get("email_bilgilendirme", r.email_bilgilendirme)
            r.whatsapp = data.get("whatsapp", r.whatsapp)
            r.kvkk = data.get("kvkk", r.kvkk)

            yeni_durum = data.get("durum", r.durum)
            r.durum = yeni_durum

            # Durum tamamlandıysa hizmet_fiyat güncelle
            if yeni_durum == 'tamamlandi':
                hizmet = Hizmet.objects.filter(hizmet_adi__iexact=r.hizmet_adi.strip()).first()
                if hizmet:
                    r.hizmet_fiyat = hizmet.fiyat
            else:
                # Durum tamamlandı değilse fiyatı sıfırla veya null yapabilirsin
                # r.hizmet_fiyat = 0
                pass

            r.save()
            return JsonResponse({"status": "ok"})

        return JsonResponse({"error": "Sadece POST veya PUT destekleniyor"}, status=405)

    except Randevu.DoesNotExist:
        return JsonResponse({"error": "Randevu bulunamadı"}, status=404)

# ------------------------- GENEL AYAR -------------------------
@csrf_exempt
def genel_ayar_kaydet(request):
    if request.method == "POST":
        try:
            ayar = GenelAyar.objects.first()
            if not ayar:
                ayar = GenelAyar.objects.create(
                    isletme_adi="Varsayılan",
                    aciklama="",
                    logo=None
                )

            if 'isletme_adi' in request.POST:
                ayar.isletme_adi = request.POST['isletme_adi']
            if 'aciklama' in request.POST:
                ayar.aciklama = request.POST['aciklama']
            if 'logo' in request.FILES:
                ayar.logo = request.FILES['logo']
            if 'acilis_saati' in request.POST:
                ayar.acilis_saati = request.POST['acilis_saati']
            if 'kapanis_saati' in request.POST:
                ayar.kapanis_saati = request.POST['kapanis_saati']

            ayar.save()
            return JsonResponse({"message": "Güncelleme başarılı."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Sadece POST kabul edilir"}, status=405)

def genel_ayar_listesi(request):
    try:
        isletme_adi = request.GET.get('isletme_adi')
        slug = request.GET.get('slug')

        if slug:
            ayarlar = list(GenelAyar.objects.filter(slug=slug).order_by('-guncellenme').values())
        elif isletme_adi:
            ayarlar = list(GenelAyar.objects.filter(isletme_adi=isletme_adi).order_by('-guncellenme').values())
        else:
            ayarlar = list(GenelAyar.objects.order_by('-guncellenme').values())

        for ayar in ayarlar:
            logo = ayar.get('logo')
            if logo:
                if not logo.startswith("http"):
                    # Göreceli ise tam URL oluştur
                    ayar['logo'] = request.build_absolute_uri(f"{settings.MEDIA_URL}{logo}")
                elif logo.startswith("http://localhost:8000"):
                    # localhost ise 127.0.0.1 olarak değiştir
                    ayar['logo'] = logo.replace("http://localhost:8000", "http://127.0.0.1:8000")
            else:
                # Logo boşsa "" olarak ayarla
                ayar['logo'] = ""

        return JsonResponse(ayarlar, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': f'Genel ayarlar alınırken hata: {str(e)}'}, status=500)
# ------------------------- GALERİ -------------------------
@csrf_exempt
def galeri_foto_ekle(request):
    if request.method == "POST":
        try:
            isletme_adi = request.POST.get("isletme_adi")
            aciklama = request.POST.get("aciklama")
            resim = request.FILES.get("resim")

            if not resim or not isletme_adi:
                return JsonResponse({"error": "Eksik veri"}, status=400)

            Galeri.objects.create(
                isletme_adi=isletme_adi,
                aciklama=aciklama,
                resim=resim
            )
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"error": f'Galeri fotoğrafı eklenirken hata: {str(e)}'}, status=400)
    return JsonResponse({"error": "Sadece POST desteklenir"}, status=405)

def galeri_listesi(request):
    try:
        slug = request.GET.get('slug')
        isletme_adi = request.GET.get('isletme_adi')

        if slug:
            try:
                isletme = GenelAyar.objects.get(slug=slug)
                galeri_qs = Galeri.objects.filter(isletme_adi=isletme.isletme_adi)
            except GenelAyar.DoesNotExist:
                galeri_qs = Galeri.objects.none()
        elif isletme_adi:
            galeri_qs = Galeri.objects.filter(isletme_adi=isletme_adi)
        else:
            galeri_qs = Galeri.objects.all()

        galeri = list(galeri_qs.values())
        for item in galeri:
            if item.get('resim'):
                item['resim'] = f"{settings.MEDIA_URL}{item['resim']}"
        return JsonResponse(galeri, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'Galeri alınırken hata: {str(e)}'}, status=500)


@csrf_exempt
def galeri_foto_sil(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            galeri_id = data.get("id")
            if not galeri_id:
                return JsonResponse({"error": "Galeri ID gerekli"}, status=400)
            
            galeri = Galeri.objects.get(id=galeri_id)
            if galeri.resim:
                galeri.resim.delete()  # Dosyayı diskten sil
            galeri.delete()  # Veritabanından sil
            return JsonResponse({"status": "ok"})
        except Galeri.DoesNotExist:
            return JsonResponse({"error": "Galeri kaydı bulunamadı"}, status=404)
        except Exception as e:
            return JsonResponse({"error": f'Galeri silinirken hata: {str(e)}'}, status=400)
    return JsonResponse({"error": "Sadece POST desteklenir"}, status=405)


@csrf_exempt
def galeri_sira_guncelle(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            sira_listesi = data.get("sira", [])

            for index, id in enumerate(sira_listesi):
                Galeri.objects.filter(id=id).update(sira=index)

            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)}, status=400)

# ------------------------- HİZMET -------------------------
@csrf_exempt
def hizmet_ekle(request):
    if request.method == "POST":
        try:
            hizmet_fotografi = request.FILES.get("hizmet_fotografi")
            hizmet_adi = request.POST.get("hizmet_adi")
            aciklama = request.POST.get("aciklama")
            detayli_aciklama = request.POST.get("detayli_aciklama")
            seans_suresi = request.POST.get("seans_suresi")
            fiyat = request.POST.get("fiyat")
            acilis_saati = request.POST.get("acilis_saati")
            kapanis_saati = request.POST.get("kapanis_saati")

            if not hizmet_adi or not hizmet_fotografi:
                return JsonResponse({"error": "Zorunlu alanlar eksik"}, status=400)

            Hizmet.objects.create(
                hizmet_adi=hizmet_adi,
                aciklama=aciklama,
                detayli_aciklama=detayli_aciklama,
                seans_suresi=seans_suresi,
                fiyat=fiyat,
                acilis_saati=acilis_saati,
                kapanis_saati=kapanis_saati,
                hizmet_fotografi=hizmet_fotografi
            )
            return JsonResponse({"status": "ok"})  
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Sadece POST kabul edilir"}, status=405)


# Hizmet ve personel listelerini slug'a göre daralt
@csrf_exempt
def hizmet_listesi(request):
    try:
        slug = request.GET.get('slug')
        isletme_adi = request.GET.get('isletme_adi')

        qs = Hizmet.objects.all()
        if slug:
            try:
                isletme = GenelAyar.objects.get(slug=slug)
                qs = qs.filter(isletme_adi=isletme.isletme_adi)
            except GenelAyar.DoesNotExist:
                qs = qs.none()
        elif isletme_adi:
            qs = qs.filter(isletme_adi=isletme_adi)

        hizmetler = qs.order_by("sira").values(
            'id',
            'hizmet_adi',
            'aciklama',
            'detayli_aciklama',
            'seans_suresi',
            'fiyat',
            'hizmet_fotografi'
        )
        hizmetler = list(hizmetler)

        for hizmet in hizmetler:
            if hizmet.get('hizmet_fotografi'):
                hizmet['hizmet_fotografi'] = f"{settings.MEDIA_URL}{hizmet['hizmet_fotografi']}"

        return JsonResponse(hizmetler, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'Hizmetler alınırken hata: {str(e)}'}, status=500)

@csrf_exempt
def hizmet_detaylari(request, hizmet_id):
    try:
        hizmet = Hizmet.objects.get(id=hizmet_id)
        personeller = Personel.objects.filter(hizmetler__icontains=hizmet.hizmet_adi)

        hizmet_data = {
            "id": hizmet.id,
            "hizmet_adi": hizmet.hizmet_adi,
            "aciklama": hizmet.aciklama,
            "detayli_aciklama": hizmet.detayli_aciklama,
            "seans_suresi": hizmet.seans_suresi,
            "fiyat": str(hizmet.fiyat),
            "acilis_saati": hizmet.acilis_saati.strftime("%H:%M") if hizmet.acilis_saati else None,
            "kapanis_saati": hizmet.kapanis_saati.strftime("%H:%M") if hizmet.kapanis_saati else None,
            "hizmet_fotografi": f"{settings.MEDIA_URL}{hizmet.hizmet_fotografi}" if hizmet.hizmet_fotografi else ""
        }

        personel_data = [{"id": p.id, "ad": p.ad} for p in personeller]

        return JsonResponse({
            "hizmet": hizmet_data,
            "uygun_personeller": personel_data
        })

    except Hizmet.DoesNotExist:
        return JsonResponse({"error": "Hizmet bulunamadı"}, status=404)

    
@csrf_exempt
def hizmet_detay(request, hizmet_id):
    try:
        hizmet = Hizmet.objects.get(id=hizmet_id)
        data = {
            "id": hizmet.id,
            "hizmet_adi": hizmet.hizmet_adi,
            "aciklama": hizmet.aciklama,
            "detayli_aciklama": hizmet.detayli_aciklama,
            "seans_suresi": hizmet.seans_suresi,
            "fiyat": str(hizmet.fiyat),
            "hizmet_fotografi": hizmet.hizmet_fotografi.url if hizmet.hizmet_fotografi else None
        }
        return JsonResponse(data)
    except Hizmet.DoesNotExist:
        return JsonResponse({"error": "Hizmet bulunamadı"}, status=404)
    
@csrf_exempt
def hizmet_sira_guncelle(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            yeni_sira = data.get("sira")

            for index, hizmet_id in enumerate(yeni_sira):
                Hizmet.objects.filter(id=hizmet_id).update(sira=index)

            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)})

@csrf_exempt
def hizmet_duzenle(request, hizmet_id):
    if request.method == "POST":
        try:
            hizmet = Hizmet.objects.get(id=hizmet_id)

            hizmet.hizmet_adi = request.POST.get("hizmet_adi", hizmet.hizmet_adi)
            hizmet.aciklama = request.POST.get("aciklama", hizmet.aciklama)
            hizmet.detayli_aciklama = request.POST.get("detayli_aciklama", hizmet.detayli_aciklama)
            hizmet.seans_suresi = request.POST.get("seans_suresi", hizmet.seans_suresi)
            hizmet.fiyat = request.POST.get("fiyat", hizmet.fiyat)

            if request.FILES.get("hizmet_fotografi"):
                hizmet.hizmet_fotografi = request.FILES["hizmet_fotografi"]

            hizmet.save()
            return JsonResponse({"status": "ok"})
        except Hizmet.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Hizmet bulunamadı"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Sadece POST isteği desteklenir"}, status=405)

@csrf_exempt
def hizmet_sil(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            hizmet_id = data.get("id")
            hizmet = Hizmet.objects.get(id=hizmet_id)
            hizmet.delete()
            return JsonResponse({"message": "Silindi."})
        except Hizmet.DoesNotExist:
            return JsonResponse({"error": "Hizmet bulunamadı."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Yalnızca POST isteği destekleniyor."}, status=405)

# ------------------------- İLETİŞİM -------------------------
@csrf_exempt
def iletisim_kaydet(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            IletisimBilgileri.objects.all().delete()  # Eski verileri sil
            IletisimBilgileri.objects.create(
                telefon=data.get("telefon", ""),
                il=data.get("il", ""),
                ilce=data.get("ilce", ""),
                mahalle=data.get("mahalle", ""),
                no=data.get("no", "")
            )
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"error": "Sadece POST isteklerine izin verilir."}, status=405)

def iletisim_listesi(request):
    if request.method == "GET":
        try:
            iletisim = IletisimBilgileri.objects.last()
            if iletisim:
                return JsonResponse({
                    "telefon": iletisim.telefon,
                    "il": iletisim.il,
                    "ilce": iletisim.ilce,
                    "mahalle": iletisim.mahalle,
                    "no": iletisim.no
                })
            else:
                return JsonResponse({"error": "İletişim bilgisi bulunamadı"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Sadece GET isteklerine izin verilir."}, status=405)

# ------------------------- SSS -------------------------
@csrf_exempt
def sss_ekle(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            soru = data.get("soru")
            cevap = data.get("cevap")
            if soru and cevap:
                SSS.objects.create(soru=soru, cevap=cevap)
                return JsonResponse({"status": "ok"})
            else:
                return JsonResponse({"status": "error", "error": "Eksik veri"})
        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)})
    return JsonResponse({"error": "Sadece POST desteklenir"}, status=405)

@csrf_exempt
def sss_sirala(request):
    if request.method != "POST":
        return JsonResponse({"error": "Sadece POST desteklenir"}, status=405)

    try:
        data = json.loads(request.body)
        siralama_listesi = data.get("siralama", [])

        if not isinstance(siralama_listesi, list):
            return JsonResponse({"status": "error", "message": "Geçersiz sıralama formatı"}, status=400)

        for index, faq_id in enumerate(siralama_listesi):
            SSS.objects.filter(id=faq_id).update(siralama=index)

        return JsonResponse({"status": "ok"})
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Geçersiz JSON formatı"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def sss_listesi(request):
    if request.method == "GET":
        sss_list = list(SSS.objects.all().order_by('siralama').values("id", "soru", "cevap"))
        return JsonResponse(sss_list, safe=False)
    return JsonResponse({"error": "Sadece GET isteklerine izin verilir."}, status=405)



@csrf_exempt
def sss_sil(request, id):
    try:
        faq = SSS.objects.get(id=id)
        faq.delete()
        return JsonResponse({"status": "ok"})
    except SSS.DoesNotExist:
        return JsonResponse({"status": "error", "message": "SSS bulunamadı"}, status=404)

@csrf_exempt
def sss_guncelle(request, id):
    if request.method in ["PUT", "POST"]:  # PUT is better, but fallback for POST
        try:
            data = json.loads(request.body)
            faq = SSS.objects.get(id=id)

            faq.soru = data.get("soru", faq.soru)
            faq.cevap = data.get("cevap", faq.cevap)
            faq.save()

            return JsonResponse({"status": "ok"})
        except SSS.DoesNotExist:
            return JsonResponse({"status": "error", "message": "SSS bulunamadı"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Yalnızca PUT veya POST desteklenir"}, status=405)




# ------------------------- PERSONEL -------------------------
@csrf_exempt
def personel_ekle(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ad = data.get("ad")
            hizmetler_list = data.get("hizmetler", [])

            if not ad or not hizmetler_list:
                return JsonResponse({"status": "error", "message": "Eksik veri"}, status=400)

            hizmetler_str = ",".join(hizmetler_list)
            personel = Personel.objects.create(ad=ad, hizmetler=hizmetler_str)
            return JsonResponse({"status": "ok", "id": personel.id})
        except Exception as e:
            import traceback
            print("🔴 HATA:", traceback.format_exc())
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"error": "Sadece POST desteklenir"}, status=405)


def personel_listesi(request):
    try:
        slug = request.GET.get('slug')
        isletme_adi = request.GET.get('isletme_adi')

        qs = Personel.objects.all()
        if slug:
            try:
                isletme = GenelAyar.objects.get(slug=slug)
                qs = qs.filter(isletme_adi=isletme.isletme_adi)
            except GenelAyar.DoesNotExist:
                qs = qs.none()
        elif isletme_adi:
            qs = qs.filter(isletme_adi=isletme_adi)

        personeller = list(qs.values())
        return JsonResponse(personeller, safe=False)
    except Exception as e:
        import traceback
        print("🔴 HATA:", traceback.format_exc())  # Terminalde gösterilecek
        return JsonResponse({'error': f'Personel alınırken hata: {str(e)}'}, status=500)


@csrf_exempt
def personel_sil(request, id):
    if request.method == "DELETE":
        try:
            personel = Personel.objects.get(id=id)
            personel.delete()
            return JsonResponse({"status": "ok"})
        except Personel.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Personel bulunamadı"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"error": "Sadece DELETE desteklenir"}, status=405)


def personel_detay(request, personel_id):
    try:
        personel = Personel.objects.get(id=personel_id)
        data = {
            "id": personel.id,
            "ad": personel.ad,
            "hizmetler": personel.hizmetler,
        }
        return JsonResponse(data)
    except Personel.DoesNotExist:
        return JsonResponse({"error": "Personel bulunamadı"}, status=404)


#------------------------------------ODEME ADIMLARİ-------------------------------------------------------------------------------------
def son_randevu(request):
    try:
        randevu = Randevu.objects.last()
        if not randevu:
            return JsonResponse({"error": "Kayıt yok"}, status=404)

        # Hizmet adı uyuşsun diye boşlukları temizle ve büyük/küçük harf duyarsız ara
        hizmet = Hizmet.objects.filter(hizmet_adi__iexact=randevu.hizmet_adi.strip()).first()

        # Eğer eşleşme yoksa bile hata almamak için kontrol
        hizmet_fiyat = str(hizmet.fiyat) if hizmet and hizmet.fiyat else ""
        hizmet_suresi = hizmet.seans_suresi if hizmet else randevu.hizmet_suresi
        hizmet_aciklama = hizmet.aciklama if hizmet else ""

        return JsonResponse({
            "ad": randevu.ad,
            "soyad": randevu.soyad,
            "telefon": randevu.telefon,
            "email": randevu.email,
            "tarih": str(randevu.tarih),
            "seans_baslangic": str(randevu.seans_baslangic),
            "seans_bitis": str(randevu.seans_bitis),
            "hizmet_adi": randevu.hizmet_adi,
            "hizmet_suresi": hizmet_suresi,
            "personel_adi": randevu.personel_adi,
            "sms": randevu.sms,
            "email_bilgilendirme": randevu.email_bilgilendirme,
            "whatsapp": randevu.whatsapp,
            "kvkk": randevu.kvkk,
            "hizmet_fiyat": hizmet_fiyat,
            "hizmet_aciklama": hizmet_aciklama
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_son_genel_ayar():
    return GenelAyar.objects.order_by('-guncellenme').first()

class GenelAyarSaatAPIView(APIView):
    def get(self, request):
        try:
            ayar = GenelAyar.objects.first()
            if not ayar:
                return Response({'error': 'Genel ayar bulunamadı'}, status=404)
            serializer = GenelAyarSerializer(ayar)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def post(self, request):
        try:
            ayar = GenelAyar.objects.first()
            if not ayar:
                ayar = GenelAyar.objects.create(
                    isletme_adi="Varsayılan",
                    aciklama="",
                    logo=None
                )
            ayar.acilis_saati = request.data.get("acilis_saati")
            ayar.kapanis_saati = request.data.get("kapanis_saati")
            ayar.save()
            serializer = GenelAyarSerializer(ayar)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

#----------------------------------------------------------ISLETME PANEL RANDEVU YONETIM------------------------------------------------------------
@csrf_exempt
def randevu_durum_degistir(request, id):
    try:
        r = Randevu.objects.get(id=id)
        if request.method == 'POST':
            data = json.loads(request.body)
            yeni_durum = data.get("durum", r.durum)

            if yeni_durum not in dict(Randevu.DURUM_CHOICES):
                return JsonResponse({"error": "Geçersiz durum değeri"}, status=400)

            r.durum = yeni_durum
            r.save()
            return JsonResponse({"status": "ok"})
    except Randevu.DoesNotExist:
        return JsonResponse({"error": "Randevu bulunamadı"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def randevu_onayla(request, id):
    try:
        r = Randevu.objects.get(id=id)
        r.durum = 'onaylandi'
        r.save()
        return JsonResponse({"status": "ok"})
    except Randevu.DoesNotExist:
        return JsonResponse({"error": "Randevu bulunamadı"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def randevu_tamamla(request, id):
    try:
        r = Randevu.objects.get(id=id)

        # Hizmet fiyatını set et
        if not r.hizmet_fiyat or r.hizmet_fiyat == 0:
            hizmet = Hizmet.objects.filter(hizmet_adi__iexact=r.hizmet_adi.strip()).first()
            if hizmet:
                r.hizmet_fiyat = hizmet.fiyat
        
        r.durum = 'tamamlandi'
        r.save()
        return JsonResponse({"status": "ok"})
    except Randevu.DoesNotExist:
        return JsonResponse({"error": "Randevu bulunamadı"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def randevu_iptal_et(request, id):
    try:
        r = Randevu.objects.get(id=id)
        r.durum = 'iptal'
        r.save()
        return JsonResponse({"status": "ok"})
    except Randevu.DoesNotExist:
        return JsonResponse({"error": "Randevu bulunamadı"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def ciro_istatistikleri(request):
    try:
        month_names = [
            'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
            'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'
        ]

        isletme_adi = request.GET.get('isletme_adi', '').strip()

        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=180)

        randevular = Randevu.objects.filter(
            tarih__gte=start_date,
            tarih__lte=end_date,
            durum="tamamlandi"
        )
        if isletme_adi:
            randevular = randevular.filter(isletme__iexact=isletme_adi)

        monthly_data = []

        for i in range(6):
            ay = (end_date.month - i - 1) % 12 + 1
            yil = end_date.year if end_date.month - i > 0 else end_date.year - 1
            month_start = datetime(yil, ay, 1).date()
            next_month = ay % 12 + 1
            next_year = yil if next_month != 1 else yil + 1
            month_end = (datetime(next_year, next_month, 1) - timedelta(days=1)).date()

            month_randevular = randevular.filter(
                tarih__gte=month_start,
                tarih__lte=month_end
            )

            total = sum([float(r.hizmet_fiyat or 0) for r in month_randevular])

            monthly_data.append({
                "ay": month_names[ay - 1],
                "yil": yil,
                "ay_adi": f"{month_names[ay - 1]} {yil}",
                "ciro": round(total, 2),
                "randevu_sayisi": month_randevular.count()
            })

        monthly_data.reverse()  # En eski ay başta olsun

        toplam_ciro = sum(d["ciro"] for d in monthly_data)
        toplam_randevu = sum(d["randevu_sayisi"] for d in monthly_data)
        ortalama = round(toplam_ciro / toplam_randevu, 2) if toplam_randevu > 0 else 0
        en_iyi_ay = max(monthly_data, key=lambda x: x["ciro"]) if monthly_data else None
        bu_ay = timezone.now().month
        bu_yil = timezone.now().year
        bu_ay_veri = next((d for d in monthly_data if d["yil"] == bu_yil and d["ay"] == month_names[bu_ay - 1]), None)

        return JsonResponse({
            "aylik_veriler": monthly_data,
            "genel_istatistikler": {
                "toplam_ciro": round(toplam_ciro, 2),
                "toplam_randevu": toplam_randevu,
                "ortalama_randevu_cirosu": ortalama,
                "en_iyi_ay": en_iyi_ay["ay_adi"] if en_iyi_ay else None,
                "en_iyi_ay_cirosu": en_iyi_ay["ciro"] if en_iyi_ay else 0,
                "bu_ay_ciro": bu_ay_veri["ciro"] if bu_ay_veri else 0,
                "bu_ay_randevu": bu_ay_veri["randevu_sayisi"] if bu_ay_veri else 0
            }
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ------------------------- SLUG TABANLI İŞLETME SAYFALARI -------------------------
def isletme_anasayfa(request, isletme_slug):
    isletme = get_object_or_404(GenelAyar, slug=isletme_slug)
    if not getattr(isletme, 'yayinla', True):
        return JsonResponse({"error": "Bu işletme yayında değil"}, status=403)
    return render(request, 'musteri_panel/galeri/index15.html', {'isletme': isletme})

def isletme_randevu(request, isletme_slug):
    isletme = get_object_or_404(GenelAyar, slug=isletme_slug)
    if not getattr(isletme, 'yayinla', True):
        return JsonResponse({"error": "Bu işletme yayında değil"}, status=403)
    return render(request, 'musteri_panel/randevu_al/index1.html', {'isletme': isletme})

@login_required
def isletme_panel(request, isletme_slug):
    isletme = get_object_or_404(GenelAyar, slug=isletme_slug)
    if isletme.owner_id and request.user.id != isletme.owner_id:
        return JsonResponse({"error": "Bu işletme için yetkiniz yok"}, status=403)
    if not getattr(isletme, 'yayinla', True):
        return JsonResponse({"error": "Bu işletme yayında değil"}, status=403)
    return render(request, 'isletme_panel/anasayfa/index6.html', {'isletme': isletme})

# Public customer pages with slug

def isletme_sss(request, isletme_slug):
    isletme = get_object_or_404(GenelAyar, slug=isletme_slug)
    if not getattr(isletme, 'yayinla', True):
        return JsonResponse({"error": "Bu işletme yayında değil"}, status=403)
    return render(request, 'musteri_panel/sss/index3.html', {'isletme': isletme})


def isletme_iletisim(request, isletme_slug):
    isletme = get_object_or_404(GenelAyar, slug=isletme_slug)
    if not getattr(isletme, 'yayinla', True):
        return JsonResponse({"error": "Bu işletme yayında değil"}, status=403)
    return render(request, 'musteri_panel/iletisim/index2.html', {'isletme': isletme})

# Odeme step pages

def isletme_odeme_hizmet_detaylari(request, isletme_slug):
    isletme = get_object_or_404(GenelAyar, slug=isletme_slug)
    if not getattr(isletme, 'yayinla', True):
        return JsonResponse({"error": "Bu işletme yayında değil"}, status=403)
    return render(request, 'odeme/hizmet_detaylari/index20.html', {'isletme': isletme})


def isletme_odeme_tarih_saat(request, isletme_slug):
    isletme = get_object_or_404(GenelAyar, slug=isletme_slug)
    if not getattr(isletme, 'yayinla', True):
        return JsonResponse({"error": "Bu işletme yayında değil"}, status=403)
    return render(request, 'odeme/tarih_saat/index22.html', {'isletme': isletme})


def isletme_odeme_musteri_bilgileri(request, isletme_slug):
    isletme = get_object_or_404(GenelAyar, slug=isletme_slug)
    if not getattr(isletme, 'yayinla', True):
        return JsonResponse({"error": "Bu işletme yayında değil"}, status=403)
    return render(request, 'odeme/musteri_bilgileri/index23.html', {'isletme': isletme})


def isletme_odeme_on_izleme(request, isletme_slug):
    isletme = get_object_or_404(GenelAyar, slug=isletme_slug)
    if not getattr(isletme, 'yayinla', True):
        return JsonResponse({"error": "Bu işletme yayında değil"}, status=403)
    return render(request, 'odeme/on_izleme/index24.html', {'isletme': isletme})
