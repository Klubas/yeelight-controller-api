import ipaddress, socket
from yeelight import discover_bulbs, Bulb, LightType


def __sync_bulbs__() -> list:
    """
    Discover bulbs in local network and saves in a list
    """

    bulbs = list()

    try:
        discovered_bulbs = discover_bulbs()
    except Exception as e:
        raise Exception(str(e))

    for bulb in discovered_bulbs:
        ip = bulb['ip']
        port = bulb['port']
        model = bulb['capabilities']['model']
        name = bulb['capabilities']['name']
        name = name if name != '' else ip
        identifier = bulb['capabilities']['id']

        found_bulb = Bulb(
            ip=ip
            , port=port
            , model=model
        )

        found_bulb.set_name(name)
        properties = found_bulb.get_properties()

        bulbs.append({
            'bulb': found_bulb
            , 'name': name
            , 'model': model
            , 'ip': ip
            , 'metadata': {
                'id': identifier
                , 'ip': ip
                , 'name': name
                , 'model': model
                , 'properties': properties
            }
        })

    return bulbs


def get_bulbs(ip=None, name=None, model=None, metadata=False) -> list:
    """
    Get a list of bulbs by ip, name or model
    :param ip:
    :param name:
    :param model:
    :param metadata:
    :return list:
    """
    bulbs = list()

    param = 'ip'
    value = ip
    return_all = False

    if name:
        param = 'name'
        value = name
    elif model:
        param = 'model'
        value = model
    elif not ip:
        return_all = True
    elif ip:
        ipaddress.ip_address(str(ip))

    for bulb in __sync_bulbs__():
        if bulb[param] == value or return_all:
            bulbs.append(bulb['metadata'] if metadata else bulb['bulb'])
    return bulbs


def get_bulb(ip=None) -> Bulb:
    """
    Get a Bulb by name or IP address
    :param ip:
    :param name:
    :return:
    """
    if ip:
        try:
            bulb = Bulb(ip=ip)
            ipaddress.ip_address(str(ip))
            return bulb
        except socket.error as e:
            raise Exception("Bulb not found for the specified IP {}".format(ip))
    else:
        raise Exception("You must specify an ip address.")


class BulbController:
    @staticmethod
    def get_bulb(ip=None):
        return get_bulb(ip=ip)

    @staticmethod
    def get_bulbs(ip=None, name=None, model=None, metadata=False):
        return get_bulbs(
            ip=ip,
            name=name,
            model=model,
            metadata=metadata
        )

    @staticmethod
    def power(ip, state='toggle') -> bool:
        """
        Switch bulb power state to <state>
        :param ip:
        :param bulb_ip:
        :param state:
        :return:
        """
        states = ['on', 'off', 'toggle']

        if state.lower() not in states:
            raise Exception("Invalid power state [{}]. Must be in {}.".format(state, str(states)))

        bulb = get_bulb(ip=ip)

        try:
            if state == states[0]:  # on
                bulb.turn_on()
            elif state == states[1]:  # off
                bulb.turn_off()
            else:  # toggle
                bulb.toggle()

        except Exception as e:
            raise Exception(str(e))
        return True

    @staticmethod
    def change_color(ip, values, color_mode='rgb') -> bool:
        """
        Change bulb color to <color>
        :param ip:
        :param values:
            RGB:    (<int>, <int>, <int>)   red, green, blue
            HSV:    (<int>, <int>, [int])   hue, saturation, value
            BRIGHT: (<int>, [int])          brightness, ambient_light [0,1]
            TEMP:   (<int>, )               temperature
        :param color_mode:
        :return:
        """
        modes = ['rgb', 'hsv', 'bright', 'temp']

        if color_mode.lower() not in modes:
            raise Exception("Invalid color type <{}>. Must be in {}".format(color_mode, str(modes)))

        if not values:
            raise Exception("Parameter <values> must be specified.")

        bulb = get_bulb(ip=ip)

        try:
            if bulb:
                if color_mode == modes[0]:
                    if len(values) != 3:
                        raise Exception("RGB mode needs exactly 3 values. [{}]".format(values))
                    red = values[0]
                    green = values[1]
                    blue = values[2]
                    try:
                        bulb.set_rgb(red, green, blue)
                    except Exception as e:
                        raise e
                elif color_mode == modes[1]:
                    if len(values) > 3 or len(values) < 2:
                        raise Exception("HSV mode needs 2 or 3 values. [{}]".format(values))
                    hue = values[0]
                    sat = values[1]
                    val = values[2]
                    bulb.set_hsv(hue, sat, val)
                elif color_mode == modes[2]:
                    if len(values) > 2 or len(values) < 1:
                        raise Exception("BRIGHT mode needs 1 or 2 values. [{}]".format(values))
                    bright = values[0]
                    ambient = values[1] if values[1] else False
                    light_type = LightType.Ambient if ambient > 0 else LightType.Main
                    bulb.set_brightness(bright, light_type=light_type)
                elif color_mode == modes[3]:
                    if len(values) != 1:
                        raise Exception("TEMP mode needs exactly 1 value. [{}]".format(values))
                    temp = values[0]
                    bulb.set_color_temp(temp)
                return True
            else:
                return False
        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def rename_bulb(ip, new_name) -> bool:
        """
        Change bulb name to <new_name>
        :param ip:
        :param new_name:
        :return:
        """
        if not ip and not new_name:
            raise Exception("Parameters <ip> and <new_name> must be especified.")

        bulb = get_bulb(ip=ip)

        try:
            bulb.set_name(name=new_name)
            return True

        except Exception as e:
            raise Exception(str(e))


