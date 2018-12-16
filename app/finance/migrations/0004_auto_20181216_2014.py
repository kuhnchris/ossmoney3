# Generated by Django 2.1.4 on 2018-12-16 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_invoiceposition_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicehead',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='invoiceposition',
            name='head',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position', to='finance.invoiceHead'),
        ),
        migrations.AlterField(
            model_name='invoiceposition',
            name='position',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]