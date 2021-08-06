from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_notification(request):
    print(request.POST.get())