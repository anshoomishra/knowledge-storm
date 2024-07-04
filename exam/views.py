import json
from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import TestSeries, Test, Subscription, TestType, TestAttempt, QuestionAttempt, Question
from django.http import HttpResponseForbidden, JsonResponse


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
        print("tests",tests)
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
        test_attempt.remained_time = test.duration
        test_attempt.save()
        first_question = test.questions.first()
        return redirect('take_test', test_attempt.id, first_question.id)


class TakeTestView(View):
    def get(self, request, attempt_id, question_id):
        test_attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
        if test_attempt.is_completed:
            return HttpResponseForbidden("You have already completed this test.")

        question = get_object_or_404(Question, id=question_id)
        test_attempt.current_question = question
        remained_time_seconds = int(test_attempt.remained_time.total_seconds())
        test_attempt.save()

        # Get the last QuestionAttempt if exists
        question_attempt = QuestionAttempt.objects.filter(test_attempt=test_attempt, question=question).last()
        question_time_spent = question_attempt.time_spent.total_seconds() if question_attempt else 0

        context = {
            'test_attempt': test_attempt,
            'question': question,
            'selected_answer_id': question_attempt.answer_id if question_attempt else None,
            'question_time_spent': question_time_spent,
            'remained_time_seconds':remained_time_seconds
        }
        return render(request, 'exam/take_test.html', context)

    def post(self, request, attempt_id, question_id):
        test_attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
        if test_attempt.is_completed:
            return HttpResponseForbidden("You have already completed this test.")

        question = get_object_or_404(Question, id=question_id)
        answer_id = request.POST.get('answer')

        time_spent = request.POST.get('time_spent', 0)
        time_spent_seconds = int(time_spent)
        # Update or create the QuestionAttempt
        question_attempt, created = QuestionAttempt.objects.update_or_create(
            test_attempt=test_attempt,
            question=question,
            defaults={
                'answer_id': answer_id,
                'time_spent': timezone.timedelta(seconds=time_spent_seconds),
                'answered_at': timezone.now()
            }
        )


        # Handle navigation to the next or previous question
        if 'next' in request.POST:
            next_question = test_attempt.test.questions.filter(id__gt=question.id).first()
            if next_question:
                test_attempt.current_question = next_question
                test_attempt.save()
                return redirect('take_test', attempt_id=test_attempt.id, question_id=next_question.id)
        elif 'previous' in request.POST:
            prev_question = test_attempt.test.questions.filter(id__lt=question.id).last()
            if prev_question:
                test_attempt.current_question = prev_question
                test_attempt.save()
                return redirect('take_test', attempt_id=test_attempt.id, question_id=prev_question.id)
        elif 'submit' in request.POST:
            test_attempt.is_completed = True
            test_attempt.end_time = timezone.now()
            test_attempt.save()
            return redirect('test_complete', attempt_id=test_attempt.id)
        elif 'pause' in request.POST:
            test_attempt.paused_at = timezone.now()
            test_attempt.save()
            return redirect('pause_test', attempt_id=test_attempt.id)

        return redirect('take_test', attempt_id=test_attempt.id, question_id=question.id)
class ResumeTestView(View):
    def get(self, request, attempt_id):
        test_attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
        if test_attempt.is_completed:
            return HttpResponseForbidden("You have already completed this test.")

        test_attempt.resume()
        return redirect('take_test', test_attempt.id, test_attempt.current_question.id)


class PauseTestView(View):
    def post(self, request, attempt_id):
        test_attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
        if test_attempt.is_completed:
            return HttpResponseForbidden("You have already completed this test.")

        test_attempt.pause()
        return redirect('test_series_detail', test_attempt.test.series.id)


class TestCompleteView(View):
    def get(self, request, attempt_id):
        test_attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
        if not test_attempt.is_completed:
            return HttpResponseForbidden("You have not completed this test.")

        context = {
            'test_attempt': test_attempt,
        }
        return render(request, 'exam/test_complete.html', context)

@csrf_exempt
def update_timer(request, attempt_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            test_attempt = TestAttempt.objects.get(id=attempt_id, user=request.user)
            test_attempt.time_spent += timezone.timedelta(seconds=data['time_spent'])
            test_attempt.remained_time = timezone.timedelta(seconds=data['remaining_time'])
            test_attempt.save()
            return JsonResponse({'status': 'success'})
        except TestAttempt.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'TestAttempt not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)