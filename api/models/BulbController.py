import ipaddress
import socket

from yeelight import discover_bulbs, Bulb, LightType


def __sync_bulbs__() -> list:
    """
    Discover bulbs in local network and returns in a list
    """

    bulbs = list()

    try:
        discovered_bulbs = discover_bulbs(timeout=2)
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
            ip=ip,
            port=port,
            model=model
        )

        found_bulb.set_name(name)
        properties = found_bulb.get_properties()

        bulbs.append({
            'bulb': found_bulb,
            'name': name,
            'model': model,
            'ip': ip,
            'metadata':
                {
                    'id': identifier,
                    'ip': ip,
                    'name': name,
                    'model': model,
                    'properties': properties
                }
        })

    return bulbs


def hex_to_rgb(hex_value):
    try:
        return tuple(int(hex_value[i:i + 2], 16) for i in (0, 2, 4))
    except Exception as e:
        raise Exception('Invalid hex value {} - {}'.format(hex_value, str(e)))


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
    :return:
    """
    if ip:
        try:
            bulb = Bulb(ip=ip)
            ipaddress.ip_address(str(ip))
            bulb.get_properties()
            return bulb
        except socket.error:
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
    def power(ip, state='toggle') -> dict:
        """
        Switch bulb power state to <state>
        :param ip:
        :param ip:
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
            properties = bulb.get_properties()
            return properties
        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def change_color(ip, values, color_mode='rgb') -> dict:
        """
        Change bulb color to <color>
        :param ip:
        :param values:
            RGB:    (<int>, <int>, <int>)   red, green, blue or hex value
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
            if not bulb:
                raise Exception("Bulb not found.")

            if color_mode == 'rgb':
                if len(values) == 1:
                    rgb_values = hex_to_rgb(str(values[0]))
                elif len(values) == 3:
                    rgb_values = values
                else:
                    raise Exception(
                        "RGB mode needs exactly 1 (hexadecimal) or 3 values (decimal). [{}]".format(values))

                red = rgb_values[0]
                green = rgb_values[1]
                blue = rgb_values[2]
                bulb.set_rgb(red, green, blue)
                properties = bulb.get_properties()
                return properties

            if color_mode == 'hsv':
                if len(values) > 3 or len(values) < 2:
                    raise Exception("HSV mode needs 2 or 3 values. [{}]".format(values))
                hue = values[0]
                sat = values[1]
                val = values[2]
                bulb.set_hsv(hue, sat, val)
                properties = bulb.get_properties()
                return properties

            if color_mode == 'bright':
                if len(values) > 2 or len(values) < 1:
                    raise Exception("BRIGHT mode needs 1 or 2 values. [{}]".format(values))
                bright = values[0]
                ambient = values[1] if values[1] else False
                light_type = LightType.Ambient if ambient > 0 else LightType.Main
                bulb.set_brightness(bright, light_type=light_type)
                properties = bulb.get_properties()
                return properties

            if color_mode == 'temp':
                if len(values) != 1:
                    raise Exception("TEMP mode needs exactly 1 value. [{}]".format(values))
                temp = values[0]
                bulb.set_color_temp(temp)
                properties = bulb.get_properties()
                return properties

            raise Exception("Unexpected color mode {}".format(color_mode))

        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def rename_bulb(ip, new_name) -> dict:
        """
        Change bulb name to <new_name>
        :param ip:
        :param new_name:
        :return:
        """
        if not ip and not new_name:
            raise Exception("Parameters <ip> and <new_name> must be specified.")

        bulb = get_bulb(ip=ip)

        try:
            bulb.set_name(name=new_name)
            properties = bulb.get_properties()
            return properties

        except Exception as e:
            raise Exception(str(e))
