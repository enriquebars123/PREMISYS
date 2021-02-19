# Generated by Django 3.0.4 on 2020-05-28 02:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aduana', models.IntegerField()),
                ('turno', models.IntegerField()),
                ('nomina', models.CharField(max_length=255)),
                ('nombre', models.CharField(max_length=255)),
                ('area_origen', models.CharField(max_length=255)),
                ('area_destino', models.CharField(max_length=255)),
                ('motivo', models.CharField(max_length=255)),
                ('epp', models.BooleanField(default=False)),
                ('lentes', models.BooleanField(default=False)),
                ('caretas', models.BooleanField(default=False)),
                ('cubrebocas', models.BooleanField(default=False)),
                ('nomina_aduana', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'meraki_registro_empleados',
            },
        ),
        migrations.CreateModel(
            name='EmpleadoExcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomina', models.CharField(max_length=255)),
                ('nombre', models.CharField(max_length=255)),
                ('planta', models.CharField(max_length=255)),
                ('mac', models.CharField(max_length=255)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'meraki_registro_empleados_excel',
            },
        ),
    ]
