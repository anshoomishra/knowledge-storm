import json
from datetime import timedelta
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from exam.models import TestAttempt, QuestionAttempt

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.attempt_id = self.scope['url_route']['kwargs']['attempt_id']
        self.room_group_name = f'test_{self.attempt_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        question_time_spent = data.get('question_time_spent')
        remaining_time_seconds = data.get('remaining_time')

        remaining_time_timedelta = timedelta(seconds=remaining_time_seconds)
        time_spent_timedelta = timedelta(seconds=question_time_spent)

        await self.update_test_attempt(remaining_time_timedelta)

        # Update QuestionAttempt asynchronously
        await self.update_question_attempt(time_spent_timedelta)

        # Send message to room group
        print(remaining_time_timedelta)
        print(time_spent_timedelta)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'update_time',
                'time_spent': question_time_spent,
                'remaining_time': remaining_time_seconds
            }
        )

    async def update_test_attempt(self, remaining_time_timedelta):
        test_attempt = await self.get_test_attempt()
        if test_attempt:
            test_attempt.remained_time = remaining_time_timedelta
            await sync_to_async(test_attempt.save)()

    async def update_question_attempt(self, time_spent_timedelta):
        question_attempt = await self.get_question_attempt()

        if question_attempt:
            print(f"Existing time_spent: {question_attempt.time_spent}")
            question_attempt.time_spent += time_spent_timedelta
            print(f"Updated time_spent: {question_attempt.time_spent}")
            await sync_to_async(question_attempt.save)()
            print("QuestionAttempt saved successfully.")

    async def get_test_attempt(self):
        attempt_id = self.attempt_id
        return await sync_to_async(TestAttempt.objects.filter(id=attempt_id).first)()

    async def get_question_attempt(self):
        attempt_id = self.attempt_id
        return await sync_to_async(QuestionAttempt.objects.filter(test_attempt__id=attempt_id).first)()

    async def update_time(self, event):
        time_spent = event['time_spent']
        remaining_time = event['remaining_time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'time_spent': time_spent,
            'remaining_time': remaining_time
        }))
