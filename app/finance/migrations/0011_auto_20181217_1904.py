# Generated by Django 2.1.4 on 2018-12-17 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0010_auto_20181217_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='UOM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('changed_on', models.DateTimeField(auto_now=True)),
                ('short_name', models.TextField(max_length=5)),
                ('long_name', models.TextField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='invoiceposition',
            old_name='amount',
            new_name='per_amount_price',
        ),
        migrations.AddField(
            model_name='invoiceposition',
            name='per_amount_price_unit',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='invoiceposition',
            name='purchase_amount',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='invoiceposition',
            name='head',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='finance.InvoiceHead'),
        ),
        migrations.RemoveField(
            model_name='invoiceposition',
            name='materialGroup',
        ),
        migrations.AddField(
            model_name='invoiceposition',
            name='materialGroup',
            field=models.ManyToManyField(blank=True, null=True, to='finance.MaterialGroup'),
        ),
        migrations.AddField(
            model_name='invoiceposition',
            name='unit_of_measure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.UOM'),
        ),
    ]