from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import TestSeries, Test, Subscription, TestType
from django.http import HttpResponseForbidden

class TestSeriesListView(ListView):
    model = TestSeries
    template_name = 'exam/test_series_list.html'
    context_object_name = 'test_series_list'

class TestSeriesDetailView(DetailView):
    model = TestSeries
    template_name = 'exam/test_series_detail.html'
    context_object_name = 'test_series'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tests'] = Test.objects.filter(test_type__test_series=self.object)
        return context

class TestDetailView(DetailView):
    model = Test
    template_name = 'exam/test_detail.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.object.questions.all()
        return context

class SubscribeTestSeriesView(LoginRequiredMixin, CreateView):
    model = Subscription
    fields = []
    template_name = 'exam/subscribe_test_series.html'

    def get_success_url(self):
        return reverse_lazy('test_series_detail', kwargs={'pk': self.object.test_series.pk})

    def form_valid(self, form):
        user = self.request.user
        test_series = get_object_or_404(TestSeries, pk=self.kwargs['pk'])

        if Subscription.objects.filter(user=user, test_series=test_series).exists():
            return HttpResponseForbidden('You have already subscribed to this test series.')

        subscription = form.save(commit=False)
        subscription.user = user
        subscription.test_series = test_series
        subscription.expires_at = timezone.now() + timezone.timedelta(days=test_series.duration_of_subscription)
        subscription.save()
        return super().form_valid(form)

class FreeTestListView(ListView):
    model = Test
    template_name = 'exam/free_test_list.html'
    context_object_name = 'free_tests'

    def get_queryset(self):
        return Test.objects.filter(test_type__is_free_test=True)

class TestResultView(TemplateView):
    template_name = 'exam/test_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test = get_object_or_404(Test, pk=self.kwargs['pk'])
        # Add logic to retrieve and display test results
        context['test'] = test
        return context