from django.conf import settings
from django.db import models

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
