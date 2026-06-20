from django.conf import settings
from django.db import migrations
from django.contrib.auth.hashers import make_password


def crear_usuario_panel(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    User.objects.update_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'password': make_password('Admin1234'),
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        }
    )


def eliminar_usuario_panel(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mi_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(crear_usuario_panel, eliminar_usuario_panel),
    ]