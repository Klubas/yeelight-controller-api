import logging
from yeelight import discover_bulbs, Bulb


class BulbController:
    def __init__(self):
        self.bulbs = list()
        self.sync_bulbs()

    def get_bulbs_metadata(self) -> list:
        """
        Return list of bulbs metadata in a dict
        :return:
        """
        bulbs = list()

        for bulb in self.bulbs:
            bulbs.append(bulb)

        for bulb in bulbs:
            bulb.pop('bulb')

        return bulbs

    def get_bulbs(self, ip=None, name=None, model=None, return_metadata=False) -> list:
        """
        Get a list of bulbs by ip, name or model
        :param ip:
        :param name:
        :param model:
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
        else:
            return_all = True

        for bulb in self.bulbs:
            if bulb[param] == value or return_all:
                bulbs.append(bulb if return_metadata else bulb['bulb'])
        return bulbs

    def get_bulb(self, ip=None, name=None) -> Bulb:
        """
        Get a Bulb by name or IP address
        :param ip:
        :param name:
        :return:
        """

        if ip or name:

            bulbs = self.get_bulbs(ip=ip, name=name)

            if len(bulbs) > 0:
                raise Exception("Multiple bulbs found for the specified arguments: Name={} ip={}"
                                .format(name, ip))
            else:
                return bulbs[0]

        else:
            raise Exception("You must specify a name or ip address.")

    def power(self, bulb_ip=None, bulb_name=None, state='on') -> bool:
        """
        Switch bulb power state to <state>
        :param bulb_ip:
        :param bulb_name:
        :param state:
        :return:
        """

        bulb = self.get_bulb(ip=bulb_ip, name=bulb_name)

        try:
            if state == 'on':
                bulb.turn_on()
            elif state == 'off':
                bulb.turn_off()
            else:
                raise Exception("Invalid power state [{}]. (on/off).".format(state))
        except Exception as e:
            logging.info(str(e))
            return False

    def change_color(self, ip, color, color_type='rgb') -> bool:
        """
        Change bulb color to <color>
        :param ip:
        :param color:
        :param color_type:
        :return:
        """
        return False

    def rename_bulb(self, ip, new_name) -> bool:
        """
        Change bulb name to <new_name>
        :param ip:
        :param new_name:
        :return:
        """
        if not ip and not new_name:
            raise Exception("Parameters <ip> and <new_name> must be especified.")

        bulb = self.get_bulb(ip=ip)

        try:
            bulb.set_name(name=new_name)
            self.sync_bulbs()
            return True

        except Exception as e:
            return False

    def sync_bulbs(self) -> None:
        """
        Discover bulbs in local network and saves in a list
        """

        bulbs = list()

        for bulb in discover_bulbs():

            ip = bulb['ip']
            port = bulb['port']
            model = bulb['capabilities']['model']
            name = bulb['capabilities']['name']
            name = name if name != '' else model
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
                    , 'properties': properties
                    , 'id': identifier
                }
            )

        self.bulbs = bulbs
