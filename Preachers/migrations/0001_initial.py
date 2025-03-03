# Generated by Django 5.0.7 on 2024-07-23 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Preacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preacher_name', models.CharField(max_length=100)),
                ('church_name', models.CharField(max_length=100)),
                ('stream_link_id', models.CharField(max_length=100)),
                ('thumbnail', models.ImageField(upload_to='')),
                ('is_live', models.BooleanField(default=True)),
                ('pinned_list_id', models.IntegerField(default=0)),
            ],
        ),
    ]
