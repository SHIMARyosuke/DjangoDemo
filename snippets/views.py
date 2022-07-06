from django.shortcuts import render
from django.http import HttpResponse

# スニペットお一覧を表示
# GET /
def top(request):
    return HttpResponse(b"Hello World")

# スニペットの登録フォームの表示
# GET /snippets/new/
def snippet_new(request):
    return HttpResponse('スニペットの登録')

def snippet_edit(request, snippet_id):
    return HttpResponse('スニペットの編集')

def snippet_detail(request, snippet_id):
    return HttpResponse('スニペットの詳細閲覧')

# 登録処理
# POST /snippets/new/

# 詳細閲覧
# GET /snippets/<snippet_id>/

# 編集フォーム表示
# GET /snippets/<snippet_id>/edit/

# 編集処理
# POST /snippets/<snippet_id>/edit/
