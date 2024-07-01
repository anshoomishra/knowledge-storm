from django.urls import path
from .views import (
    TestSeriesListView,
    TestSeriesDetailView,
    TestDetailView,
    SubscribeTestSeriesView,
    FreeTestListView,
    TestResultView,
)

urlpatterns = [
    path('test-series/', TestSeriesListView.as_view(), name='test_series_list'),
    path('test-series/<uuid:pk>/', TestSeriesDetailView.as_view(), name='test_series_detail'),
    path('test/<uuid:pk>/', TestDetailView.as_view(), name='test_detail'),
    path('subscribe/<uuid:pk>/', SubscribeTestSeriesView.as_view(), name='subscribe_test_series'),
    path('free-tests/', FreeTestListView.as_view(), name='free_test_list'),
    path('test-result/<uuid:pk>/', TestResultView.as_view(), name='test_result'),
]