from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('randevu_app', '0002_genelayar_guncellenme'),
    ]

    operations = [
        migrations.AddField(
            model_name='randevu',
            name='sms',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='randevu',
            name='email_notif',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='randevu',
            name='whatsapp',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='randevu',
            name='kvkk',
            field=models.BooleanField(default=False),
        ),
    ] 