from datetime import datetime
from yeelight import Bulb


class BulbCache:
    def __init__(self):
        self.cached_bulbs = dict()

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
            'cached_properties': cached_properties

        }

    def update_cached_property(self, bulb_id, property_name, property_value):
        self.cached_bulbs[bulb_id]['cached_properties'][property_name] = property_value

    def clear(self):
        self.cached_bulbs.clear()

    def list(self) -> list:
        return list(self.cached_bulbs.values())
