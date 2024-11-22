from django.db import models

class Teacher(models.Model):
    firstname = models.TextField()
    lastname = models.TextField()
    email = models.TextField()

class Student(models.Model):
    firstname = models.TextField()
    lastname = models.TextField()
    email = models.TextField()
    classroom = models.ForeignKey("Classroom", on_delete=models.SET_NULL, null=True)

class Classroom(models.Model):
    name = models.TextField()
    teacher = models.ForeignKey("Teacher", on_delete=models.SET_NULL, null=True)

class Assignment(models.Model):
    title = models.TextField()
    description = models.TextField()
    classroom = models.ForeignKey("Classroom", on_delete=models.CASCADE)

class Score(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    assignment = models.ForeignKey("Assignment", on_delete=models.CASCADE)
    score = models.FloatField()

