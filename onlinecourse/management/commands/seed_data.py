from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from onlinecourse.models import Course, Lesson, Instructor, Learner, Question, Choice


class Command(BaseCommand):
    help = "Create a demo admin, learner, course, lessons and a mock exam."

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        learner_user, _ = User.objects.get_or_create(
            username='learner', defaults={'first_name': 'Demo', 'last_name': 'Learner'})
        learner_user.set_password('learner123')
        learner_user.save()
        Learner.objects.get_or_create(user=learner_user)

        instructor_user, _ = User.objects.get_or_create(username='instructor')
        instructor, _ = Instructor.objects.get_or_create(user=instructor_user, defaults={'total_learners': 100})

        course, created = Course.objects.get_or_create(
            name='Introduction to Cloud Computing',
            defaults={'description': 'Learn the fundamentals of cloud computing.',
                      'pub_date': '2026-01-01'})
        if not created:
            self.stdout.write("Demo data already present.")
            return
        course.instructors.add(instructor)

        lessons = [
            ('What is Cloud Computing?', 'Cloud computing delivers computing services over the internet.'),
            ('Service Models', 'IaaS, PaaS and SaaS are the three main service models.'),
            ('Deployment Models', 'Public, private and hybrid clouds.'),
        ]
        for i, (title, content) in enumerate(lessons):
            Lesson.objects.create(title=title, order=i, course=course, content=content)

        exam = [
            ('Which of these is a cloud service model?',
             [('IaaS', True), ('PaaS', True), ('SaaS', True), ('LaaS', False)]),
            ('Cloud computing delivers services over the internet.',
             [('True', True), ('False', False)]),
            ('Which is a deployment model?',
             [('Hybrid cloud', True), ('Local cloud', False), ('Offline cloud', False)]),
        ]
        for text, choices in exam:
            q = Question.objects.create(course=course, question_text=text, grade=1)
            for ctext, correct in choices:
                Choice.objects.create(question=q, choice_text=ctext, is_correct=correct)
        self.stdout.write(self.style.SUCCESS("Seeded demo data (admin/admin123, learner/learner123)."))
