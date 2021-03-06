# Generated by Django 4.0.3 on 2022-04-11 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0010_teamabout_alter_order_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeSlider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('image', models.ImageField(upload_to='Home-Slider/images/')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Order Canceled', 'Order Canceled'), ('Order Completed', 'Order Completed'), ('Order Processing', 'Order Processing'), ('On the way', 'On the way'), ('Order Received', 'Order Received')], max_length=50),
        ),
    ]
