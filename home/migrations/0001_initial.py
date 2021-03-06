# Generated by Django 3.1.2 on 2020-10-17 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('content', models.TextField(max_length=10000)),
                ('status', models.CharField(default='noreply', max_length=100)),
                ('contact_dt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
