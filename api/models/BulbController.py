from dotenv import load_dotenv
from yeelight import LightType

from api.models.BulbCache import BulbCache

load_dotenv()
found_bulbs = BulbCache()


class BulbColorController:
    @staticmethod
    def change_temp(bulb, values):
        if len(values) != 1:
            raise Exception("TEMP mode needs exactly 1 value. [{}]".format(values))

        temp = values[0]

        if temp > 6500 or temp < 1700:
            raise Exception("TEMP must be between 1700 and 6500. [{}]".format(values))

        bulb.set_color_temp(temp)

    @staticmethod
    def change_bright(bulb, values):
        if len(values) > 2 or len(values) < 1:
            raise Exception("BRIGHT mode needs 1 or 2 values. [{}]".format(values))
        if len(values) == 1:
            ambient = False
        else:
            ambient = values[1] if values[1] else None

        bright = values[0]

        if bright > 100 or bright < 0:
            raise Exception("TEMP must be between 0 and 100. [{}]".format(values))

        if ambient is not None:
            bulb.set_brightness(
                bright, LightType.Ambient if ambient > 0 else LightType.Main)
        else:
            bulb.set_brightness(bright)

    @staticmethod
    def change_hsv(bulb, values):
        if len(values) > 3 or len(values) < 2:
            raise Exception("HSV mode needs 2 or 3 values. [{}]".format(values))

        hue = values[0]
        sat = values[1]
        val = values[2]

        if (hue > 360 or hue < 0) \
                or (sat > 100 or sat < 0) \
                or (val > 100 or val < 0):
            raise Exception(
                "HSV values must be between 0 - 360 for Hue and 0 - 100 for Sat and Val . [{}]".format(values))

        bulb.set_hsv(hue, sat, val)

    @staticmethod
    def change_rgb(bulb, values):

        def hex_to_rgb(hex_value):
            try:
                return tuple(int(hex_value[i:i + 2], 16) for i in (0, 2, 4))
            except Exception as e:
                raise Exception('Invalid hex value {} - {}'.format(hex_value, str(e)))

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

        if (red > 255 or red < 0) \
                or (green > 255 or green < 0) \
                or (blue > 255 or green < 0):
            raise Exception(
                "RGB values must be between 0 and 255. [{}]".format(values))

        bulb.set_rgb(red, green, blue)


class BulbController:
    @staticmethod
    def get_bulb(ip=None, identifier=None):
        return found_bulbs.get_bulb(ip=ip, identifier=identifier)

    @staticmethod
    def get_bulbs(ip=None, name=None, model=None, metadata=False, identifier=None):
        return found_bulbs.get_bulbs(
            ip=ip,
            name=name,
            model=model,
            identifier=identifier
        )

    @staticmethod
    def power(ip=None, state='toggle', identifier=None) -> dict:
        """
        Switch bulb power state to <state>
        :param ip:
        :param identifier:
        :param state:
        :return:
        """
        states = ['on', 'off', 'toggle']

        if state.lower() not in states:
            raise Exception("Invalid power state [{}]. Must be in {}.".format(state, str(states)))

        bulb = found_bulbs.get_bulb(ip=ip, identifier=identifier)

        try:
            if state == states[0]:  # on
                bulb.turn_on()
            elif state == states[1]:  # off
                bulb.turn_off()
            else:  # toggle
                bulb.toggle()
            found_bulbs.update_property(identifier, 'power', state)
            return found_bulbs.get_bulb_properties(identifier)

        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def change_color(ip, values, color_mode='rgb', identifier=None) -> dict:
        """
        Change bulb color to <color>
        :param ip:
        :param identifier:
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

        bulb = found_bulbs.get_bulb(ip=ip, identifier=identifier)

        try:
            if not bulb:
                raise Exception("Bulb not found.")

            if color_mode == 'rgb':
                BulbColorController.change_rgb(bulb, values)

            if color_mode == 'hsv':
                BulbColorController.change_hsv(bulb, values)

            if color_mode == 'bright':
                BulbColorController.change_bright(bulb, values)

            if color_mode == 'temp':
                BulbColorController.change_temp(bulb, values)

            found_bulbs.update_cached_property(
                identifier=identifier
                , property_name='color_mode'
                , property_value=color_mode
            )

            found_bulbs.sync_bulb_properties(identifier)

            return found_bulbs.get_bulb_properties(identifier)

        except Exception as e:
            raise Exception(str(e))

    @staticmethod
    def rename_bulb(ip, new_name, identifier) -> dict:
        """
        Change bulb name to <new_name>
        :param ip:
        :param identifier:
        :param new_name:
        :return:
        """
        if not identifier and not ip and not new_name:
            raise Exception("Parameters <identifier> and <new_name> must be specified.")

        bulb = found_bulbs.get_bulb(ip=ip, identifier=identifier)

        try:
            bulb.set_name(name=new_name)
            found_bulbs.update_property(identifier, 'name', new_name)
            return found_bulbs.get_bulb_properties(identifier)

        except Exception as e:
            raise Exception(str(e))
