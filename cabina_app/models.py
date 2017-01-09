# encoding: utf-8
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=250, blank=False)
    password = models.CharField(max_length=250, blank=True)
    email = models.EmailField(blank=True)
    genre = models.CharField(max_length=6, blank=False)
    autonomous_community = models.CharField(max_length=250, blank=False)
    age = models.IntegerField(blank=False)

    def __unicode__(self):
        return self.username + " " + self.email


class Vote(models.Model):
    token = models.IntegerField(blank=False)
    idPregunta = models.IntegerField(blank=False)
    voto = models.CharField(max_length=1000,blank=False)

    def __unicode__(self):
        return str(self.token) + ", " + str(self.idPregunta) + ", " + str(self.voto)


class Poll(models.Model):
    id = models.IntegerField(blank=False, primary_key=True)
    title = models.CharField(max_length=250, blank=False)
    description = models.CharField(max_length=250, blank=False)
    startDate = models.DateField()
    endDate = models.DateField()

    def __unicode__(self):
        return str(self.id) + " " + str(self.title)


class Question(models.Model):
    question_id = models.IntegerField(blank=False, primary_key= True)
    text = models.CharField(max_length=250, blank=False)
    poll_reference = models.ForeignKey(Poll, blank=False)

    def __unicode__(self):
        return str(self.question_id) + " " + str(self.text) + " " + str(self.questions)

class Answer(models.Model):
    answer_id = models.IntegerField(blank=False, primary_key= True)
    text = models.CharField(max_length=250, blank=False)
    question_reference = models.ForeignKey(Question, blank =False)