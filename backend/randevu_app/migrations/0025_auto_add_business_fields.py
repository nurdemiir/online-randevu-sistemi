from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('randevu_app', '0024_genelayar_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='genelayar',
            name='yayinla',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='personel',
            name='isletme_adi',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hizmet',
            name='isletme_adi',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ] 