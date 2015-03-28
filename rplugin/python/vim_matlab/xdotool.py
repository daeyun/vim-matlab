from command import Command
from logger import log

__author__ = 'daeyun'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class InvalidWindowIdError(Exception):
    pass


class Xdotool():
    def __init__(self, timeout=2):
        if Command('which xdotool').run()[2] != 0:
            raise RuntimeError('xdotool not found')
        self.timeout = timeout

    def run(self, command):
        log.info(command)
        result = Command(command).run(self.timeout)
        if result[2] != 0:
            if 'BadWindow' in result[1]:
                raise InvalidWindowIdError()
            log.error(result[1])
            raise RuntimeError()
        return result[0]

    def find_windows_by_class(self, window_class):
        result = self.run(
            'xdotool search --maxdepth 4 --class {}'.format(window_class))
        window_ids = result.strip().split()

        if len(window_ids) == 0:
            raise RuntimeError(
                'Unable to find window class "{}"'.format(window_class))

        return window_ids

    def find_windows_by_name(self, window_name):
        result = self.run(
            'xdotool search --maxdepth 4 --name "{}"'.format(window_name))
        window_ids = result.strip().split()

        if len(window_ids) == 0:
            raise RuntimeError(
                'Unable to find window name {}'.format(window_name))

        return window_ids

    def find_windows(self, window_name, window_class, is_unique=True):
        result = list(
            set(self.find_windows_by_class(window_class)).intersection(
                set(self.find_windows_by_name(window_name))))

        if len(result) == 0:
            raise RuntimeError(
                'Window not found: {}, {}'.format(window_name, window_class))

        if is_unique and len(result) > 1:
            raise RuntimeError(
                'More and one window found: {}, {}'.format(window_name,
                                                           window_class))

        return result

    def enter_keys(self, keys, window_id=None):
        if window_id is None:
            self.run('xdotool key --clearmodifier {}'.format(' '.join(keys)))
        else:
            self.run(
                'xdotool windowactivate --sync {} key --clearmodifiers {}'.format(
                    window_id, ' '.join(keys)))

    def get_active_window_id(self):
        return self.run('xdotool getactivewindow').strip()

    def activate_window(self, window_id):
        self.run('xdotool windowactivate --sync {}'.format(window_id))
