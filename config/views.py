from django.http import JsonResponse

def homepage(request):
    return JsonResponse({'message': '歡迎來到 EatHub API'}, status=200)