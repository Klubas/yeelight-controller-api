# YeelightHub API

This repo contains the yeelight-controller-api. With this you can get and control all yeelight bulbs in your network. 

## Todo

* Create endpoint to change/create scenes

### Start server locally:
    
    gunicorn --bind <hostname>:<port> wsgi:app
    
### Deploy to balena application

    balena push <application-name>

> make sure you are using the correct Dockerfiles    

### Environment variables (.env)

    #.env 
    YC_DEBUG=True                   # Debug mode, if true will add stacktrace field in json response
    YC_USERNAME=admin               # Username
    YC_PWD=secret                   # Password
    YC_LOCAL_TOKEN=local_network    # Define if you want to accepet requests from local network without authentication

#### Endpoints

Returns the authentication token
    
    [POST] /api/logon
    
Returns all properties of all the bulbs in the network
    
    [GET] /api/bulbs
    
Return one or all properties of the specified bulb

    [GET] /api/bulb?ip=<bulb_ip>[&property=<property_name>]
    
Rename bulb

    [PUT] /api/bulb?ip=<bulb_ip>[&new_name=<new_name>]
    
Change bulb power state (on/off). Default is to toggle.

    [POST] /api/bulb/power?ip=<bulb_ip>[&state=<on/off/toggle>]

Change bulb color. Color modes may be RGB, HSV, Brightness, or Color temperature

    [POST] /api/bulb/color?ip=<bulb_ip>&color=<red>&color=<green>&color=<blue>


There's a postman collection in the repo with usage examples os all endpoints.


