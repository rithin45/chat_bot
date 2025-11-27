from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('login',views.login),
    path('about',views.about),
    path('admin_home',views.admin_home),
    path('therapist_home',views.therapist_home),
    path('therapist_register',views.therapist_register),
    path('admin_therapistpending',views.admin_therapistpending),
    path('admin_therapistaccept/<id2>',views.admin_therapistaccept),
    path('admin_therapistblock/<id2>',views.admin_therapistblock),
    path('admin_therapist',views.admin_therapist),
    path('user_register',views.user_register),
    path('user_home',views.user_home),
    path('admin_userview',views.admin_userview),
    path('admin_feedback',views.admin_feedback),
    path('admin_viewratings',views.admin_viewratings),
    path('admin_passwordchange',views.admin_passwordchange),
    path('therapist_schedule',views.therapist_schedule),
    path('therapist_scheduledelete/<id2>',views.therapist_scheduledelete),
    path('therapist_scheduleupdate/<id1>',views.therapist_scheduleupdate),
    path('therapist_changepasswrd',views.therapist_changepasswrd),
    path('therapist_motivationalvdo',views.therapist_motivationalvdo),
    path('admin_questionmanage',views.admin_questionmanage),
    path('admin_answermanage/<id1>',views.admin_answermanage),
    path('admin_questionmanagedelete/<id2>',views.admin_questionmanagedelete),
    path('admin_questionmanageupdate/<id1>',views.admin_questionmanageupdate),
    path('user_quiz',views.user_quiz),
    path('therapist_motivationalvdodelete/<id2>',views.therapist_motivationalvdodelete),
    path('user_bookshedule',views.user_bookshedule),
    path('user_bookings/<id2>', views.user_bookings),
    path('user_viewbookings',views.user_viewbookings),
    path('user_viewmotivationalvdo',views.user_viewmotivationalvdo),
    path('user_sentfeedback',views.user_sentfeedback),
    path('user_sentfeedbackdelete/<id2>',views.user_sentfeedbackdelete),
    path('user_changepasswrd',views.user_changepasswrd),
    path('therapist_viewbookings',views.therapist_viewbookings),
    path('therapist_viewbookingsconfirm/<id1>',views.therapist_viewbookingsconfirm),    
    path('therapist_viewusers',views.therapist_viewusers),
    path('view_therapists',views.view_therapists),
    path('therapist_view_rating',views.therapist_view_rating),
    path('user_chat/<id1>',views.user_chat),
    path('therapist_chat/<user_id>', views.therapist_chat, name='therapist_chat'),
    path('therapist_previousbookings',views.therapist_previousbookings),
    path('user_rate_therapist',views.user_rate_therapist),
    path('rate/<int:therapist_id>/', views.rate_therapist, name='rate_therapist'),
    
    
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chat/', views.chat, name='chat'),
    



]
