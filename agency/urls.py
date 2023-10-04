from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from agency.views import (
    NewspaperListView,
    TopicListView,
    topic_newspapers,
    NewspaperDetailView,
    RedactorListView,
    redactor_newspapers,
    NewspaperCreateView,
    NewspaperUpdateView,
    NewspaperDeleteView,
    register,
    RedactorUpdateView,
    TopicCreateView,
)


urlpatterns = [
    path("registration/", register, name="register"),
    path("", NewspaperListView.as_view(), name="index"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("topics/<int:pk>/", topic_newspapers, name="topic-newspapers"),
    path(
        "newspaper/<int:pk>/",
        NewspaperDetailView.as_view(),
        name="newspaper-detail",
    ),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path(
        "redactors/<int:pk>/", redactor_newspapers, name="redactor-newspapers"
    ),
    path(
        "newspaper/create/",
        NewspaperCreateView.as_view(),
        name="newspaper-create",
    ),
    path(
        "newspaper/<int:pk>/update/",
        NewspaperUpdateView.as_view(),
        name="newspaper-update",
    ),
    path(
        "newspaper/<int:pk>/delete/",
        NewspaperDeleteView.as_view(),
        name="newspaper-delete",
    ),
    path(
        "redactors/<int:pk>/update/",
        RedactorUpdateView.as_view(),
        name="redactor-update",
    ),
    path(
        "redactors/<int:pk>/delete/",
        RedactorUpdateView.as_view(),
        name="redactor-delete",
    ),
    path("topics/create/", TopicCreateView.as_view(), name="topic-create"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name = "agency"
