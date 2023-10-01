from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from agency.forms import NewspaperForm
from agency.models import Newspaper, Topic, Redactor


class NewspaperListView(generic.ListView):
    model = Newspaper
    template_name = 'agency/index.html'


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
    redactor = get_user_model().objects.get(pk=pk)
    newspaper_list = Newspaper.objects.filter(publishers=redactor)
    return render(request,
                  'agency/redactor-newspapers.html',
                  {'newspaper_list': newspaper_list}
                  )


class NewspaperCreateView(generic.CreateView):
    model = Newspaper
    success_url = reverse_lazy('agency:index')
    form_class = NewspaperForm


class NewspaperUpdateView(generic.UpdateView):
    model = Newspaper
    success_url = reverse_lazy('agency:index')
    form_class = NewspaperForm


