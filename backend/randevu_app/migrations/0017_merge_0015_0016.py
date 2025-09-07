from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('randevu_app', '0015_remove_personel_hizmetler_personel_hizmetler'),
        ('randevu_app', '0016_randevu_iletisim_tercihleri_kvkk'),
    ]

    operations = [
        # Bu migration sadece iki dalı birleştirir, DB üzerinde değişiklik yapmaz
    ]
