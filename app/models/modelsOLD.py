import logging
from yeelight import discover_bulbs, Bulb


class BulbController:
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

    def music_mode(self, bulb_name=None, start=False):
        if bulb_name is None:
            logging.info('Unsuported action')
        else:

            bulb = self.get_bulb()

            if start:
                return bulb.start_music()
            else:
                return bulb.stop_music()

    def turn_on(self, bulb_name=None):
        response = None
        if bulb_name:
            for bulb in self.bulbs:  # refatorar pra receber uma lista?
                if bulb['name'] == bulb_name:
                    response = bulb['bulb'].turn_on()
        else:
            for bulb in self.bulbs:
                response = bulb['bulb'].turn_on()
        return response

    def turn_off(self, bulb_name=None):
        response = None
        if bulb_name:
            for bulb in self.bulbs:  # refatorar pra receber uma lista?
                if bulb['name'] == bulb_name:
                    response = bulb['bulb'].turn_off()
        else:
            for bulb in self.bulbs:
                response = bulb['bulb'].turn_off()
        return response

    def set_bulb_color(self, color=(255, 255, 255), bulb_name=None):
        try:
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
        except Exception as e:
            return str(e)

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

    def get_bulb(self, bulb_name=None):
        if bulb_name:
            for bulb in self.bulbs:  # refatorar pra receber uma lista?
                if bulb['name'] == bulb_name:
                    return bulb['bulb']
        else:
            for bulb in self.bulbs:
                return bulb['bulb']

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
            return self.turn_on(bulb_name=name)

        elif action == 'off':
            return self.turn_off(bulb_name=name)

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
            return self.set_bulb_color(bulb_name=name, color=color)

        elif action == 'music':

            start = params['start']
            return self.music_mode(bulb_name=name, start=start)

        elif action == 'rename':

            new_name = params['new_name'] if 'new_name' in params else None

            if not new_name:
                return

            return self.set_bulb_name(new_name=new_name, bulb_name=name)
