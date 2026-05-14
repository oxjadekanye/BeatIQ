from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_user_email_verified_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="birth_year",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="birth_month",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
