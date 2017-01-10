# encoding: utf-8
from base64 import b64decode
import json
import urllib
import urllib2
from Crypto.PublicKey.RSA import importKey

import subprocess
import requests
import rsa

from cabina_app.models import User, Poll, Vote, Question, Answer


def verify_user(token):
    try:
        x = token.split(":")
        r = requests.get("https://authb.agoraus1.egc.duckdns.org/api/index.php?method=checkTokenUser&user="+ str(x[0]) +"&token="+ str(token))
        json_autenticacion = r.json()
        result = False
        if json_autenticacion['valid'] is True:
            result = True
    except ValueError:
        result = False
    print result
    return result


def can_vote(token):
    try:
        x = token.split(":")
        r = requests.get("https://censos.agoraus1.egc.duckdns.org/census/canVote.do?idVotacion="+ str(token)+" &username= "+ str(x[0]))
        json_censo = r.json()
        result = False
        if json_censo['result'] == "si":
            result = True
    except ValueError:
        result = False
    return result

def save_vote(encryption_votes):
    for vote in encryption_votes:
        payload = {'token': vote.token, 'idPregunta': vote.idPregunta, 'voto': vote.voto}
        print payload
        try:
            r = requests.post("https://beta.recuento.agoraus1.egc.duckdns.org/api/emitirVoto", data=payload)
            print r
            result = True
        except:
            result = False
    return 0


def get_poll(id_poll):
    try:
        r = requests.get('https://recuento.agoraus1.egc.duckdns.org/api/verVotacion?idVotacion='+ str(id_poll)+'&detallado=si' )
        
        json_poll = json.dumps(r.json())
        #poll = json.loads(json_poll, object_hook=json_as_poll)
        poll = json_as_poll(json_poll)
    except ValueError:
        poll = None
    return poll


def get_user(token):
    try:
        x = token.split(":")
        r = requests.get("https://authb.agoraus1.egc.duckdns.org/auth/api/getUser?method=getUser&user="+ str(x[0]))
        json_auth = json.dumps(r.json())
        user = json.json_as_user(json_auth)
    except ValueError:
        user = None
    return user


def get_vote(token, post_data):
    votes = []
    public_key = get_key_rsa()
    for question in post_data:
        if question!="id_poll":

            vote = Vote()
            vote.idPregunta = question.replace('group_','')
            vote.token = token


            try:
                if public_key is not None:
                    encrypt_vote = encrypt_rsa(post_data[question], public_key)
                else:
                    encrypt_vote = None
            except OverflowError:
                encrypt_vote = False
                votes = None

            vote.voto = encrypt_vote

            votes.append(vote)
    return votes


def update_user(token, id_poll):
    try:
        x = token.split(":")
        print "hola"

        r = requests.get("https://censos.agoraus1.egc.duckdns.org/census/updateUser.do?idVotacion="+ str(id_poll)+" &tipoVotacion=abierto&username= "+ str(x[0]))
        print r.json()

        json_censo = r.json()
        result = False
        if json_censo['result'] == "si":
            result = True
    except ValueError:
        result = False
    return result


def json_as_poll(json_poll):
    poll = Poll()
    x = json.loads(json_poll)

    poll.id = x['votacion']['id_votacion']
    poll.title = x['votacion']['titulo']
    poll.endDate = x['votacion']['fecha_cierre'][0:10]
    poll.startDate = x['votacion']['fecha_creacion'][0:10]
    poll.description = x['votacion']['titulo']


    for pregunta in x['votacion']['preguntas']:
        question = Question()
        question.question_id = pregunta['id_pregunta']
        question.text = pregunta['texto_pregunta']
        question.poll_reference = poll

        for opcion in pregunta['opciones']:
            answer = Answer()
            answer.answer_id = opcion['id_opcion']
            answer.text = opcion['texto_opcion']
            answer.question_reference = question

            question.answer_set.add(answer)


        poll.question_set.add(question)

    poll.save()

    return poll


def json_as_user(json_auth):
    user = User()
    x = json.loads(json_auth)

    user.username = x['username']
    user.genre= x['genre']
    user.autonomous_community= x['autonomous_community']
    user.email= x['email']
    user.age= x['age']
    return user


def vote_as_json(vote):
    to_dump_vote = {
        'id': vote.id,
        'id_poll': vote.id_poll,
        'age': vote.age,
        'genre': vote.genre,
        'autonomous_community': vote.autonomous_community,
        'answers': vote.answers
    }
    return json.dumps(to_dump_vote)


def encrypt_rsa(message, public_key_loc):
    # cifra el mensaje y lo codifica a base64
    cryptos = subprocess.check_output(['java', '-jar', 'cabina_app/verification.jar', 'cipher', '%s' % message, '%s' % public_key_loc])
    crypto = cryptos.encode("base64")
    return crypto


def decrypt_rsa(crypto, private_key):
    key_decode = b64decode(private_key)
    key_perfect = importKey(key_decode, passphrase=None)
    crypto = crypto.decode("base64")
    return subprocess.check_output(['java', '-jar', 'cabina_app/verification.jar', 'decipher', '%s' % crypto, '%s' % key_perfect])


def get_key_rsa():
    url = 'https://recuento.agoraus1.egc.duckdns.org/api/clavePublica'
    public_key = requests.get(url).text
    return public_key

