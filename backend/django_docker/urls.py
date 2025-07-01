"""
URL configuration for django_docker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from core.views import (
    index,
    get_conversation,
    total_conversations,
    emotion_summary,
    emotion_table,
    compliance_scores,
    compliance_trend,
    analysis_table,
)


urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
    path(
        "api/conversation/<int:conversation_id>/",
        get_conversation,
        name="get_conversation",
    ),
    path("api/stats/conversations/", total_conversations, name="total_conversations"),
    path("api/stats/emotions/", emotion_summary, name="emotion_summary"),
    path("api/stats/emotion-table/", emotion_table, name="emotion_table"),
    path(
        "api/stats/compliance-scores/",
        compliance_scores,
        name="compliance_scores",
    ),
    path("api/stats/compliance-trend/", compliance_trend, name="compliance_trend"),
    path("api/stats/analysis-table/", analysis_table, name="analysis-table"),
]
