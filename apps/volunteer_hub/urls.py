from rest_framework.routers import DefaultRouter
from django.urls import path

from apps.volunteer_hub.views import VolunteerEnrollmentViewSet, VolunteerProjectViewSet, form_generator_page

router = DefaultRouter()
router.register("projects", VolunteerProjectViewSet, basename="volunteer-projects")
router.register("enrollments", VolunteerEnrollmentViewSet, basename="volunteer-enrollments")

urlpatterns = [
	path("form-generator/", form_generator_page, name="volunteer-form-generator"),
	*router.urls,
]
