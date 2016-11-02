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
    id = models.IntegerField(blank=False, primary_key=True)
    id_poll = models.IntegerField(blank=False)
    age = models.IntegerField(blank=False)
    genre = models.CharField(max_length=6, blank=False)
    autonomous_community = models.CharField(max_length=250, blank=False)
    answers = models.TextField(blank=False)

    def __unicode__(self):
        return str(self.id) + " " + str(self.id_poll) + str(
            self.age) + " " + self.genre + " " + self.autonomous_community + " " + self.answers


class Poll(models.Model):
    id = models.IntegerField(blank=False, primary_key=True)
    title = models.CharField(max_length=250, blank=False)
    description = models.CharField(max_length=250, blank=False)
    startDate = models.DateField()
    endDate = models.DateField()

    def __unicode__(self):
        return str(self.id) + " " + str(self.title)


class Question(models.Model):
    id = models.IntegerField(blank=False, primary_key=True)
    text = models.CharField(max_length=250, blank=False)
    questions = models.ForeignKey(Poll, blank=False)

    def __unicode__(self):
        return str(self.id) + " " + str(self.text) + " " + str(self.questions)