from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

# urls.py에서 여기로 넘어옴. 
# 해당되는 url에 대한 view함수 실행됨.
# return할 때 render할 html 파일 지정
# +) html 파일에서 필요한 값 넘겨주기 (ex:'post_test' 라는 변수가 필요)
# 한 번 정해진 pk는 변하지 않는다. 중간 게시글 삭제하더라도!

# post list view
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html',{'post_test':posts})

#post detail view
def post_detail(request, pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request, 'blog/post_detail.html',{'post':post})

#edit post
#@login_required
def post_new(request):
    #request.POST, request.FILES
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES) #files 역할??
        if form.is_valid(): #빠진 값이 없는가
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save() #db에 저장
            return redirect('post_detail', pk=post.pk) #post_detail이라는 view로 이동 (바로 위에 정의된거)
    else:  #그럼 이건 POST말고 어떤방식?
        form = PostForm() 
    return render(request,'blog/post_edit.html',{'form':form})

def post_edit(request,pk):
    post = get_object_or_404(Post, pk=pk) #pk로 원하는(수정하고자 하는) 글을 찾는다
    if request.method == "POST": #post (save 버튼 눌렀을 때 db 저장)
        form = PostForm(request.POST, request.FILES, instance=post) #이전에 입력했던 폼과 데이터 가져옴 
        post = form.save(commit=False)                              #instance=post를 빼면 새로운 게시글로 추가되는구낭
        if form.is_valid():
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else: #get (맨처음에 edit 페이지 보여주기)
        form = PostForm(instance=post) #placeholder가 되는 form을 html(front)로 넘겨줌
    return render(request, 'blog/post_edit.html', {'form': form})