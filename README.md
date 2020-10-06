# YeelightHub API

This repo contains the yeelight-controller-api. 

With it you can (theoretically, I just have one) view and control all yeelight bulbs in your network. 

#### Start server locally:
    
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
There's a postman collection in the repo with usage examples os all endpoints.

    [POST] /api/logon
Returns the authentication token
    
    [GET] /api/bulbs
Returns all properties of all the bulbs in the network
    
    [GET] /api/bulb
Return on or all properties of the specified bulb
    
    [PUT] /api/bulb
Update bulb name
    
    [POST] /api/bulb/power
Change bulb power state (on/off). Default is to toggle.
    
    [POST] /api/bulb/color
Change bulb color. Color modes may be RGB, HSV, Brightness, or Color temperature

