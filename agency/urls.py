from django.urls import path

from agency.views import (index,
                          TopicListView,
                          topic_newspapers,
                          NewspaperDetailView,
                          RedactorListView,
                          redactor_newspapers
                          )


urlpatterns = [
    path("", index, name='index'),
    path("topics/", TopicListView.as_view(), name='topic-list'),
    path("topics/<int:pk>/", topic_newspapers, name='topic-newspapers'),
    path("newspaper/<int:pk>/", NewspaperDetailView.as_view(), name='newspaper-detail'),
    path ("redactors/", RedactorListView.as_view(), name='redactor-list'),
    path("redactors/<int:pk>/", redactor_newspapers, name='redactor-newspapers'),
]

app_name = 'agency'
