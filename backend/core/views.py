from django.http import JsonResponse, Http404
from django.db.models import Count
from core.models import Conversation, AnalysisResult


def index(request):
    return JsonResponse({"message": "Welcome to the Voice Assistant API!"})


def total_conversations(request):
    total = AnalysisResult.objects.values("conversation_id").distinct().count()
    return JsonResponse({"total": total})


def emotion_summary(request):
    emotion_counts = (
        AnalysisResult.objects.values("emotion")
        .annotate(count=Count("emotion"))
        .order_by("-count")
    )
    return JsonResponse(list(emotion_counts), safe=False)


def emotion_table(request):
    results = AnalysisResult.objects.select_related("conversation").all()
    data = [
        {
            "conversation_id": r.conversation.id,
            "customer_name": r.conversation.customer_name,
            "emotion": r.emotion,
        }
        for r in results
    ]
    return JsonResponse(data, safe=False)


def compliance_scores(request):
    data = (
        AnalysisResult.objects.values("compliance_score")
        .annotate(count=Count("compliance_score"))
        .order_by("compliance_score")
    )
    return JsonResponse(list(data), safe=False)


def compliance_trend(request):
    results = AnalysisResult.objects.select_related("conversation").order_by(
        "conversation__id"
    )
    data = [
        {
            "conversation_id": result.conversation.id,
            "compliance_score": result.compliance_score,
        }
        for result in results
    ]
    return JsonResponse(data, safe=False)


def get_conversation(request, conversation_id):
    try:
        conversation = Conversation.objects.prefetch_related("messages").get(
            id=conversation_id
        )
    except Conversation.DoesNotExist:
        raise Http404("Conversation not found.")

    data = {
        "conversation_id": conversation.id,
        "messages": [
            {"sender": msg.sender, "text": msg.text}
            for msg in conversation.messages.all().order_by("id")
        ],
    }
    return JsonResponse(data)


def analysis_table(request):
    results = AnalysisResult.objects.select_related("conversation").all()
    data = [
        {
            "conversation_id": result.conversation.id,
            "customer_name": result.conversation.customer_name,
            "emotion_summary": result.emotion_summary,
            "compliance_summary": result.compliance_summary,
        }
        for result in results
    ]
    return JsonResponse(data, safe=False)
