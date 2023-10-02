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
)


urlpatterns = [
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
]

app_name = "agency"
