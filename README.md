# YeelightHub API

This repo contains the yeelight-controller-api. With this you can get and control all yeelight bulbs in your network. 

### Start server locally:
    
    gunicorn --bind <hostname>:<port> wsgi:app
    
### Deploy to balena application

    balena push <application-name>

> make sure you are using the correct Dockerfiles    

#### User credentials:

    #.env 
    YC_USERNAME='admin'
    YC_PWD='secret'
    YC_DEBUG=True

#### Endpoints

Returns the authentication token
    
    [POST] /api/logon
    
Returns all properties of all the bulbs in the network
    
    [GET] /api/bulbs
    
Return one or all properties of the specified bulb

    [GET] /api/bulb?ip=<bulb_ip>[&property=<property_name>]
    
Update bulb name

    [PUT] /api/bulb?ip=<bulb_ip>
    
Change bulb power state (on/off). Default is to toggle.

    [POST] /api/bulb/power?ip=<bulb_ip>[&state=<on/off/toggle>]

Change bulb color. Color modes may be RGB, HSV, Brightness, or Color temperature

    [POST] /api/bulb/color?ip=<bulb_ip>&color=<red>&color=<green>&color=<blue>


There's a postman collection in the repo with usage examples os all endpoints.


