from django.urls import path, include
from rest_framework.routers import DefaultRouter
from teachers import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'teachers', views.TeacherViewSet)
# router.register(r'subjects', views.SubjectViewSet)
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path(r'home', views.home_page, name="home"),
    path(r'teacher/<str:email>', views.teacher_profile, name="teacher_profile"),
    path(r'import', views.load_importer, name="load_importer"),
    path(r'import/process', views.process_import, name="process_import")
]
