from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import generic

from agency.models import Newspaper, Topic, Redactor


def index(request:HttpRequest) -> HttpResponse:
    newspaper_list = Newspaper.objects.select_related("topic")
    return render(request,
                  'agency/index.html',
                  {'newspaper_list': newspaper_list}
                  )


class TopicListView(generic.ListView):
    model = Topic


def topic_newspapers(request, pk) :
    newspaper_list = Newspaper.objects.filter(topic_id=pk)
    return render(request,
                  'agency/topic-newspapers.html',
                  {'newspaper_list': newspaper_list}
                  )


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class RedactorListView(generic.ListView):
    model = Redactor


def redactor_newspapers(request: HttpRequest, pk) -> HttpResponse:
    redactor = Redactor.objects.get(pk=pk)
    newspaper_list = Newspaper.objects.filter(publishers=redactor)
    return render(request,
                  'agency/redactor-newspapers.html',
                  {'newspaper_list': newspaper_list}
                  )
