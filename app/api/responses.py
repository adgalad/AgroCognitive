from rest_framework.response import Response
from rest_framework import status

def BadUserAuthentication():
	msg = {'detail': 'El email o la contraseña son incorrectas.'}
	return Response(msg, status=status.HTTP_400_BAD_REQUEST)


class ImagesUpload:
    def success():
        msg = {'detail': 'Se subieron las imagenes exitosamente.'} 
        return Response(msg)

    def error(error):
        msg = {'detail': error} 
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)