from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from agency.forms import (
    NewspaperForm,
    NewspaperSearchForm,
    TopicSearchForm,
    RedactorSearchForm,
)
from agency.models import Newspaper, Topic, Redactor


class NewspaperListView(generic.ListView):
    model = Newspaper
    template_name = "agency/index.html"
    paginate_by = 6
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
    paginate_by = 6

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
    search_query = request.GET.get("title")
    topic = get_object_or_404(Topic, pk=pk)
    if search_query:
        newspaper_list = newspaper_list.filter(title__icontains=search_query)
    page_number = request.GET.get("page")
    paginator = Paginator(newspaper_list, 6)
    try:
        newspaper_list = paginator.page(page_number)
    except PageNotAnInteger:
        newspaper_list = paginator.page(1)
    except EmptyPage:
        newspaper_list = paginator.page(paginator.num_pages)
    context = {
        "newspaper_list": newspaper_list,
        "page_obj": newspaper_list,
        "is_paginated": newspaper_list.has_other_pages,
        "search_form": form,
        "topic": topic,
    }
    return render(request, "agency/redactor_newspapers.html", context)


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class RedactorListView(generic.ListView):
    model = Redactor
    queryset = Redactor.objects.all()
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        form = RedactorSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                username__istartswith=form.cleaned_data["username"]
            )
        return self.queryset


def redactor_newspapers(request: HttpRequest, pk) -> HttpResponse:
    redactor = get_object_or_404(Redactor, pk=pk)
    newspaper_list = Newspaper.objects.filter(publishers=redactor)
    form = NewspaperSearchForm(request.GET)
    search_query = request.GET.get("title")

    if search_query:
        newspaper_list = newspaper_list.filter(title__icontains=search_query)

    paginator = Paginator(newspaper_list, 6)
    page_number = request.GET.get("page")

    try:
        newspaper_list = paginator.page(page_number)
    except PageNotAnInteger:
        newspaper_list = paginator.page(1)
    except EmptyPage:
        newspaper_list = paginator.page(paginator.num_pages)

    context = {
        "newspaper_list": newspaper_list,
        "page_obj": newspaper_list,
        "is_paginated": newspaper_list.has_other_pages,
        "search_form": form,
        "redactor": redactor,
        "page_number": page_number,
    }
    return render(request, "agency/redactor_newspapers.html", context)


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    success_url = reverse_lazy("agency:index")
    form_class = NewspaperForm


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    success_url = reverse_lazy("agency:index")
    form_class = NewspaperForm


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("agency:index")
