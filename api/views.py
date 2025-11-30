from django.http import JsonResponse
from .weatherData_io import currentWeatherData

def get_weather(request):
    # Get parameters from the URL query string
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    units = request.GET.get('units', 'metric')
    
    if not lat or not lon:
        return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)
    
    # Call your function with the parameters
    data = currentWeatherData(lat, lon, units)
    
    if data:
        return JsonResponse(data)  # Remove safe=False
    else:
        return JsonResponse({'error': 'Location not found'}, status=404)