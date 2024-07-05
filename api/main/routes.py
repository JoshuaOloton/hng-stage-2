from . import main
from flask import jsonify, request
from os import environ
import requests

@main.route('/')
def index():
    return 'Navigate to the hello route!'

@main.route('/hello')
def greeting():
    name = request.args.get('visitor_name')
    if name is None or name == "":
        display_name = ""
    else:
        display_name = name.strip("'\"") # remove quotes from name

    greeting_intro = f'Hello, {display_name}!' if display_name != "" else "Hello Guest!"

    # get client ip address
    if request.headers.getlist("X-Forwarded-For"):
        ip_result = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    else:
        ip_result = request.remote_addr

    # get location and temperature
    weather_url = f"http://api.weatherapi.com/v1/current.json?key={environ.get('API_KEY')}&q={ip_result}"

    location_response = requests.get(weather_url)
    if location_response.status_code != 200:
        return jsonify({
        'client_ip': ip_result,
        'location': 'Location not found.',
        'greeting': greeting_intro
    })
    
    # parse location json
    location_result = location_response.json()
    location = location_result.get('location', {})
    region = location.get('region', 'Region not found.')

    current = location_result.get('current', {})
    temp_c =  current.get('temp_c', 'Temperature not found.')

    return jsonify({
        'client_ip': ip_result,
        'location': region,
        'greeting': f'{greeting_intro}, the temperature is {temp_c} degrees Celsius in {region}'
    })
    