# Generated by Django 3.2.4 on 2021-06-12 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessionize_id', models.PositiveIntegerField(verbose_name='SessionizeにおけるプロポーザルID')),
                ('title', models.CharField(max_length=100, verbose_name='セッションタイトル')),
                ('description', models.TextField(verbose_name='詳細（構成・タイムライン）')),
                ('elevator_pitch', models.CharField(max_length=300, verbose_name='概要（エレベータピッチ）')),
                ('track', models.CharField(choices=[('Python core and around', 'Python core and around'), ('Machine learning', 'Machine learning'), ('Web programming', 'Web programming'), ('Visual / Game / Music', 'Visual / Game / Music'), ('Outside of Python language', 'Outside of Python language'), ('Approaching to social problem', 'Approaching to social problem'), ('Only for fun or try new techniques', 'Only for fun or try new techniques'), ('Anything else basically which doesn’t fall into the types of topics above', 'Anything else basically which doesn’t fall into the types of topics above')], max_length=73, verbose_name='セッションのカテゴリ')),
                ('audience_python_level', models.CharField(choices=[('Beginner', 'Beginner：PythonチュートリアルなどでPythonの文法や標準ライブラリの使い方を学んでいる'), ('Intermediate', 'Intermediate：Pythonチュートリアルを終え、サードパーティーライブラリを使って、Webアプリ開発、データ分析、自動化などのいずれかに取り組んでいる'), ('Advanced', 'Advanced：Pythonを数年使っていて、パッケージを公開していたり、Pythonのパフォーマンスや内部実装に関心があったりする'), ('Expert', 'Expert：Python自体やよく知られたPythonライブラリに開発で貢献している')], max_length=12, verbose_name='聴衆のPythonのレベル')),
                ('audience_prior_knowledge', models.TextField(verbose_name='聴衆に求める前提知識')),
                ('audience_take_away', models.TextField(verbose_name='聴衆が持って帰れる具体的な知識やノウハウ')),
                ('motivation_and_why', models.TextField(verbose_name='この題材を話すのに自分がふさわしいと考える理由やこのトークをするモチベーション')),
                ('materials_url', models.TextField(blank=True, verbose_name='このトピックについて過去の登壇で使った資料やソースコードのURL')),
                ('speaking_language', models.TextField(choices=[('ja', 'Japanese'), ('en', 'English')], max_length=2, verbose_name='発表の言語')),
                ('slide_language', models.TextField(choices=[('ja', 'Japanese'), ('en', 'English'), ('bo', 'Both')], max_length=2, verbose_name='スライドの言語')),
                ('submit_user_id', models.UUIDField(verbose_name='Sessionizeにおける、投稿者のユーザID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reviewer_not_displayed_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='投稿者（レビュー不可）')),
            ],
        ),
    ]