from django.shortcuts import render,get_object_or_404,redirect
from . import models
from . import forms
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse,reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic import (View,TemplateView,ListView,DetailView,
                                    CreateView,UpdateView,DeleteView,FormView)
                            

# Create your views here.
class AboutView(TemplateView):
    template_name = "blog/about.html"
    

class PostListView(ListView):
    model = models.Post
    template_name = "blog/post_list.html"

    def get_queryset(self):
        return models.Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        # lte = less than or equal to
        # -published_date: ordered by publish date by descending order
        # Go to Field lookups https://docs.djangoproject.com/en/3.0/ref/models/querysets/#id4
 
class PostDetailView(DetailView):
    model = models.Post

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.CommentForm
        return context
    
class PostCreateView(LoginRequiredMixin,CreateView):
    login_url = 'login/'
    # redirect_field_name = 'blog/post_list.html'
    model = models.Post
    form_class = forms.PostForm
    
class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = models.Post
    form_class = forms.PostForm
    
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = models.Post

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull=True).order_by('-create_date')

##########################
##########################

# Function Based View

@login_required
def add_comment_to_post(request,pk):

    post = get_object_or_404(models.Post, pk=pk)
    form = forms.CommentForm()
    
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = forms.CommentForm()
    return redirect('post_detail', pk=post.pk)
    
    
@login_required
def approve_comment(request,pk):
    comment = get_object_or_404(models.Comment,pk=pk)
    comment.approve_comment()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def remove_comment(request,pk):
    comment = get_object_or_404(models.Comment,pk=pk)
    post_pk = comment.post.pk #save it as a variable before deletion
    comment.delete()
    return redirect('post_detail',pk=post_pk)

@login_required
def publish_draft(request,pk):
    post = get_object_or_404(models.Post,pk=pk)
    post.publish()
    messages.success(request, 'Draft has been published.')
    return redirect('post_detail',pk=post.pk)

            


