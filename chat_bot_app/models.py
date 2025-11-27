from django.db import models

# Create your models here.
# Login Model
class Login(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    usertype = models.CharField(max_length=200)

# Therapist Model
class Therapist(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

# User Model
class User(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

# Schedule Model
class Schedule(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    week = models.CharField(max_length=200)
    from_time = models.CharField(max_length=200)
    to_time = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

# Booking Model
class Booking(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

# Video Model
class Video(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video = models.FileField()

# Chat Model
class Chat(models.Model):
    sender_id = models.CharField(max_length=200)
    receiver_id = models.CharField(max_length=200)
    chat = models.CharField(max_length=200)
    reply = models.CharField(max_length=200)
    date = models.CharField(max_length=200)

# Question Model
class Question(models.Model):
    question = models.CharField(max_length=200)

# Answer Model
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

# Feedback Model
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=200)
    reply = models.CharField(max_length=200)
    date = models.CharField(max_length=200)

# Rating Model
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    rating = models.CharField(max_length=200)
    review = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
