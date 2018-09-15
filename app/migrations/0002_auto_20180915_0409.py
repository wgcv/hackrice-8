# Generated by Django 2.1.1 on 2018-09-15 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='transaction',
            name='type_transaction',
            field=models.CharField(choices=[('DP', 'Deposit'), ('WD', 'Withdrawal'), ('PM', 'Payment'), ('TR', 'Transference')], default='', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datauser',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
