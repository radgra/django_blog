from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .forms import LikeForm
# Create your views here.


@require_http_methods(["POST"])
def set_like(request):
    body = json.loads(request.body)
    if request.user.is_authenticated and request.user.is_writer is False:
        body["profil"] = request.user.userprofil.id
        form = LikeForm(body)
        if form.is_valid():
            print("Yeahh")
            form.save()
            return JsonResponse({"code":201})
        else:
            return JsonResponse({"errors":form.errors})
            

    return JsonResponse({"errors": "You have to register","code":401})
