# Generated by Django 4.2.6 on 2023-10-06 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_alter_employee_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]