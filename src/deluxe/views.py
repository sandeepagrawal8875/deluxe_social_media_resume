from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .forms import NewCommentForm
from users.models import Follow, Profile
from .models import *

import sys
import time


@login_required(login_url='login')
def home(request):
    profile = Profile.objects.filter(user=request.user)
    skills_obj = Skills.objects.filter(author=request.user)
    education_obj = Education.objects.filter(author=request.user)
    blog_p = Blog.objects.filter(author=request.user).order_by("-id")
    project_p = Project.objects.filter(author=request.user).order_by("-id")
    certificate_p = Certificate.objects.filter(author=request.user).order_by("-id")
    hobby_obj = Hobby.objects.filter(author=request.user)

    blog_count = blog_p.count()
    page = request.GET.get('page', 1)

    # blog paginator
    paginator = Paginator(blog_p, 3)
    try:
        blog_obj = paginator.page(page)
    except PageNotAnInteger:
        blog_obj = paginator.page(1)
    except EmptyPage:
        blog_obj = paginator.page(paginator.num_pages)

    # project paginator
    paginator = Paginator(project_p, 10)
    try:
        project_obj = paginator.page(page)
    except PageNotAnInteger:
        project_obj = paginator.page(1)
    except EmptyPage:
        project_obj = paginator.page(paginator.num_pages)

    # certificate paginator
    paginator = Paginator(certificate_p, 10)
    try:
        certificate_obj = paginator.page(page)
    except PageNotAnInteger:
        certificate_obj = paginator.page(1)
    except EmptyPage:
        certificate_obj = paginator.page(paginator.num_pages)

    # time
    currentTime = time.strftime('%H')   
    if int(currentTime) < 12 :
        greet = 'Good morning'
    elif int(currentTime) > 12  and  int(currentTime) < 17:
        greet = 'Good afternoon'
    else :
        greet = 'Good evening'

    context = {
        'profile':profile,
        'education_obj':education_obj,
        'blog_obj':blog_obj,
        'project_obj':project_obj,
        'certificate_obj':certificate_obj,
        'skills_obj':skills_obj,
        'greet':greet,
        'hobby_obj':hobby_obj,
        'blog_count':blog_count,
    }
    return render(request,'deluxe/home.html',context)

@login_required(login_url='login')
def userPostListView(request,username):
    p_user = get_object_or_404(User, username=username)
    profile = Profile.objects.filter(user=p_user)
    skills_obj = Skills.objects.filter(author=p_user)
    education_obj = Education.objects.filter(author=p_user)
    blog_p = Blog.objects.filter(author=p_user).order_by("-id")
    project_p = Project.objects.filter(author=p_user).order_by("-id")
    certificate_p = Certificate.objects.filter(author=p_user).order_by("-id")
    hobby_obj = Hobby.objects.filter(author=p_user)

    blog_count = blog_p.count()
    page = request.GET.get('page', 1)

    # blog paginator
    paginator = Paginator(blog_p, 3)
    try:
        blog_obj = paginator.page(page)
    except PageNotAnInteger:
        blog_obj = paginator.page(1)
    except EmptyPage:
        blog_obj = paginator.page(paginator.num_pages)


    # project paginator
    paginator = Paginator(project_p, 10)
    try:
        project_obj = paginator.page(page)
    except PageNotAnInteger:
        project_obj = paginator.page(1)
    except EmptyPage:
        project_obj = paginator.page(paginator.num_pages)

    # certificate paginator
    paginator = Paginator(certificate_p, 10)
    try:
        certificate_obj = paginator.page(page)
    except PageNotAnInteger:
        certificate_obj = paginator.page(1)
    except EmptyPage:
        certificate_obj = paginator.page(paginator.num_pages)


    logged_user = request.user

    if logged_user.username == '' or logged_user is None:
        can_follow = False
    else:
        can_follow = (Follow.objects.filter(user=logged_user,
                                            follow_user=p_user).count() == 0)



    if request.user.id is not None:
        follows_between = Follow.objects.filter(user=request.user,
                                                follow_user=p_user)
        if 'follow' in request.POST:
            new_relation = Follow(user=request.user, follow_user=p_user)
            if follows_between.count() == 0:
                new_relation.save()
                return redirect(userPostListView, username=p_user)
        elif 'unfollow' in request.POST:
            if follows_between.count() > 0:
                follows_between.delete()
                return redirect(userPostListView, username=p_user)


    context = {
        'p_user':p_user,
        'profile':profile,
        'education_obj':education_obj,
        'blog_obj':blog_obj,
        'project_obj':project_obj,
        'certificate_obj':certificate_obj,
        'skills_obj':skills_obj,
        'can_follow':can_follow,
        'hobby_obj':hobby_obj,
        'blog_count':blog_count,
    }
    return render(request, "deluxe/user_post.html",context)


# Blog

class BlogListView(LoginRequiredMixin, TemplateView):

    template_name = 'deluxe/blog_list.html'

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        blogList = Blog.objects.all()
        user = self.request.user
        followedList = Follow.objects.filter(user=self.request.user)
        followedList2 = [user]

        for e in followedList:
            followedList2.append(e.follow_user)
        blogList = Blog.objects.filter(author__in=followedList2).order_by("-id")
        for p1 in blogList:
            p1.liked = False
            ob = BlogLike.objects.filter(blog=p1, liked_by=self.request.user)
            if ob:
                p1.liked = True
            obj_List = BlogLike.objects.filter(blog=p1)
            p1.likedno = obj_List.count()
        context["blog_obj"] = blogList
        return context

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['text','picture']
    template_name = 'deluxe/create_blog.html'
    success_url = '/#blog'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Create Post'
        return data

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = 'deluxe/delete_blog.html'
    context_object_name = 'blog'
    success_url = '/#blog'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'delete blog'
        return data

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['text','picture']
    template_name = 'deluxe/update_blog.html'
    success_url = '/#blog'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Update Blog'
        return data


# blog detail & Comment

class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = 'deluxe/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(blog_connected=self.get_object()).order_by('-cr_date')
        data['comments'] = comments_connected
        data['form'] = NewCommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        try :
            new_comment = Comment(text=request.POST.get('text'),
                                picture=request.FILES['picture'],
                                author=self.request.user,
                                blog_connected=self.get_object())
        except:
            new_comment = Comment(text=request.POST.get('text'),
                                author=self.request.user,
                                blog_connected=self.get_object())

        new_comment.save()

        return self.get(self, request, *args, **kwargs)

class BlogCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'deluxe/delete_comment.html'
    context_object_name = 'comment'
    success_url = '/'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'delete Comment'
        return data

class BlogCommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['text','picture']
    template_name = 'deluxe/update_comment.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Update Comment'
        return data


# Skills

class SkillsCreateView(LoginRequiredMixin, CreateView):
    model = Skills
    fields = ['skill','percentage']
    template_name = 'deluxe/add_skills.html'
    success_url = '/#skills'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add Skills'
        return data

class SkillsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Skills
    template_name = 'deluxe/delete_skills.html'
    context_object_name = 'skills'
    success_url = '/#skills'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'delete Skills'
        return data

class SkillsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Skills
    fields = ['skill','percentage']
    template_name = 'deluxe/update_skills.html'
    success_url = '/#skills'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Update Skills'
        return data


# Certificate

class CertificateCreateView(LoginRequiredMixin, CreateView):
    model = Certificate
    fields = ['certificate_pic','certificate_title','source']
    template_name = 'deluxe/add_certificate.html'
    success_url = '/#certificate'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add Certificate'
        return data

class CertificateDetailView(LoginRequiredMixin, DetailView):
    model = Certificate
    template_name = 'deluxe/certificate_detail.html'
    context_object_name = 'certificate'

class CertificateDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Certificate
    template_name = 'deluxe/delete_certificate.html'
    context_object_name = 'certificate'
    success_url = '/#certificate'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'delete Certificate'
        return data

class CertificateUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Certificate
    fields = ['certificate_pic','certificate_title','source']
    template_name = 'deluxe/update_certificate.html'
    success_url = '/#certificate'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Update Certificate'
        return data


# Education

class EducationCreateView(LoginRequiredMixin, CreateView):
    model = Education
    fields = ['start_year','end_year','dgree_name','about','dgree_document']
    template_name = 'deluxe/add_education.html'
    success_url = '/#education'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add Education'
        return data

class EducationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Education
    template_name = 'deluxe/delete_education.html'
    context_object_name = 'education'
    success_url = '/#education'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'delete Education'
        return data

class EducationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Education
    fields = ['start_year','end_year','dgree_name','about','dgree_document']
    template_name = 'deluxe/update_education.html'
    success_url = '/#education'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Update Education'
        return data

class EducationDetailView(LoginRequiredMixin, DetailView):
    model = Education
    template_name = 'deluxe/education_detail.html'
    context_object_name = 'education'

# Project

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['project_name','contribution','about_project','github_project_link','main_thumbnial','thumbnial_1','thumbnial_2','thumbnial_3']
    template_name = 'deluxe/add_project.html'
    success_url = '/#project'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add Project'
        return data

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'deluxe/project_detail.html'
    context_object_name = 'project'

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'deluxe/delete_project.html'
    context_object_name = 'project'
    success_url = '/#project'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'delete Project'
        return data

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['project_name','contribution','about_project','github_project_link','main_thumbnial','thumbnial_1','thumbnial_2','thumbnial_3']
    template_name = 'deluxe/update_project.html'
    success_url = '/#project'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Update Project'
        return data


# Hobby

class HobbyCreateView(LoginRequiredMixin, CreateView):
    model = Hobby
    fields = ['hobby','about_hobby']
    template_name = 'deluxe/add_hobby.html'
    success_url = '/#hobbies'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add hobby'
        return data

class HobbyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Hobby
    template_name = 'deluxe/delete_hobby.html'
    context_object_name = 'hobby'
    success_url = '/#hobbies'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Delete Hobby'
        return data

# BLog like & dislike

def like(request, pk):
    blog = Blog.objects.get(pk=pk)
    BlogLike.objects.create(blog=blog, liked_by=request.user)
    return redirect('blog_list')

def unlike(request, pk):
    blog = Blog.objects.get(pk=pk)
    BlogLike.objects.filter(blog=blog, liked_by=request.user).delete()
    return redirect('blog_list')

# Search user

class ProfileListView(LoginRequiredMixin,ListView):
    model = Profile
    template_name = 'deluxe/profile_search.html'
    context_object_name = 'project_obj'

    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        
        value = Profile.objects.filter(
            Q(name__icontains=si) | 
            Q(phone_no__icontains=si) | 
            Q(field__icontains=si) | 
            Q(location__icontains=si) | 
            Q(user__username__icontains=si) | 
            Q(user__email__icontains=si)).order_by("-id")

        return value


# Follow 

class FollowsListView(ListView):
    model = Follow
    template_name = 'deluxe/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'follows'
        return data

class FollowersListView(ListView):
    model = Follow
    template_name = 'deluxe/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(follow_user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'followers'
        return data
