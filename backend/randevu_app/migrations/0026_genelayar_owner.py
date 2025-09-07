from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('randevu_app', '0025_auto_add_business_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='genelayar',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='isletmeler', to='auth.user'),
        ),
    ] 