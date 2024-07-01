from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import TestSeries, Test, Subscription, TestType, TestAttempt, QuestionAttempt, Question
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
        tests = self.object.tests.all()
        test_attempts = {
            test.id: test.test_attempts.filter(user=self.request.user).first()
            for test in tests
        }
        context['tests'] = tests
        context['test_attempts'] = test_attempts
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
class StartTestView(View):
    def get(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        test_attempt = TestAttempt.objects.create(user=request.user, test=test)
        first_question = test.questions.first()
        return redirect('take_test', test_attempt.id, first_question.id)


class TakeTestView(View):
    def get(self, request, test_id, question_id):
        test = get_object_or_404(Test, id=test_id)

        # Fetch the test attempts for the user and the test
        test_attempts = TestAttempt.objects.filter(test=test, user=request.user)

        if test_attempts.exists():
            # If multiple attempts exist, get the first incomplete one or the latest one
            test_attempt = test_attempts.filter(is_completed=False).first() or test_attempts.latest('created_at')
        else:
            # Create a new test attempt if none exists
            test_attempt = TestAttempt.objects.create(
                test=test,
                user=request.user,
                current_question=test.questions.first()
            )

        if test_attempt.is_completed:
            return HttpResponseForbidden("You have already completed this test.")

        if not test_attempt.current_question:
            first_question = test_attempt.test.questions.first()
            test_attempt.current_question = first_question
            test_attempt.save()

        context = {
            'test_attempt': test_attempt,
            'question': test_attempt.current_question,
        }
        return render(request, 'exam/take_test.html', context)

    def post(self, request, test_id, question_id):
        # Fetch the test attempts for the user and the test
        test_attempts = TestAttempt.objects.filter(test_id=test_id, user=request.user)

        if test_attempts.exists():
            # If multiple attempts exist, get the first incomplete one or the latest one
            test_attempt = test_attempts.filter(is_completed=False).first() or test_attempts.latest('created_at')
        else:
            return HttpResponseForbidden("Test attempt not found.")

        if test_attempt.is_completed:
            return HttpResponseForbidden("You have already completed this test.")

        question = test_attempt.current_question
        answer_id = request.POST.get('answer')
        time_spent = int(request.POST.get('time_spent', 0))

        QuestionAttempt.objects.create(
            test_attempt=test_attempt,
            question=question,
            answer_id=answer_id,
            time_spent=timezone.timedelta(seconds=time_spent),
            answered_at=timezone.now(),
        )

        next_question = test_attempt.test.questions.filter(id__gt=question.id).first()
        if next_question:
            test_attempt.current_question = next_question
            test_attempt.save()
            return redirect('take_test', test_attempt.test.id, next_question.id)
        else:
            test_attempt.completed_at = timezone.now()
            test_attempt.is_active = False
            test_attempt.is_completed = True
            test_attempt.save()
            return redirect('test_complete', test_attempt.id)


class ResumeTestView(View):
    def get(self, request, attempt_id):
        test_attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
        if test_attempt.is_completed:
            return HttpResponseForbidden("You have already completed this test.")

        if test_attempt.paused_at:
            pause_duration = timezone.now() - test_attempt.paused_at
            test_attempt.time_spent += pause_duration
            test_attempt.paused_at = None
            test_attempt.save()

        return redirect('take_test', test_attempt.id)

class TestCompleteView(View):
    def get(self, request, attempt_id):
        test_attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
        return render(request, 'exam/test_complete.html', {'test_attempt': test_attempt})
class PauseTestView(View):
    def post(self, request, attempt_id):
        test_attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
        test_attempt.paused_at = timezone.now()
        test_attempt.save()
        return redirect('test_series_detail', test_attempt.test.test_series.id)