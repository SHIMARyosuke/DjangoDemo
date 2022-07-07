from django.shortcuts import render, get_object_or_404, redirect
from snippets.models import Snippet
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from snippets.forms import SnippetForm
# スニペットお一覧を表示
# GET /

def top(request):
    snippets = Snippet.objects.all()
    context = {"snippets": snippets}
    return render(request, "snippets/top.html", context)

# スニペットの登録フォームの表示
# GET /snippets/new/
@login_required
def snippet_new(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.created_by = request.user
            snippet.save()
            return redirect(snippet_detail, snippet_id=snippet.pk)

    else:
        form = SnippetForm()
        return render(request, "snippets/snippet_new.html", {'form': form})


# スニペットの編集
@login_required
def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if snippet.created_by_id != request.user.id:
        return HttpResponseForbidden("このスニペットの編集は許可されていません")

    if request.method == "POST":
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect('snippet_detail', snippet_id=snippet_id)
    else:
        form = SnippetForm(instance=snippet)
        return render(request, 'snippets/snippet_edit.html', {'form': form})
    return HttpResponse('スニペットの編集')

def snippet_detail(request, snippet_id):
    # get_object_or_404は、DBからデータが見つからなかった場合 django.http.Http404例外を投げる
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    return render(request, 'snippets/snippet_detail.html', {'snippet': snippet})

# 登録処理
# POST /snippets/new/

# 詳細閲覧
# GET /snippets/<snippet_id>/

# 編集フォーム表示
# GET /snippets/<snippet_id>/edit/

# 編集処理
# POST /snippets/<snippet_id>/edit/
