from django.conf import settings
from django.db import models


class Proposal(models.Model):
    class SessionTrack(models.TextChoices):
        # ref: https://pyconjp.blogspot.com/2021/05/2021-proposal-track.html
        CORE_AND_AROUND = "Python core and around", "Python core and around"
        MACHINE_LEARNING = "Machine learning", "Machine learning"
        WEB_PROGRAMMING = "Web programming", "Web programming"
        VISUAL_GAME_MUSIC = "Visual / Game / Music", "Visual / Game / Music"
        SOCIAL_PROBLEM = (
            "Outside of Python language",
            "Outside of Python language",
        )
        OUTSIDE_LANGUAGE = (
            "Approaching to social problem",
            "Approaching to social problem",
        )
        FUN_OR_NEW = (
            "Only for fun or try new techniques",
            "Only for fun or try new techniques",
        )
        ANYTHING_ELSE = (
            "Anything else basically which doesn’t fall into the types of "
            "topics above",
            "Anything else basically which doesn’t fall into the types of "
            "topics above",
        )

    class AudiencePythonKnowledge(models.TextChoices):
        # ref: https://pyconjp.blogspot.com/2021/05/2021-proposal-audience.html
        BEGINNER = (
            "Beginner",
            "Beginner：PythonチュートリアルなどでPythonの文法や標準ライブラリの使い方を学んでいる",
        )
        INTERMEDIATE = (
            "Intermediate",
            "Intermediate：Pythonチュートリアルを終え、サードパーティーライブラリを使って、"
            "Webアプリ開発、データ分析、自動化などのいずれかに取り組んでいる",
        )
        ADVANCED = (
            "Advanced",
            "Advanced：Pythonを数年使っていて、パッケージを公開していたり、"
            "Pythonのパフォーマンスや内部実装に関心があったりする",
        )
        EXPERT = ("Expert", "Expert：Python自体やよく知られたPythonライブラリに開発で貢献している")

    class SpeakingLanguage(models.TextChoices):
        JAPANESE = "ja", "Japanese"
        ENGLISH = "en", "English"

    class SlideLanguage(models.TextChoices):
        JAPANESE = "ja", "Japanese"
        ENGLISH = "en", "English"
        BOTH = "bo", "Both"

    sessionize_id = models.PositiveIntegerField("SessionizeにおけるプロポーザルID")

    title = models.CharField("セッションタイトル", max_length=100)  # Same as 2020
    description = models.TextField("詳細（構成・タイムライン）")
    # 100字以上、200字程度 / up to 50 words (minimum 30 words)
    elevator_pitch = models.CharField("概要（エレベータピッチ）", max_length=300)
    track = models.CharField(
        "セッションのカテゴリ", max_length=73, choices=SessionTrack.choices
    )
    audience_python_level = models.CharField(
        "聴衆のPythonのレベル", max_length=12, choices=AudiencePythonKnowledge.choices
    )
    audience_prior_knowledge = models.TextField("聴衆に求める前提知識")
    audience_take_away = models.TextField("聴衆が持って帰れる具体的な知識やノウハウ")
    motivation_and_why = models.TextField(
        "この題材を話すのに自分がふさわしいと考える理由やこのトークをするモチベーション"
    )
    materials_url = models.TextField(
        "このトピックについて過去の登壇で使った資料やソースコードのURL", blank=True
    )
    speaking_language = models.TextField(
        "発表の言語", max_length=2, choices=SpeakingLanguage.choices
    )
    slide_language = models.TextField(
        "スライドの言語", max_length=2, choices=SlideLanguage.choices
    )

    reviewer_not_displayed_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="投稿者（レビュー不可）",
        blank=True,
        null=True,
    )
    # 同じユーザで複数提出を確認できる機能を実装するために2020から追加
    submit_user_id = models.UUIDField("Sessionizeにおける、投稿者のユーザID")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.sessionize_id} {self.title}"
