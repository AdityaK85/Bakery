import os
import traceback
from django.core.files.images import ImageFile
from PIL import Image
import io
from django.http import HttpResponse
from PIL import Image
# Compress formdata and blob image size minimum is 375.0 KB 

def img_compressed_size(thumbnail, img_name):  
    try:
        target_size_bytes = 375 * 1024                 
        quality_setting = 95
        
        if thumbnail.size > target_size_bytes:
            img = Image.open(thumbnail)
            img = img.convert('RGB')
            
            while True:
                temp_buffer = io.BytesIO()
                img.save(temp_buffer, 'JPEG', quality=quality_setting)
                image_size_bytes = len(temp_buffer.getvalue())
                if image_size_bytes <= target_size_bytes:
                    break

                quality_setting -= 1
            temp_buffer.seek(0)

            return ImageFile(temp_buffer, name=f"{img_name}.jpeg")
        else:
            return ImageFile(io.BytesIO(thumbnail.read()), name=f"{img_name}.jpeg")
    except:
        traceback.print_exc()
        return HttpResponse('Something went wrong')


