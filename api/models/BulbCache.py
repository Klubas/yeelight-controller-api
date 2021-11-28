import ipaddress
import os
import socket
from datetime import datetime
from yeelight import Bulb, discover_bulbs


class BulbCache:
    def __init__(self):
        self.cached_bulbs = dict()

    def __sync_bulbs__(self) -> list:
        """
        Discover bulbs in local network and returns in a list
        """
        try:
            discovered_bulbs = discover_bulbs(timeout=int(os.getenv('YC_SYNC_TIMEOUT')))
        except Exception as e:
            raise Exception(str(e))

        for bulb in discovered_bulbs:
            self.insert_bulb(bulb)

        bulbs = self.list()

        return bulbs

    def get_bulbs(self, ip=None, name=None, model=None, identifier=None, cache_only=False) -> list:
        """
        Get a list of bulbs by ip, name or model
        :param identifier:
        :param ip:
        :param name:
        :param model:
        :param cache_only:
        :return list:
        """

        param = 'ip'
        value = ip
        return_all = False

        if name:
            param = 'name'
            value = name
        elif model:
            param = 'model'
            value = model
        elif not ip and not identifier:
            return_all = True
        elif identifier:
            param = 'id'
            value = identifier
        elif ip:
            ipaddress.ip_address(str(ip))

        if not cache_only:
            self.__sync_bulbs__()

        bulbs = self.list()

        if return_all:
            return bulbs
        else:
            for bulb in bulbs:
                if bulb[param] != value:
                    bulbs.pop(bulb)
        return bulbs

    def get_bulb(self, ip=None, identifier=None) -> Bulb:
        """
        Get a Bulb by IP address
        :param ip:
        :param identifier:
        :return:
        """

        if identifier:
            for bulb in self.list():
                if bulb['id'] == identifier:
                    ip = bulb['ip']

        if not ip:
            for bulb in self.__sync_bulbs__():
                if bulb['id'] == identifier:
                    ip = bulb['ip']

        if ip:
            try:
                bulb = Bulb(ip=ip)
                ipaddress.ip_address(str(ip))
                bulb.get_properties()
                return bulb
            except socket.error:
                raise Exception("Bulb not found for the specified IP {}".format(ip))
        else:
            raise Exception("You must specify an ip address or bulb identifier.")

    def insert_bulb(self, bulb):

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

        if identifier in self.cached_bulbs.keys():
            cached_properties = self.cached_bulbs[identifier]['cached_properties']
        else:
            cached_properties = dict()

        self.cached_bulbs[identifier] = {
            'id': identifier,
            'name': name,
            'model': model,
            'ip': ip,
            'power': properties['power'],
            'bright': properties['bright'],
            'ct': properties['ct'],
            'rgb': properties['rgb'],
            'hue': properties['hue'],
            'sat': properties['sat'],
            'current_brightness': properties['current_brightness'],
            'properties': properties,
            'cached_properties': cached_properties,
            'timestamp': str(datetime.now())
        }

        if len(cached_properties.items()) == 0:
            self.update_cached_property(identifier, 'color_mode', 'temp')

    def update_cached_property(self, bulb_id, property_name, property_value):
        self.cached_bulbs[bulb_id]['cached_properties'][property_name] = property_value

    def clear(self):
        self.cached_bulbs.clear()

    def list(self) -> list:
        return list(self.cached_bulbs.values())
