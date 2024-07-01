from django.urls import path
from .views import (
    TestSeriesListView,
    TestSeriesDetailView,
    TestDetailView,
    SubscribeTestSeriesView,
    FreeTestListView,
    TestResultView, StartTestView, TakeTestView, ResumeTestView, TestCompleteView, PauseTestView
)

urlpatterns = [
    path('test-series/', TestSeriesListView.as_view(), name='test_series_list'),
    path('test-series/<uuid:pk>/', TestSeriesDetailView.as_view(), name='test_series_detail'),
    path('test/<uuid:pk>/', TestDetailView.as_view(), name='test_detail'),
    path('subscribe/<uuid:pk>/', SubscribeTestSeriesView.as_view(), name='subscribe_test_series'),
    path('free-tests/', FreeTestListView.as_view(), name='free_test_list'),
    path('test-result/<uuid:pk>/', TestResultView.as_view(), name='test_result'),
    path('start-test/<uuid:test_id>/', StartTestView.as_view(), name='start_test'),
    path('take-test/<uuid:attempt_id>/<uuid:question_id>/', TakeTestView.as_view(), name='take_test'),
    path('resume-test/<uuid:attempt_id>/', ResumeTestView.as_view(), name='resume_test'),
    path('test-complete/<uuid:attempt_id>/', TestCompleteView.as_view(), name='test_complete'),
    path('pause-test/<uuid:attempt_id>/', PauseTestView.as_view(), name='pause_test'),
]