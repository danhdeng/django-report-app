import base64,uuid
from django.core.files.base import ContentFile

def get_report_image(data):
    _ , str_image=data.split(';base64')
    print(str_image)
    decoded_image = base64.b64decode(str_image)
    file_name =str(uuid.uuid4()) + '.png'
    data=ContentFile(decoded_image, file_name)
    return data