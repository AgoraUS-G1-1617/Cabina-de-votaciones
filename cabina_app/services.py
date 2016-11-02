# encoding: utf-8
from base64 import b64decode
import json
import urllib
import urllib2
from Crypto.PublicKey.RSA import importKey

import requests
import rsa

from cabina_app.models import User, Poll, Vote


def verify_user(request):
    try:
        user = request.COOKIES.get('user')
        token = request.COOKIES.get('token')
        r = requests.get("http://localhost/auth/api/checkTokenUser?user=" + str(user) + "&token=" + str(token))
        json_autenticacion = r.json()
        result = False
        if json_autenticacion['valid'] is True:
            result = True
    except ValueError:
        result = False
    return result


def can_vote(request, id_poll):
    try:
        user = request.COOKIES.get('user')
        token = request.COOKIES.get('token')
        cookies = dict(user=user, token=token)
        r = requests.get("http://localhost:8080/ADMCensus/census/canVote.do?idVotacion=" + str(id_poll),
                         cookies=cookies)
        json_censo = r.json()
        result = False
        if json_censo['result'] == "yes":
            result = True
    except ValueError:
        result = False
    return result


def get_encryption_vote(vote):
    json_vote = vote_as_json(vote)
    json_string = str(json_vote)
    try:
        public_key = get_key_rsa(vote.id_poll)
        if public_key is not False:
            encrypt_vote = encrypt_rsa(json_string, public_key)
        else:
            encrypt_vote = False
    except OverflowError:
        encrypt_vote = False
    return encrypt_vote


def save_vote(encryption_vote, id_poll):
    data = [('vote', encryption_vote), ('votation_id', id_poll)]
    data = urllib.urlencode(data)
    path = 'http://php-egc.rhcloud.com/vote.php'
    req = urllib2.Request(path, data)
    response = urllib2.urlopen(req)
    response_data = json.load(response)
    result = False
    if response_data['msg'] == u'1':
        result = True
    return result


def get_poll(id_poll):
    try:
        r = requests.get('http://localhost:8080/CreacionAdminVotaciones/vote/survey.do?id=' + str(id_poll))
        json_poll = json.dumps(r.json())
        poll = json.loads(json_poll, object_hook=json_as_poll)
    except ValueError:
        poll = None
    return poll


def get_user(request):
    try:
        username = request.COOKIES.get('user')
        r = requests.get("http://localhost/auth/api/getUser?user=" + username)
        json_auth = json.dumps(r.json())
        user = json.loads(json_auth, object_hook=json_as_user)
    except ValueError:
        user = None
    return user


def get_vote(poll, user, post_data):
    answers = []
    for question in poll.questions:
        answer_question = post_data[str(question.id)]
        a = {"question": question.text, "answer_question": answer_question}
        answers.append(a)

    vote = Vote()
    vote.id = 1
    vote.id_poll = poll.id
    vote.age = user.age
    vote.genre = user.genre
    vote.autonomous_community = user.autonomous_community
    vote.answers = answers
    return vote


def update_user(request, id_poll):
    try:
        user = request.COOKIES.get('user')
        token = request.COOKIES.get('token')
        cookies = dict(user=user, token=token)
        r = requests.get("http://localhost:8080/ADMCensus/census/updateUser.do?idVotacion=" + str(id_poll),
                         cookies=cookies)
        json_censo = r.json()
        result = False
        if json_censo['result'] == "yes":
            result = True
    except ValueError:
        result = False
    return result


def json_as_poll(json_poll):
    poll = Poll()
    poll.__dict__.update(json_poll)
    return poll


def json_as_user(json_auth):
    user = User()
    user.__dict__.update(json_auth)
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
    key_decode = b64decode(public_key_loc)
    key_perfect = importKey(key_decode, passphrase=None)
    cryptos = rsa.encrypt(message, key_perfect)
    crypto = cryptos.encode("base64")
    return crypto


def decrypt_rsa(crypto, private_key):
    key_decode = b64decode(private_key)
    key_perfect = importKey(key_decode, passphrase=None)
    crypto = crypto.decode("base64")
    return rsa.decrypt(crypto, key_perfect)


def get_key_rsa(id_votacion):
    web = urllib2.urlopen("http://www.egcprueba.esy.es/getKeys.php?id=" + str(id_votacion))
    result = False
    try:
        keys = json.load(web)
        public = keys['Publickey']
        if public is not None and public is not "":
            result = public
        return result
    except ValueError:
        return False

