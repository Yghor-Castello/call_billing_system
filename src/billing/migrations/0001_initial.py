# Generated by Django 5.1.3 on 2024-11-19 00:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11)),
                ('period_start', models.DateField()),
                ('period_end', models.DateField()),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='CallRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('start', 'Start'), ('end', 'End')], max_length=5)),
                ('timestamp', models.DateTimeField()),
                ('call_id', models.CharField(max_length=50)),
                ('source', models.CharField(blank=True, max_length=11, null=True)),
                ('destination', models.CharField(blank=True, max_length=11, null=True)),
            ],
            options={
                'unique_together': {('call_id', 'type')},
            },
        ),
        migrations.CreateModel(
            name='CallDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=11)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('phone_bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='call_details', to='billing.phonebill')),
            ],
        ),
    ]