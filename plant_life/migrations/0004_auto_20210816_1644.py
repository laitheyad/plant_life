# Generated by Django 3.2.6 on 2021-08-16 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plant_life', '0003_auto_20210814_0110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.FloatField(default=10.0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plant_life.category')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plant_life.shop')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plant_life.shop'),
        ),
    ]