from django.http import JsonResponse

def custom_404_view(request, exception):
    return JsonResponse({'error': 'Page not found'}, status=404)