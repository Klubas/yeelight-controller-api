callEndpoint = async (actionValue, paramValue = null) => {

    const url = currentLocation + '/api/bulb';
    const settings = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify(
                {
                    action: actionValue,
                    params: {
                        color: paramValue,
                        start: paramValue
                    }

                }
            )
    };
    try {
        const fetchResponse = await fetch(url, settings)
        const data = await fetchResponse.json()
    } catch (e) {
        await console.log(e)
    }

}

function changeLampState(){
	if(lampOn){
		callEndpoint('off')
		btnSwitch.setAttribute('value', 'On')
		lampOn = false
	} else {
		callEndpoint('on')
		btnSwitch.setAttribute('value', 'Off')
		lampOn = true
	}
}

function changeLampColor(newColor){
    console.log(newColor)
    newColor = convertHexToRGB(newColor)
    color = newColor.r.toString().concat(" ", newColor.g.toString(), " ", newColor.b.toString())
    console.log(color)
    callEndpoint('color', color)
}

function convertHexToRGB(hexColor) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hexColor);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

const btnSwitch = document.getElementById('btnSwitch')
var lampOn = true
btnSwitch.setAttribute('value', 'Off')
btnSwitch.addEventListener('click',
	function(){changeLampState()}
)

var colorLightBulb = document.getElementById('colorLightBulb')
colorLightBulb.addEventListener('change',
    function(){
        var newColor = colorLightBulb.value
        changeLampColor(newColor)
    }
)

const currentLocation = window.location.href
console.log(currentLocation)