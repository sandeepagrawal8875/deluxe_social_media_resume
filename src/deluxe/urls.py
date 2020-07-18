from django.urls import path
from deluxe.views import *
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('user/<str:username>', views.userPostListView, name='user_profile'),
    path('search_profile', ProfileListView.as_view(), name='search_profile'),
 

    path('blog/new/', BlogCreateView.as_view(), name='blog_create'),

    path('add_skills/', SkillsCreateView.as_view(), name='add_skills'),
    path('add_certificate/', CertificateCreateView.as_view(), name='add_certificate'),
    path('add_education/', EducationCreateView.as_view(), name='add_education'),
    path('add_hobby/', HobbyCreateView.as_view(), name='add_hobby'),
    path('add_project/', ProjectCreateView.as_view(), name='add_project'),


    path('hobby/<int:pk>/delete/', HobbyDeleteView.as_view(), name='hobby_delete'),


    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/<int:pk>/update/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/<int:pk>/detail/', BlogDetailView.as_view(), name='blog_detail'),


    path('blog/comment/<int:pk>/delete/', BlogCommentDeleteView.as_view(), name='comment_delete'),
    path('blog/comment/<int:pk>/update/', BlogCommentUpdateView.as_view(), name='comment_update'),

    path('blog/like/<int:pk>', views.like , name="blog_like"),
    path('blog/dislike/<int:pk>', views.unlike, name="blog_dislike"),


    path('skills/<int:pk>/delete/', SkillsDeleteView.as_view(), name='skills_delete'),
    path('skills/<int:pk>/update/', SkillsUpdateView.as_view(), name='skills_update'),

    path('education/<int:pk>/detail/', EducationDetailView.as_view(), name='education_detail'),
    path('education/<int:pk>/delete/', EducationDeleteView.as_view(), name='education_delete'),
    path('education/<int:pk>/update/', EducationUpdateView.as_view(), name='education_update'),


    path('project/<int:pk>/detail/', ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),

    
    path('certificate/<int:pk>/detail/', CertificateDetailView.as_view(), name='certificate_detail'),
    path('certificate/<int:pk>/delete/', CertificateDeleteView.as_view(), name='certificate_delete'),
    path('certificate/<int:pk>/update/', CertificateUpdateView.as_view(), name='certificate_update'),

    
    path('user/<str:username>/follows', FollowsListView.as_view(), name='follows'),
    path('user/<str:username>/followers', FollowersListView.as_view(), name='followers'),


]
