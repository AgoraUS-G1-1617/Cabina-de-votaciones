from cabina_app.models import User, Poll, Vote, Question
from django.shortcuts import get_object_or_404
import traceback

def get_User(user_id):
    try:
        newUser = get_object_or_404(pk=user_id)
    except Exception as e:
        print "No se pudo extraer el usuario"
        raise

    return newUser

def get_Poll(poll_id):
    try:
        newPoll = get_object_or_404(Poll,pk=poll_id)
        print(newPoll.__unicode__())
    except Exception as e:
        print "No se pudo extraer la encuesta"
        raise

    return newPoll

def get_Question(question_id):
    try:

        newQuestion = get_object_or_404(pk=question_id)
    except Exception as e:
        print "No se pudo extraer la pregunta"
        traceback.print_exc()
        raise

    return newQuestion

def get_Vote(vote_id):
    try:
        newVote = get_object_or_404(pk=vote_id)
    except Exception as e:
        print "No se pudo extraer el voto"
        raise

    return newVote
