# Generated by Django 3.2.4 on 2021-06-13 04:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(choices=[(5, 'YES😃'), (3, 'MAYBE😐'), (1, 'NO😫')], verbose_name='レビュースコア')),
                ('comment', models.TextField(blank=True, verbose_name='レビューコメント（NOの場合は必須）')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reviews', to='review.proposal', verbose_name='レビュー対象のプロポーザル')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='レビュアー')),
            ],
        ),
    ]