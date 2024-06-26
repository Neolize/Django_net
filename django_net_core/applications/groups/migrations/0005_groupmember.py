# Generated by Django 4.2.1 on 2024-03-28 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0004_grouppost_user_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_members', to='groups.group')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_member', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'group_member',
            },
        ),
    ]
