# Generated by Django 4.2.20 on 2025-06-02 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_paymentlog_method_paymentorder_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentlog',
            name='method',
            field=models.CharField(choices=[('ecpay', '綠界'), ('linepay', 'LINE Pay')], max_length=20),
        ),
        migrations.AlterField(
            model_name='paymentorder',
            name='method',
            field=models.CharField(choices=[('ecpay', '綠界'), ('linepay', 'LINE Pay')], max_length=20),
        ),
    ]
