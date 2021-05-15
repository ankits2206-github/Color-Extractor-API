from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
import requests
from io import BytesIO
from colorthief import ColorThief
import urllib

# Create your views here.

@api_view(['GET'])
def index(request):
    if request.method == "GET":
        url = request.GET['src']
        urllib.request.urlretrieve(url, "sample.png")
        color_thief = ColorThief("sample.png")
        dominant = color_thief.get_color(quality=1)
        dominant_hex='#%02x%02x%02x' % dominant
        img = Image.open("sample.png")
        width, height = img.size

        freq = dict()


        for i in range(width):
            left = img.getpixel((i,0))
            right = img.getpixel((i,height-1))
            
            t=0
            if(len(left)==4):
                t=1
            color_tuple = (left[t],left[t+1],left[t+2])
            
            
            if color_tuple in freq.keys():
                freq[color_tuple] += 1
            else:
                freq[color_tuple]=1
                
            if(len(right)==4):
                t=1
            color_tuple = (right[t],right[t+1],right[t+2])
            
            if color_tuple in freq.keys():
                freq[color_tuple]+= 1
            else:
                freq[color_tuple]=1

        for i in range(height):
            top = img.getpixel((0, i))
            bottom = img.getpixel((width-1, i))
            
            t=0
            if len(top)==4:
                t=1
            color_tuple = (top[t],top[t+1],top[t+2])
            
            
            if color_tuple in freq.keys():
                freq[color_tuple] += 1
            else:
                freq[color_tuple]=1
                
            if len(bottom)==4:
                t=1
            color_tuple = (bottom[t],bottom[t+1],bottom[t+2])
            
            
            if color_tuple in freq.keys():
                freq[color_tuple] += 1
            else:
                freq[color_tuple]=1
                


        border = max(freq, key=freq.get)
        
        dominant_border='#%02x%02x%02x' % border
        
        return Response({'logo_border': dominant_border,'dominant_color':dominant_hex},status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)