# Generated by Django 5.0.1 on 2024-04-21 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='visit',
            name='eating_status',
            field=models.CharField(blank=True, choices=[('before_eating', 'Before Eating'), ('after_eating', 'After Eating')], max_length=20),
        ),
        migrations.RemoveField(
            model_name='visit',
            name='medicine_name',
        ),
        migrations.AddField(
            model_name='visit',
            name='medicine_name',
            field=models.ManyToManyField(to='shop.medicine'),
        ),
    ]
