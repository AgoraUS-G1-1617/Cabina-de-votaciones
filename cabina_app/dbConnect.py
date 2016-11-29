from cabina_app.models import User, Poll, Vote, Question
import traceback

def get_User(user_id):
    try:
        newUser = User.objects.get(id=user_id)
    except Exception as e:
        print "No se pudo extraer el usuario"
        raise

    return newUser

def get_Poll(poll_id):
    try:
        newPoll = Poll.objects.get(id=poll_id)
        print(newPoll.__unicode__())
    except Exception as e:
        print "No se pudo extraer la encuesta"
        raise

    return newPoll

def get_Question(question_id):
    try:
        newQuestion = Question.objects.get(id=question_id)
    except Exception as e:
        print "No se pudo extraer la encuesta por pregunta"
        traceback.print_exc()
        raise

    return newQuestion

def get_Vote(vote_id):
    try:
        newVote = Vote.objects.get(id=vote_id)
    except Exception as e:
        print "No se pudo extraer el voto"
        raise

    return newVote
