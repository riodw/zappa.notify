# Generated by Django 2.1.3 on 2018-11-13 21:09

from django.db import migrations, models
import notification.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(default=notification.models.keyGen, editable=False, max_length=32, unique=True)),
                ('message', models.TextField()),
                ('subject', models.CharField(default='Notify Notification', max_length=254)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.EmailField(max_length=255)),
                ('sender', models.EmailField(max_length=254)),
                ('source', models.CharField(max_length=254)),
                ('type', models.IntegerField(default=0)),
                ('runs', models.IntegerField(default=0)),
                ('sent', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['datetime'],
            },
        ),
    ]
