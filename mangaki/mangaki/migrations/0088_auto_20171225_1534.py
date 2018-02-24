# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-25 15:34
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.http import _urlsplit, limited_parse_qsl

def infer_source(url):
    if 'myanimelist' in url:
        return 'MAL'
    elif 'anidb' in url:
        return 'AniDB'
    elif 'manga-news' in url:
        return 'Manga-News'
    elif 'icotaku' in url:
        return 'Icotaku'
    elif 'animeka' in url:
        return 'Animeka'
    elif 'vgmdb' in url:
        return 'VGMdb'
    else:
        _, netloc, _, _, _ = _urlsplit(url)
        return netloc

def infer_identifier(url, source):
    if source == 'MAL':
        # structure is: protocol://myanimelist.net/(type)/(identifier)
        return int(url.split('/')[4])
    elif source == 'AniDB':
        _, _, _, query_encoded, _ = _urlsplit(url)
        query_params = dict(limited_parse_qsl(query_encoded))
        return query_params.get('aid', None)
    elif source == 'Manga-News':
        # structure is: protocol://www.manga-news.com/index.php/serie/(identifier)
        return url.split('/')[5]
    elif source == 'Icotaku':
        # structure is: protocol://anime.icotaku.com/anime/(identifier)/(name)
        return int(url.split('/')[4])
    elif source == 'Animeka':
        # structure is
        # protocol://www.animeka.com/animes/detail/(identifier).html
        return url.split('/')[5][:-5]
    elif source == 'VGMdb':
        # structure is the same as MAL.
        return int(url.split('/')[4])
    else:
        raise ValueError('Unknown source')

def copy_url_to_id_and_source(apps, schema_editor):
    Reference = apps.get_model('mangaki', 'Reference')
    db_alias = schema_editor.connection.alias
    for ref in Reference.objects.using(db_alias).iterator():
        try:
            ref.source = infer_source(ref.url.lower())
            ref.identifier = infer_identifier(ref.url, ref.source)
            ref.save(using=db_alias)
        except (TypeError, ValueError) as e:
            print('Failed to data-migrate: {} - {} ({})'.format(ref.id, ref.url, e))
            continue

def copy_source_field_to_reference(apps, schema_editor):
    Reference = apps.get_model('mangaki', 'Reference')
    Work = apps.get_model('mangaki', 'Work')
    db_alias = schema_editor.connection.alias
    for work in Work.objects.using(db_alias).exclude(source='').iterator():
        try:
            source = infer_source(work.source.lower())
            identifier = infer_identifier(work.source, source)
            if identifier is not None:
                ref = Reference.objects.get_or_create(work=work,
                                source=source,
                                identifier=identifier,
                                url=work.source)
        except (TypeError, ValueError) as e:
            print('Failed to data-migrate: {} - {} ({})'.format(ref.id, ref.url, e))
            continue

# migrations.RunPython.noop cause circular reference error…
def noop(apps, schema_editor):
    return None

class Migration(migrations.Migration):

    dependencies = [
        ('mangaki', '0087_auto_20171023_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='identifier',
            field=models.CharField(default="none", max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reference',
            name='source',
            field=models.CharField(default='unknown', max_length=100),
            preserve_default=False,
        ),
        migrations.RunPython(copy_url_to_id_and_source,
                             reverse_code=migrations.RunPython.noop),
        migrations.RunPython(copy_source_field_to_reference,
                             reverse_code=migrations.RunPython.noop)
    ]
