# Generated by Django 2.1.2 on 2018-11-30 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_unjsonify_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalwork',
            name='media_of_origin',
            field=models.CharField(blank=True, choices=[('Digital', 'Digital'), ('Cinta', 'Cinta'), ('CD', 'CD'), ('Vinilo', 'Vinilo')], default='Digital', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='historicalworktoworkrel',
            name='relationship',
            field=models.TextField(blank=True, choices=[('Series<contains>Album', 'Is the series which contains this album.'), ('Series<contains>Recording', 'Is the series which contains this track.'), ('Series<influenced>Recording', 'Is a series which influenced this track.')], default='Series<contains>Recording', null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='media_of_origin',
            field=models.CharField(blank=True, choices=[('Digital', 'Digital'), ('Cinta', 'Cinta'), ('CD', 'CD'), ('Vinilo', 'Vinilo')], default='Digital', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='worktoworkrel',
            name='relationship',
            field=models.TextField(blank=True, choices=[('Series<contains>Album', 'Is the series which contains this album.'), ('Series<contains>Recording', 'Is the series which contains this track.'), ('Series<influenced>Recording', 'Is a series which influenced this track.')], default='Series<contains>Recording', null=True),
        ),
    ]
