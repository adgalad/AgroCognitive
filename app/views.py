# from watson_developer_cloud import VisualRecognitionV3 as VisualRecognition
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib as plt
# from matplotlib.patches import Circle
# from django.shortcuts import render
# from app.forms import *
# from skimage import io
# import math
# import json
# import zipfile
# import sys
# import os
# import re
# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt


# from app.models import *
# from app.ibm_cloud import COSZipUploadHandler

# # Create your views here.

# # API Key del servicio de Visual Recognition en Bluemix
# API_KEY_VISUAL = '5b01d311b14fe61bb24b4d46aa61b868e52c23f0'

# # Lista con los ID de los modelos usados
# clasificadores = ['EstadoxCultivo_1555493827']

# # Creamos una instancia del servicio de Visual Recognition
# visual_recognition = VisualRecognition('2016-05-20',api_key=API_KEY_VISUAL)



# @csrf_exempt
# def signup(request):
#   if request.method == "POST":
#     data = json.loads(request.body)
#     form = SignUpForm(data)
#     if form.is_valid():
#       form.save()
#       return JsonResponse({'details': 'Usuario creado'})
#     else:
#       for i in form.errors:
#         print(i)
#   return HttpResponse(status=400)


#----------- Vista del home de AgroCognitive -------------#
def home(request):
  x = Nutrition.objects.all()
  print(x)
  if request.method == 'POST':
    form = iniciarSesionForm(request.POST)

    if form.is_valid():
      # Verifico si el usuario existe, esté activo o no
      user = authenticate(username = form.cleaned_data['identificacion'], password = form.cleaned_data['clave'])
      if user is not None:
        if (user.is_active):
          login(request, user)
        else:
          msg = "Su usuario se encuentra inactivo."
          return render(request, 'index.html', {'form': form, 'msg': msg})
      else:
        msg = "Usuario o contraseña incorrecta."
        return render(request, 'index.html', {'form': form, 'msg': msg})
    return render(request, 'menuPrincipal.html')
  return render(request, 'index.html')

# Función que permite añadir archivos en un .zip
#
# Parámetros:
#           myzip: file descriptor del .zip que se quiere modificar
#           fList: lista de los archivos que se agregarán al .zip
# def crearZip(fList, idt):
#   myzip = zipfile.ZipFile('/tmp/'+str(idt)+'.zip', 'w')
#   for f in fList:
#     if (f):
#       myzip.write(f)

# # Función que permite crear un mapa de calor de una imagen de cultivo
# #
# # Parámetros:
# #           input_path: nombre del archivo .zip que sube el usuario
# #           dim: dimension de las divisiones de la imagen
# def generarDiagnostico(input_path, dim, nombreOriginal):
#   image = io.imread(input_path)[0]                    
  
#   h = image.shape[1]
#   w = image.shape[0]

#   stepsH = h // dim
#   stepsW = w // dim

#   print(h,w, stepsH, stepsW)

#   tmpH = 0
#   i = 0 # Filas
#   contador = 0
#   listaImagenes = []
#   tmp = []
#   while (i < stepsH):
#     j = 0 # Columnas
#     tmpW = 0
#     tmpMapa = []
#     while (j < stepsW):
#       newImg = image[tmpW:tmpW+dim, tmpH:tmpH+dim]
#       nombre = "/tmp/%d-%d-%s"%(i, j, nombreOriginal)
#       plt.image.imsave(nombre, newImg)
#       tmp.append(nombre)
#       contador += 1
#       if (contador == 19):
#         listaImagenes.append(tmp)
#         tmp = []
#         contador = 0
#       j += 1
#       tmpW += dim
#     i += 1
#     tmpH += dim
#   if (listaImagenes == []):
#     listaImagenes.append(tmp)

#   dpi = 80
#   height, width, nbands = image.shape
#   # What size does the figure need to be in inches to fit the image?
#   figsize = width / float(dpi), height / float(dpi)

#   # Create a figure of the right size with one axes that takes up the full figure
#   fig = plt.pyplot.figure(figsize=figsize)
#   ax = fig.add_axes([0, 0, 1, 1])

#   # Hide spines, ticks, etc.
#   ax.axis('off')
#   ax.imshow(image, interpolation='nearest')

#   plantasSanas = 0
#   plantasAfectadas = 0
#   centros = []
#   for aux in range(len(listaImagenes)):
#     crearZip(listaImagenes[aux], aux)
#     with open('/tmp/'+str(aux)+'.zip', 'rb') as images_file:
#       results = visual_recognition.classify(images_file=images_file, classifier_ids=clasificadores, threshold=0.5)
#       responses_imgs = results['images'] # Extracción de las imagenes clasificadas
#       print(results)

#       for resp in responses_imgs:
#         if ("classifiers" in resp):
#           if (resp["classifiers"] == []):
#             pass
#             print("Suelo")
#           else:
#             sorted_json = sorted(resp["classifiers"][0]["classes"], key=lambda k: (float(k["score"])),reverse=True)
#             predicted_class = sorted_json[0]["class"] 
#             predicted_score = sorted_json[0]["score"]
  
#             print(resp['image'])
#             nombreImagen = re.sub("/tmp/"+str(aux)+".zip/tmp/",'', resp['image'])
#             nombreImagen = nombreImagen.split("-")
  
#             print(nombreImagen)
#             print(resp['image'])
#             if (predicted_class == "sano"):
#               print("Sano")
#               plantasSanas += 1
#             elif (predicted_class == "enfermo"):
#               plantasAfectadas += 1
#               #circ = Circle(((int(nombreImagen[0])*dim)+(dim/2),(int(nombreImagen[1])*dim)+(dim/2)), radius=dim/2, fill=False, edgecolor='#f2af00', linewidth=2)
#               centros.append([(int(nombreImagen[0])*dim)+(dim/2),(int(nombreImagen[1])*dim)+(dim/2)])
#               print("Coordenadas", (int(nombreImagen[0])*dim)+(dim/2),(int(nombreImagen[1])*dim)+(dim/2))
#               #ax.add_patch(circ)
#             elif (predicted_class == "suelo"):
#               print("Suelo")
#   numPlantasEnfermas = (plantasAfectadas*80)/100
#   for i in range(0,plantasAfectadas):
#     if (i < numPlantasEnfermas):
#       circ = Circle((centros[i][0],centros[i][1]), radius=dim/2, fill=False, edgecolor='#ff7f0e', linewidth=4)
#       ax.add_patch(circ)
#     else:
#       circ = Circle((centros[i][0],centros[i][1]), radius=dim/2, fill=False, edgecolor='#1f77b4', linewidth=4)
#       ax.add_patch(circ)

#   BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#   STATIC_URL = os.path.join(BASE_DIR, 'static/img/')
#   plt.pyplot.savefig(STATIC_URL+"diagnostico_"+nombreOriginal,  dpi=dpi, transparent=True)
#   return plantasSanas, plantasAfectadas, centros

# def dibujarProyeccion(radio, img, nombreOriginal, centros, dim):
#   dpi = 80

#   # img = plt.pyplot.imread(input_path)
#   height, width, nbands = img.shape

#   # What size does the figure need to be in inches to fit the image?
#   figsize = width / float(dpi), height / float(dpi)

#   # Create a figure of the right size with one axes that takes up the full figure
#   fig2 = plt.pyplot.figure(figsize=figsize)
#   ax2 = fig2.add_axes([0, 0, 1, 1])

#   # Hide spines, ticks, etc.
#   ax2.axis('off')

#   # Display the image.
#   ax2.imshow(img, interpolation='nearest')
#   print("radio", radio)
#   for c in centros:   
#     print("Centro", c)
#     #originalCirc = Circle((c[0],c[1]), radius=dim/2, fill=False, edgecolor='#f2af00', linewidth=1)
#     #ax2.add_patch(originalCirc)
#     propCirc = Circle((c[0],c[1]), radius=radio, fill=False, edgecolor='#ffffff', linewidth=2, ls="dashed")
#     ax2.add_patch(propCirc)

#   #ax.set(xlim=[0, width], ylim=[height, 0], aspect=1)

#   BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#   STATIC_URL = os.path.join(BASE_DIR, 'static/img/')
#   plt.pyplot.savefig(STATIC_URL+"proyeccion_"+nombreOriginal, dpi=dpi, transparent=True)


# #------------ Vista de la opción de cargar imágenes de plan de vuelo -------------#
# @csrf_exempt
# def cargarImagenes(request):
#   request.upload_handlers = [COSZipUploadHandler(request)]
#   if (request.method == 'POST'):
#     form = cargarImagenesVueloForm(request.POST, request.FILES)
#     return JsonResponse({'details': 'Imagen cargada: ' + str(request.FILES)}, )
#   else:
#   #   form = cargarImagenesVueloForm(request.POST, request.FILES)
#     return JsonResponse({'details':'Only POST'})
#   # return render(request, 'cargarImagenes.html', {'form': form, 'msg': "0"})

# #------------- Vista del menú principal -------------#
# def menuPrincipal(request):
#   if (request.method == 'GET'):
#     return render(request, 'menuPrincipal.html')

# #------------- Vista del menú de cultivos -------------#
# def monitorearCultivos(request):
#   if (request.method == 'GET'):
#     return render(request, 'monitorearCultivo.html')

# #-------------- Vista del cultivo en específico ---------#
# def infoCultivo(request):
#   if (request.method == 'GET'):
#     return render(request,'infoCultivo.html')
    
# def planVuelo(request):
#   if (request.method == 'GET'):
#     return render(request,'planVuelo.html')
    
# #--------------- Vista del estado del cultivo --------------#
# def estadoCultivo(request):
#   if (request.method == 'GET'):
#     pAfectado = math.floor((request.session['plantasA']*100)/(request.session['plantasS'] + request.session['plantasA']))
#     pRoya = 80
#     return render(request, 'estadoCultivo.html', {'imagenOriginal': request.session['imagenOriginal'], 'diagnostico': request.session['diagnostico'],
#                             'pAfectado': pAfectado, 'pRoya': pRoya})

# def generarProyeccion():
#   #Funcion de tasa de crecimiento de la roya de cafe para m2 de cultivos 
#   areaAfectada = 50*50*0.03       # Area afectada por la roya del cultivo
#   prom_germin = 28                # Promedio de germinacion en condiciones ideales en dias
#   tasa_crecimiento_n = 0.19       # Tasa de crecimiento en condiciones ideales
#   tasa_crecimiento_ex = 0.42      # Tasa de crecimiento en condiciones extremas
#   dias_revision = 60              # Numero de dias hasta la proxima revision. Dias de propagacion
#   num_pp_af = 100                 # Numero de plantas afectadas por cada 50m2
#   area_propagacion = 50*50*0.03   # Area afectada despues de la propagacion a 45 dias
#   num_plantas_propagacion = 0     # Numero de plantas afectadas por estimacion
#   radio_propagacion = 0           # Radio de propagacion a 45 dias
  
#   for i in range(dias_revision):
#     area_propagacion = area_propagacion + ((areaAfectada*tasa_crecimiento_ex)/100) 

#   num_plantas_propagacion = (area_propagacion*2000)/10000 # Numero de plantas despues de 45 dias de infeccion
#   print(num_plantas_propagacion)
#   radio_propagacion = area_propagacion/2

#   return radio_propagacion, num_plantas_propagacion, area_propagacion

# #--------------- Vista de reportes -----------------------#
# def generarReporte(request):
#   if (request.method == 'GET'):
#     minAreaMetros = 50*50*0.03         # Area en m en un cuadro de 50x50
    
#     areaSana = minAreaMetros*request.session['plantasS']
#     areaAfectada = minAreaMetros*request.session['plantasA']
#     areaTotal = areaSana + areaAfectada

#     totalPlantasSanas = math.ceil((areaSana*2000)/10000)
#     totalPlantasAfectadas = math.ceil((areaAfectada*2000)/10000)

#     aPlagas = (80*areaAfectada)/100
#     aNutrientes = areaAfectada - aPlagas
#     numP_Plagas = round((aPlagas*2000)/10000)                  # Tomando que hay 2000 matas en una hectarea
#     numP_Nutrientes = totalPlantasAfectadas - numP_Plagas

#     if (totalPlantasAfectadas != 0):
#       pNutrientes = (numP_Nutrientes*100)/totalPlantasAfectadas
#       pPlagas = (numP_Nutrientes*100)/totalPlantasAfectadas
#     else:
#       pNutrientes = 0
#       pPlagas = 0
    
#     kilosSanas = (totalPlantasSanas*2600)/2000          # Tomando que por 2000 matas hay 2600 kg de cafe
#     kilosAfectadas = (totalPlantasAfectadas*1000)/2000  # Tomando que por 2000 matas afectadas hay 1000 kg de cafe


#     #--- Datos para la proyeccion del esparcimiento de la enfermedad ---#
#     pctProp = (request.session['area_prop']*100)/aPlagas
#     incremento_prop = pctProp - 100
#     print(areaTotal, aPlagas, request.session['area_prop'])

#     return render(request, 'generarReporte.html', {'plantasS': request.session['plantasS'], 'plantasA': request.session['plantasA'],
#                             'imagenOriginal': request.session['imagenOriginal'], 'diagnostico': request.session['diagnostico'],
#                             'areaAfectada': areaAfectada, 'areaSana': areaSana, 'pPlagas': pPlagas, 'pNutrientes': pNutrientes,
#                             'aPlagas': aPlagas, 'aNutrientes': aNutrientes, 'kilosSanas': kilosSanas, 'kilosAfectadas': kilosAfectadas,
#                             'numP_Plagas': numP_Plagas, 'numP_Nutrientes': numP_Nutrientes,
#                             'numP_Sanas': totalPlantasSanas, 'numP_Afectadas': totalPlantasAfectadas, 'numPlantas_prop': request.session['numPlantas_prop'],
#                             'area_prop': request.session['area_prop'], 'incremento_prop': incremento_prop})
#     return render(request,'infoCultivo.html')

# def planVuelo(request):
 
#  #--------------- Vista del estado del cultivoinfoCultivo------#
#     return render(request,'planVuelo.html')
    
# #--------------- Vista del estado del cultivo --------------#
# def estadoCultivo(request):
#   if (request.method == 'GET'):
#     pAfectado = math.floor((request.session['plantasA']*100)/(request.session['plantasS'] + request.session['plantasA']))
#     pRoya = 80
#     return render(request, 'estadoCultivo.html', {'imagenOriginal': request.session['imagenOriginal'], 'diagnostico': request.session['diagnostico'],
#                             'pAfectado': pAfectado, 'pRoya': pRoya})

# def cargarZip(request):

#   if (request.method != 'POST'): return
#   f = request.FILES['archivo']
#   r = processZipFile(request, f)
#   print(r)

# def processZipFile(request,file):
#   from PIL import Image
#   from io import BytesIO
#   try:
#     zip = zipfile.ZipFile(file)
#   except zipfile.BadZipfile as e:
#     return print("El archivo subido no es un archivo ZIP.")
#   except zipfile.LargeZipFile as e:
#     return print("El archivo ZIP es muy grande.")

#   UserID = request.user.id
#   OperationNumber = 1
#   fileID = 1
  
#   # Create folder
#   try:
#     path = "/tmp/" + str(UserID) + "/"
#     os.mkdir(path)
#   except OSError as e:
#     pass # directory is already created

#   try:
#     path += str(OperationNumber) + "/"
#     os.mkdir(path)
#   except OSError as e:
#     pass # directory is already created

#   b = True
#   fileNames = []
#   result = []
#   # Save files
#   for f in zip.namelist():
#     if f.startswith('__MACOSX/'):
#       continue
#     elif f.lower().endswith(('.png', '.jpg', '.jpeg')):
#       with zip.open(f) as file:
#         img = Image.open(file)
#         exif_bytes = None
#         if 'exif' in img.info:
#           exif_bytes = img.info['exif']

#     nImages = 20
#     imgwidth, imgheight = img.size
#     nih = math.floor(math.sqrt(20*imgheight/imgwidth))
#     niw = math.floor(nImages/nih)
#     width = math.ceil(imgwidth/niw)
#     height = math.ceil(imgheight/nih)
    
#     count = 0
#     imageZip = zipfile.ZipFile('/tmp/zip_%d.zip'%fileID, 
#                    mode='w',
#                    compression=zipfile.ZIP_DEFLATED, 
#                    )

#     for i in range(0, imgheight, height):
#       for j in range(0, imgwidth, width):
#         box = (j, i, j+width, i+height)
#         try:
#           a = img.crop(box)
          
#           # splittedImages.append(a)

#           imgByteArr = BytesIO()
#           a.save(imgByteArr, format='JPEG', exif=exif_bytes)
#           print(fileID, count)
#           imageZip.writestr('%d-%d.jpeg'%(fileID,count), imgByteArr.getvalue())

#         except Exception as e:
#           print(e)
#           pass
#         count += 1
#         if count == nImages:
#           break
#     imageZip.close()
#     fileNames.append('/tmp/zip_%d.zip'%fileID)   
#     fileID += 1
#     file.close()
#   else:
#     print(f, "No es una imagen.")
#   return fileNames

# def generarProyeccion():
#   #Funcion de tasa de crecimiento de la roya de cafe para m2 de cultivos 
#   areaAfectada = 50*50*0.03       # Area afectada por la roya del cultivo
#   prom_germin = 28                # Promedio de germinacion en condiciones ideales en dias
#   tasa_crecimiento_n = 0.19       # Tasa de crecimiento en condiciones ideales
#   tasa_crecimiento_ex = 0.42      # Tasa de crecimiento en condiciones extremas
#   dias_revision = 60              # Numero de dias hasta la proxima revision. Dias de propagacion
#   num_pp_af = 100                 # Numero de plantas afectadas por cada 50m2
#   area_propagacion = 50*50*0.03  # Area afectada despues de la propagacion a 45 dias
#   num_plantas_propagacion = 0     # Numero de plantas afectadas por estimacion
#   radio_propagacion = 0           # Radio de propagacion a 45 dias
  
#   for i in range(dias_revision):
#     area_propagacion = area_propagacion + ((areaAfectada*tasa_crecimiento_ex)/100) 

#   num_plantas_propagacion = (area_propagacion*2000)/10000 # Numero de plantas despues de 45 dias de infeccion
#   print(num_plantas_propagacion)
#   radio_propagacion = area_propagacion/2

#   return radio_propagacion, num_plantas_propagacion, area_propagacion

# #--------------- Vista de reportes -----------------------#
# def generarReporte(request):
#   if (request.method == 'GET'):
#     minAreaMetros = 50*50*0.03         # Area en m en un cuadro de 50x50
    
#     areaSana = minAreaMetros*request.session['plantasS']
#     areaAfectada = minAreaMetros*request.session['plantasA']
#     areaTotal = areaSana + areaAfectada

#     totalPlantasSanas = math.ceil((areaSana*2000)/10000)
#     totalPlantasAfectadas = math.ceil((areaAfectada*2000)/10000)

#     aPlagas = (80*areaAfectada)/100
#     aNutrientes = areaAfectada - aPlagas
#     numP_Plagas = round((aPlagas*2000)/10000)                  # Tomando que hay 2000 matas en una hectarea
#     numP_Nutrientes = totalPlantasAfectadas - numP_Plagas

#     if (totalPlantasAfectadas != 0):
#       pNutrientes = (numP_Nutrientes*100)/totalPlantasAfectadas
#       pPlagas = (numP_Nutrientes*100)/totalPlantasAfectadas
#     else:
#       pNutrientes = 0
#       pPlagas = 0
    
#     kilosSanas = (totalPlantasSanas*2600)/2000          # Tomando que por 2000 matas hay 2600 kg de cafe
#     kilosAfectadas = (totalPlantasAfectadas*1000)/2000  # Tomando que por 2000 matas afectadas hay 1000 kg de cafe


#     #--- Datos para la proyeccion del esparcimiento de la enfermedad ---#
#     pctProp = (request.session['area_prop']*100)/aPlagas
#     incremento_prop = pctProp - 100
#     print(areaTotal, aPlagas, request.session['area_prop'])

#     return render(request, 'generarReporte.html', {'plantasS': request.session['plantasS'], 'plantasA': request.session['plantasA'],
#                             'imagenOriginal': request.session['imagenOriginal'], 'diagnostico': request.session['diagnostico'],
#                             'areaAfectada': areaAfectada, 'areaSana': areaSana, 'pPlagas': pPlagas, 'pNutrientes': pNutrientes,
#                             'aPlagas': aPlagas, 'aNutrientes': aNutrientes, 'kilosSanas': kilosSanas, 'kilosAfectadas': kilosAfectadas,
#                             'numP_Plagas': numP_Plagas, 'numP_Nutrientes': numP_Nutrientes,
#                             'numP_Sanas': totalPlantasSanas, 'numP_Afectadas': totalPlantasAfectadas, 'numPlantas_prop': request.session['numPlantas_prop'],
#                             'area_prop': request.session['area_prop'], 'incremento_prop': incremento_prop})