from ibm_botocore import credentials
from django.core.files.uploadhandler import FileUploadHandler, StopUpload
import xml.etree.ElementTree as xml
import requests

COS_API_Key = 'yJoxUb3FKZBYaxzTTKJFLHmfiztVJCy81YHFJ1OVQjjp'
COS_service_instance = 'crn:v1:bluemix:public:cloud-object-storage:global:a/ce9e974530c83fa4891688cf239a0c9d:c8082bb2-3916-4649-83fc-fdad7999b2c1::'
COS_Bucket_Name = 'prueba-agrocognitive'


class COSZipUploadHandler(FileUploadHandler):
  endpoint = 's3-api.us-geo.objectstorage.softlayer.net'
  bucket = COS_Bucket_Name
  count = 1
  max_size = 100 #Mb
  lastStart = 0
  data = b''
  COS_Token_Manager = credentials.DefaultTokenManager( 
                     api_key_id=COS_API_Key,
                     service_instance_id=COS_service_instance,
                     auth_endpoint='https://iam.bluemix.net/oidc/token'
                    )
  headers = {
    'Authorization':'Bearer ' + COS_Token_Manager.get_token(),
  }
  uploadID = 0
  etags = []
  error = ''



  def requestMultipartUpload(self):
    return requests.post('https://%s/%s/%s?uploads='%
                          (self.endpoint, self.bucket, self.file_name),
                         headers = self.headers)

  def uploadPart(self):
    return requests.put('https://%s/%s/%s?partNumber=%d&uploadId=%s'%
                            (self.endpoint, self.bucket, self.file_name,
                             self.count, self.uploadID),
                        headers = self.headers,
                        data = self.data)

  def createCompleteXML(self):
    xml = '<CompleteMultipartUpload>'
    for i in self.etags:
      xml += '<Part><PartNumber>%d</PartNumber><ETag>%s</ETag></Part>'%(i[0], i[1])
    xml += '</CompleteMultipartUpload>'
    return xml

  def complete(self):
    return requests.post('https://%s/%s/%s?uploadId=%s'%
                          (self.endpoint, self.bucket, self.file_name, self.uploadID),
                         headers = self.headers,
                         data = self.createCompleteXML())
  def delete(self):
    return requests.delete('https://%s/%s/%s?uploadId=%s'%
                            (self.endpoint, self.bucket, self.file_name, self.uploadID),
                           headers = self.headers)

  def new_file(self, *args, **kwargs):
    ''' Creates the multipart upload request at IBM COS '''
    super().new_file(*args, **kwargs)
    if not self.file_name:
      self.error = 'No se subio ningún archivo.'
      raise StopUpload
    if not self.file_name.endswith(".zip"):
      self.error = 'El archivo debe tener formato ZIP.'
      raise StopUpload

    request = self.requestMultipartUpload()
    if request.status_code == 200:
      content = xml.fromstring(request.content)
      #/ 0: bucket name
      #/ 1: file name
      #/ 2: uploadID  --------v
      self.uploadID = content[2].text
    else:
      self.delete()
      self.error = 'Error interno: No se pudo almacenar el archivo. (new_file: %d)'%request.status_code
      raise StopUpload

  def receive_data_chunk(self, raw_data, start):
    ''' Every chunk of the file is to be saved inside a buffer and be send when it reach 5MB '''
    if start < self.max_size * (2 ** 20): # 100 MB
      self.data = self.data + raw_data
      if start - self.lastStart > 5 * (2 ** 20):
        request = self.uploadPart()
        self.data = b''
        self.lastStart = start
        if request.status_code == 200:
          self.etags.append( (self.count,request.headers['ETag']) )
          self.count += 1
      return raw_data
    self.delete()
    self.error = 'El tamaño del archivo no puede ser mayor a %d Mb.' % self.max_size
    raise StopUpload

  def file_complete(self, file_size):
    ''' Send the rest of the file buffer. Also, a complete signal with meta information 
        of the file parts wrtten on a XML, has to be sent to IBM COS '''
    request = self.uploadPart()
    if request.status_code == 200:
      self.etags.append( (self.count,request.headers['ETag']) )
      self.count += 1
    else:
      self.delete()
      self.error = 'Error interno: No se pudo almacenar el archivo. (uploadPart: %d)'%request.status_code
      raise StopUpload
    request = self.complete()
    if request.status_code != 200:
      self.delete()
      self.error = 'Error interno: No se pudo almacenar el archivo. (complete: %d)'%request.status_code
      raise StopUpload
    return None