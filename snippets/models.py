from django.conf import settings
from django.db import models


class SnippetQuerySet(models.QuerySet):
    # 下書き状態のスニペットを返す
    def drafts(self):
        return self.filter(is_draft=False)

    # 直近に更新されたスニペットを返す
    def recent_updates(self):
        return self.order_by('-updated_at')

    recent_updates.queryset_only = True

class DraftSnippetManager(models.Manager):
    # 下書き状態のスニペットを返す
    def get_queryset(self):
        return super().get_queryset().filter(is_draft=True)

class Snippet(models.Model):
    title = models.CharField('タイトル', max_length=128)
    code = models.TextField('コード', blank=True)
    description = models.TextField('説明', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name="投稿者",
                                   on_delete=models.CASCADE)
    is_draft = models.BooleanField('下書き', default=False)
    created_at = models.DateTimeField("投稿日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    # モデルマネージャの読み込み
    objects = models.Manager()
    drafts = DraftSnippetManager()

    # QuerySetを使いたい場合
    # objects = SnippetQuerySet.as_manager()

    # マネージャとQuerySetを同時に使いたい場合
    # from_querysetメソッドは、QuerySetを受け取って Manager クラスを生成するため、さらに括弧が必要
    # objects = DraftSnippetManager.from_queryset(SnippetQuerySet)()

    def __str__(self):
        return f'{self.pk} {self.title}'

    # Meta オプション
    class Meta:
        # テーブル名を明示的に指定する
        db_table = 'snippets'

class Comment(models.Model):
    text = models.TextField('本文', blank=False)
    comment_to = models.ForeignKey(
        Snippet,
        verbose_name = 'スニペット',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.pk} {self.text}'

    class Meta:
        db_table = 'comments'

class Tag(models.Model):
    name = models.CharField(
        'タグ名',
        max_length = 32
    )

    # snippetsテーブルとtagsテーブルを多対多の関係で紐付ける。
    # 中間テーブルは自動で生成される
    snippets = models.ManyToManyField(
        Snippet,
        related_name='tags',
        related_query_name='tag'
    )

    def __str__(self):
        return f'{self.pk} {self.name}'

    class Meta:
        db_table = 'tags'
