from django.db import models


class Conversation(models.Model):
    customer_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.CharField(max_length=50)
    text = models.TextField()


class AnalysisResult(models.Model):
    conversation = models.OneToOneField(
        Conversation, on_delete=models.CASCADE, related_name="analysis"
    )
    emotion_summary = models.JSONField()
    compliance_summary = models.JSONField()
    emotion = models.CharField(max_length=10)
    compliance_score = models.IntegerField()
