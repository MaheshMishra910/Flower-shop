# Generated by Django 4.0.3 on 2022-04-02 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_wishlist_alter_order_order_status_wishlistproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=0)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainApp.customer')),
            ],
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('On the way', 'On the way'), ('Order Completed', 'Order Completed'), ('Order Received', 'Order Received'), ('Order Processing', 'Order Processing'), ('Order Canceled', 'Order Canceled')], max_length=50),
        ),
        migrations.CreateModel(
            name='CompareProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('subtotal', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.product')),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.compare')),
            ],
        ),
    ]
