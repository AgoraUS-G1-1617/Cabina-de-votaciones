# encoding: utf-8
from rest_framework.decorators import api_view
from cabina_app.services import *
from django.shortcuts import render


@api_view(['GET'])
def recibe_id_votacion(request, id_poll):
    # Comprobar que el identificador de la votacion es numerico
    try:
        id_poll = int(id_poll)
    except ValueError:
        informacion = "El identificador de la votación es erronea"
        return render(request, "informacion.html", {'informacion': informacion, 'error': True})

    # Comprobar que dicho usuario autenticado es valido
    if not verify_user(request):
        informacion = "El usuario es erroneo, autenticate de nuevo"
        return render(request, "informacion.html", {'informacion': informacion, 'error': True})

    # Comprobar que el usuario autenticado puede votar en dicha votacion
    if not can_vote(request, id_poll):
        informacion = "Usted no puede votar en esta votación"
        return render(request, "informacion.html", {'informacion': informacion, 'error': True})

    # Construir la votacion
    poll = get_poll(id_poll)
    if poll is None:
        informacion = "El identificador de la votación es erronea"
        return render(request, "informacion.html", {'informacion': informacion, 'error': True})

    return render(request, "index.html", {'poll': poll, 'questions': poll.questions})


@api_view(['POST'])
def cabinarecepcion(request):
    if request.method == 'POST':

        post_data = request.POST

        # Comprobar que el identificador de la votacion es numerico
        try:
            id_poll = int(post_data['id_poll'])
        except ValueError:
            informacion = "El identificador de la votación es erronea"
            return render(request, "informacion.html", {'informacion': informacion, 'error': True})

        # Comprobar que dicho usuario autenticado es valido
        if not verify_user(request):
            informacion = "El usuario es erroneo, autenticate de nuevo"
            return render(request, "informacion.html", {'informacion': informacion, 'error': True})

        # Comprobar que el usuario autenticado puede votar en dicha votacion
        if not can_vote(request, id_poll):
            informacion = "Usted no puede votar en esta votación"
            return render(request, "informacion.html", {'informacion': informacion, 'error': True})

        # Construir la votacion
        poll = get_poll(id_poll)
        if poll is None:
            informacion = "El identificador de la votación es erronea"
            return render(request, "informacion.html", {'informacion': informacion, 'error': True})

        # Construir el usuario
        user = get_user(request)
        if user is None:
            informacion = "El usuario es erroneo"
            return render(request, "informacion.html", {'informacion': informacion, 'error': True})

        # Construir voto
        vote = get_vote(poll, user, post_data)

        # Cifrar el voto
        encryption_vote = get_encryption_vote(vote)
        if encryption_vote is False:
            informacion = "La contraseña proporcionada es demasiada corta como para cifrar dicho voto. Usted no podrá " \
                          "votar en esta votación hasta que se arregle dicho fallo.\n\nPongase en contacto con " \
                          "verificación."
            return render(request, "informacion.html", {'informacion': informacion, 'error': True})

        # Actualizar el estado de la votacion del usuario
        if not update_user(request, poll.id):
            informacion = "No se ha podido actualizar el estado de la votación del usuario"
            return render(request, "informacion.html", {'informacion': informacion, 'error': True})
        else:
            # Almacenar el voto
            if not save_vote(encryption_vote, poll.id):
                informacion = "No se ha podido almacenar el voto"
                return render(request, "informacion.html", {'informacion': informacion, 'error': True})

        informacion = "Votacion guardada con éxito"
        return render(request, "informacion.html", {'informacion': informacion, 'error': False})
    else:
        informacion = "Lo sentimos, el metodo solicitado no esta disponible"
        return render(request, "informacion.html", {'informacion': informacion, 'error': True})