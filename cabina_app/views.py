# encoding: utf-8
from rest_framework.decorators import api_view
from cabina_app.services import *
from django.shortcuts import render
from cabina_app.dbConnect import *


@api_view(['GET'])
def recibe_id_votacion(request, id_poll = None):
        informacion = None
        if(id_poll is None):
            informacion = "Error: No se ha recibido ninguna votacion"
            return render(request, "informacion.html", {'informacion': informacion, 'error': True})
        # Comprobar que el identificador de la votacion es numerico
        try:
            id_poll = int(id_poll)
        except ValueError:
            informacion = "El identificador de la votación es erronea"
            return render(request, "informacion.html", {'informacion': informacion, 'error': True})
        '''
        # Comprobar que dicho usuario autenticado es valido
        if not verify_user(request):
            informacion = "El usuario es erroneo, autenticate de nuevo"
        # Comprobar que el usuario autenticado puede votar en dicha votacion
        elif not can_vote(request, id_poll):
            informacion = "Usted no puede votar en esta votación"
        else:'''
            # Construir la votacion
        poll = get_poll(id_poll)
        if poll is None:
            informacion = "El identificador de la votación es erronea"

        if informacion is None:
            respuesta = render(request, "index.html", {'poll': poll, 'questions': poll.question_set.all()})
        else:
            respuesta =  render(request, "informacion.html", {'informacion': informacion, 'error': True})
        return respuesta

'Simula la renderización de index mediante un poll que viene de base de datos'
'actualmente, dado que Poll no tiene atributo questions y que éste está en Question, lo que se recupera es una pregunta de la Poll'
'This is for developers tests purposes only'
@api_view(['GET'])
def recibe_id_votacion_fromdb(request, id_question):
    #question = get_Question(id_question)
    poll = get_Poll(id_question)
    return render(request, "index.html", {'poll': poll, 'questions': poll.question_set.all()})



@api_view(['POST'])
def cabinarecepcion(request):

    error = True

    if request.method == 'POST':

        post_data = request.POST

        # Comprobar que el identificador de la votacion es numerico
        try:
            id_poll = int(post_data['id_poll'])
        except ValueError:
            informacion = "El identificador de la votación es erronea"
            return render(request, "informacion.html", {'informacion': informacion, 'error': error})

        #Construir votación y usuario
        poll = get_poll(id_poll)
        user = get_user(request)

        # Comprobar que dicho usuario autenticado es valido
        if not verify_user(request):
            informacion = "El usuario es erroneo, autenticate de nuevo"
        # Comprobar que el usuario autenticado puede votar en dicha votacion
        elif not can_vote(request, id_poll):
            informacion = "Usted no puede votar en esta votación"
        # Comprobar la votacion
        elif poll is None:
            informacion = "El identificador de la votación es erronea"
        # Comprobar el usuario
        elif user is None:
            informacion = "El usuario es erroneo"
        # Construir voto
        else:
            vote = get_vote(poll, user, post_data)

            # Cifrar el voto
            encryption_vote = get_encryption_vote(vote)
            if encryption_vote is False:
                informacion = "La contraseña proporcionada es demasiada corta como para cifrar dicho voto. Usted no podrá " \
                            "votar en esta votación hasta que se arregle dicho fallo.\n\nPongase en contacto con " \
                            "verificación."

            # Actualizar el estado de la votacion del usuario
            elif not update_user(request, poll.id):
                informacion = "No se ha podido actualizar el estado de la votación del usuario"
            else:
                # Almacenar el voto
                if not save_vote(encryption_vote, poll.id):
                    informacion = "No se ha podido almacenar el voto"
                else:
                    error = False
                    informacion = "Votacion guardada con éxito"
    else:
        informacion = "Lo sentimos, el metodo solicitado no esta disponible"

    return render(request, "informacion.html", {'informacion': informacion, 'error': error})
