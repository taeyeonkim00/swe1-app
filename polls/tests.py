from django.test import TestCase
from django.urls import reverse
from .models import Question
from django.utils import timezone


class QuestionModelTests(TestCase):
    def test_question_has_choices(self):
        """
        Test if a Question can have related Choices.
        """
        question = Question.objects.create(
            question_text="Sample Question", pub_date=timezone.now()
        )
        question.choice_set.create(choice_text="Choice 1", votes=0)
        question.choice_set.create(choice_text="Choice 2", votes=0)

        self.assertEqual(question.choice_set.count(), 2)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_questions_exist(self):
        """
        If questions exist, they are displayed on the index page.
        """
        question = Question.objects.create(
            question_text="Sample Question", pub_date=timezone.now()
        )
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])


class QuestionDetailViewTests(TestCase):
    def test_question_detail_view(self):
        """
        Test that the detail view correctly shows the question.
        """
        question = Question.objects.create(
            question_text="Sample Question", pub_date=timezone.now()
        )
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)


class VoteViewTests(TestCase):
    def setUp(self):
        """
        Set up a question and choices for vote testing.
        """
        self.question = Question.objects.create(
            question_text="Sample Question", pub_date=timezone.now()
        )
        self.choice1 = self.question.choice_set.create(choice_text="Choice 1", votes=0)
        self.choice2 = self.question.choice_set.create(choice_text="Choice 2", votes=0)

    def test_vote_valid_choice(self):
        """
        Test voting for a valid choice.
        """
        response = self.client.post(
            reverse("polls:vote", args=(self.question.id,)), {"choice": self.choice1.id}
        )
        self.choice1.refresh_from_db()
        self.assertEqual(self.choice1.votes, 1)
        self.assertRedirects(
            response, reverse("polls:results", args=(self.question.id,))
        )
