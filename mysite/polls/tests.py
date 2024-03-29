import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    # create a question with the given text and published the given number of
    # days offset to now (negative for published questions)
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        # test if no questions exist, an appropriate message is displayed
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_questions'],[])

    def test_past_question(self):
        # test that questions with a past pub date are displayed on the Index
        # page
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
                ['<Question: Past question.>']
        )

    def test_future_question(self):
        # test that questions with a future pub date are not displayed on the
        # Index page
        create_question(question_text="Past question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_questions'],[])

    def test_future_question_and_past_question(self):
        # test that even if past and future questions exist, only past questions
        # are displayed
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    def test_two_past_questions(self):
        # the questions index page may display multiple questions.
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        respones = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions'],[])

    def test_future_and_past_question(self):



class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        # returns false for questions whose pub_date is in the future
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        # returns false for questions whose pub_date is older than one day
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        # returns true for questions whose pub_date is within the last day
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
            seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
