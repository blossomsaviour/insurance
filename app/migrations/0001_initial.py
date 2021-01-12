# Generated by Django 3.0.5 on 2020-12-30 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insurance_name', models.CharField(max_length=30)),
                ('insurance_basic_price', models.IntegerField()),
                ('insurance_type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=30)),
                ('vehicle_name', models.CharField(max_length=30)),
                ('vehicle_number', models.CharField(max_length=30)),
                ('vehicle_reg_year', models.DateField()),
                ('vehicle_price', models.IntegerField()),
                ('insurance_name', models.CharField(max_length=30)),
                ('insurance_type', models.IntegerField()),
                ('insurance_price', models.IntegerField()),
            ],
        ),
    ]
