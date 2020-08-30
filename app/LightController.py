import logging
from yeelight import discover_bulbs, Bulb


class LightController:
    def __init__(self):
        self.bulbs = list()

        for bulb in discover_bulbs():

            found_bulb = Bulb(
                    ip=bulb['ip']
                    , port=bulb['port']
                    , model=bulb['capabilities']['model']
            )

            if bulb['capabilities']['name'] == '':
                name = bulb['ip']
            else:
                name = bulb['capabilities']['name']
            found_bulb.set_name(name)

            self.bulbs.append({
                    'bulb': found_bulb
                    , 'name': name
                    , 'ip': bulb['ip']
                }
            )

    def turn_on(self, bulb_name=None):
        if bulb_name:
            for bulb in self.bulbs: # refatorar pra receber uma lista?
                if bulb['name'] == bulb_name:
                    bulb['bulb'].turn_on()
        else:
            for bulb in self.bulbs:
                bulb['bulb'].turn_on()

    def turn_off(self, bulb_name=None):
        if bulb_name:
            for bulb in self.bulbs: # refatorar pra receber uma lista?
                if bulb['name'] == bulb_name:
                    bulb['bulb'].turn_off()
        else:
            for bulb in self.bulbs:
                bulb['bulb'].turn_off()

    def set_bulb_color(self, color=(255, 255, 255), bulb_name=None):
        if bulb_name:
            for bulb in self.bulbs:
                if bulb['name'] == bulb_name:
                    bulb['bulb'].set_rgb(
                        red=int(color[0]), green=int(color[1]), blue=int(color[2])
                    )
        else:
            for bulb in self.bulbs:
                bulb['bulb'].set_rgb(
                    red=int(color[0]), green=int(color[1]), blue=int(color[2])
                )

    def __get_all_bulbs_properties__(self) -> list:
        properties = list()
        for bulb in self.bulbs:
            properties.append(bulb['bulb'].get_properties())
        return properties

    def get_bulb_names(self) -> list:
        names = list()
        for bulb in self.bulbs:
            names.append(bulb['name'])
        return names

    def set_bulb_name(self, new_name, bulb_name=None):
        if not bulb_name or not new_name:
            logging.info(
                '{modulo} No name set'.format(
                    modulo=__file__
                )
            )
            return

        bulb_to_rename = None

        for bulb in self.bulbs:
            if bulb['name'] == bulb_name:
                bulb_to_rename = bulb['bulb']
                break

        if not bulb_to_rename:
            logging.info(
                '{modulo} Bulb {bulb_name} not found'.format(
                    modulo=__file__, bulb_name=bulb_name
                )
            )
            return

        bulb_to_rename.set_name(new_name)

    def run_action(self, name=None, action=None, params=None):

        if action == 'on':
            self.turn_on(bulb_name=name)

        elif action == 'off':
            self.turn_off(bulb_name=name)

        elif action == 'color':

            color = params['color'] if 'color' in params else None

            if not color:
                logging.info(
                    '{module} No color specified'.format(
                        module=__file__
                    )
                )
                return

            color = color.split(' ')

            logging.info(
                '{module} Bulb {name} set to color {color}'.format(
                    module=__file__, name=name, color=str(color)
                )
            )
            self.set_bulb_color(bulb_name=name, color=color)

        elif action == 'rename':

            new_name = params['new_name'] if 'new_name' in params else None

            if not new_name:
                return

            self.set_bulb_name(new_name=new_name, bulb_name=name)


