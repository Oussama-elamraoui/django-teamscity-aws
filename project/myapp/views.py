from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

# Create your views here.
class HelloWorldView(View):
    def get(self, request):

        host = request.get_host()
        ip = host.split(':')[0] 
        return JsonResponse({
            'message': 'Yes, you connected successfully!',
            'api': ip,
            'status': 'after the update of auto scaling group'
        })
