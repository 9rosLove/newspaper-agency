from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from agency.forms import NewspaperForm, NewspaperSearchForm, TopicSearchForm, RedactorSearchForm
from agency.models import Newspaper, Topic, Redactor


class NewspaperListView(generic.ListView):
    model = Newspaper
    template_name = 'agency/index.html'
    paginate_by = 10
    queryset = Newspaper.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = NewspaperSearchForm(initial={"title": title})
        return context

    def get_queryset(self):
        form = NewspaperSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                title__istartswith=form.cleaned_data["title"]
            )
        return self.queryset


class TopicListView(generic.ListView):
    model = Topic
    queryset = Topic.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TopicSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = TopicSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__istartswith=form.cleaned_data["name"]
            )
        return self.queryset


def topic_newspapers(request: HttpRequest, pk) -> HttpResponse:
    newspaper_list = Newspaper.objects.filter(topic_id=pk)
    form = NewspaperSearchForm(request.GET)
    if form.is_valid():
        search_query = form.cleaned_data.get('title')
        if search_query:
            newspaper_list = newspaper_list.filter(title__icontains=search_query)
    context = {'newspaper_list': newspaper_list, 'search_form': form}
    return render(
        request,
        'agency/topic-newspapers.html',
        context
    )


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class RedactorListView(generic.ListView):
    model = Redactor
    queryset = Redactor.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorSearchForm(initial={"username": username})
        return context

    def get_queryset(self):
        form = RedactorSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                username__istartswith=form.cleaned_data["username"]
            )
        return self.queryset


def redactor_newspapers(request: HttpRequest, pk) -> HttpResponse:
    redactor = get_user_model().objects.get(pk=pk)
    newspaper_list = Newspaper.objects.filter(publishers=redactor)
    form = NewspaperSearchForm(request.GET)
    if form.is_valid():
        search_query = form.cleaned_data.get('title')
        if search_query:
            newspaper_list = newspaper_list.filter(title__icontains=search_query)
    context = {'newspaper_list': newspaper_list, 'search_form': form}
    return render(
        request,
        'agency/redactor-newspapers.html',
        context
    )


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    success_url = reverse_lazy('agency:index')
    form_class = NewspaperForm


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    success_url = reverse_lazy('agency:index')
    form_class = NewspaperForm


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy('agency:index')
