from django.core.management.base import BaseCommand
from core.models import (
    Conversation,
    Message,
    AnalysisResult,
)
import json
from .run_gemini import detect_emotion_from_llm, detect_compliance_from_llm
import os


class Command(BaseCommand):
    help = "Load mock conversations into the database"

    def handle(self, *args, **kwargs):
        mock_conversations_json = os.path.join(
            os.path.dirname(__file__),
            "mock_conversations.json",
        )
        with open(mock_conversations_json, "r") as f:
            data = json.load(f)

        # print(data)
        for convo in data:
            conversation = Conversation.objects.create(
                customer_name=convo["customer_name"]
            )
            Message.objects.bulk_create(
                [
                    Message(
                        conversation=conversation,
                        sender=msg["sender"],
                        text=msg["text"],
                    )
                    for msg in convo["messages"]
                ]
            )

            emotion_summary, emotion = detect_emotion_from_llm(convo["messages"])
            # print(emotion_summary, emotion)

            compliance_summary, compliance_score = detect_compliance_from_llm(
                convo["messages"]
            )
            # print(compliance_summary, compliance_score)

            AnalysisResult.objects.create(
                conversation=conversation,
                emotion_summary=emotion_summary,
                emotion=emotion,
                compliance_summary=compliance_summary,
                compliance_score=compliance_score,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Conversation {conversation.id} loaded and classified as '{emotion}'."
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Conversation {conversation.id} compliance score is '{compliance_score}'."
                )
            )

        self.stdout.write(self.style.SUCCESS("Mock conversations loaded successfully."))
