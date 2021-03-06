# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-29 21:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('datasetid', models.AutoField(primary_key=True, serialize=False)),
                ('dataset_name', models.CharField(max_length=200)),
                ('dataset_rootpath', models.FilePathField(blank=True, max_length=500)),
                ('dataset_startdate', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='date initialized')),
                ('dataset_description', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('imageid', models.AutoField(primary_key=True, serialize=False)),
                ('image_filepath', models.FilePathField(max_length=500)),
                ('image_spaceorigin', models.CharField(default='Unknown', max_length=200)),
                ('image_endian', models.CharField(default='Unknown', max_length=200)),
                ('image_spacedirections', models.CharField(default='Unknown', max_length=200)),
                ('image_space', models.CharField(default='Unknown', max_length=200)),
                ('image_sizes', models.CharField(default='Unknown', max_length=200)),
                ('image_encoding', models.CharField(default='Unknown', max_length=200)),
                ('image_nrrdname', models.CharField(default='Unknown', max_length=200)),
                ('image_kinds', models.CharField(default='Unknown', max_length=200)),
                ('image_type', models.CharField(default='Unknown', max_length=200)),
                ('image_dimension', models.CharField(default='Unknown', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patientid', models.AutoField(primary_key=True, serialize=False)),
                ('patient_rootpath', models.FilePathField(blank=True, max_length=500)),
                ('patient_dicomid', models.CharField(default='Anonymized', max_length=200)),
                ('fk_patient_dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='databrowser.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='Segmentation',
            fields=[
                ('segmentationid', models.AutoField(primary_key=True, serialize=False)),
                ('segmentation_filepath', models.FilePathField(max_length=500)),
                ('segmentation_spaceorigin', models.CharField(default='Unknown', max_length=200)),
                ('segmentation_endian', models.CharField(default='Unknown', max_length=200)),
                ('segmentation_spacedirections', models.CharField(default='Unknown', max_length=200)),
                ('segmentation_space', models.CharField(default='Unknown', max_length=200)),
                ('segmentation_sizes', models.CharField(default='Unknown', max_length=200)),
                ('segmentation_encoding', models.CharField(default='Unknown', max_length=200)),
                ('segmentation_nrrdname', models.CharField(default='Unknown', max_length=200)),
                ('segmentation_kinds', models.CharField(default='Unknown', max_length=200)),
                ('segmentation_type', models.CharField(default='Unknown', max_length=200)),
                ('segmentation_dimension', models.CharField(default='Unknown', max_length=200)),
                ('segmentation_validationstatus', models.CharField(choices=[('1', 'Missing'), ('2', 'Invalidated'), ('3', 'Validated')], default='1', max_length=1)),
                ('fk_segmentation_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='databrowser.Image')),
            ],
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('studyid', models.AutoField(primary_key=True, serialize=False)),
                ('study_rootpath', models.FilePathField(blank=True, max_length=500)),
                ('study_name', models.CharField(default='Unknown Study', max_length=200)),
                ('fk_study_patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='databrowser.Patient')),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='fk_image_study',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='databrowser.Study'),
        ),
    ]
