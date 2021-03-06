#!/usr/bin/python

"""
-------------------------
Ansible module for avconv
-------------------------

Usage example::

    task = {
        'avconv': {
            'rate': frame_rate,
            'width': width,
            'height': height,
            'display': display,
            'codec': codec,
            'options': options,
            'file': file_path
        }
    }
"""

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from ansible.module_utils.basic import *

import tempfile


def wrap_async(cmd):
    pid_path = tempfile.mktemp()
    cmd = 'nohup ' + cmd
    cmd += ' & echo $! > ' + pid_path + ' && cat ' + pid_path
    return 'bash -c "{}"'.format(cmd)


def main():
    module = AnsibleModule(
        argument_spec={
            'rate': {'required': True, 'type': 'int'},
            'width': {'required': True, 'type': 'int'},
            'height': {'required': True, 'type': 'int'},
            'display': {'required': True, 'type': 'int'},
            'codec': {'required': True, 'type': 'str'},
            'options': {'required': False, 'type': 'list'},
            'file': {'required': True, 'type': 'str'},
        })

    rate = module.params['rate']
    width = module.params['width']
    height = module.params['height']
    display = module.params['display']
    codec = module.params['codec']
    options = module.params['options']
    file = module.params['file']

    cmd = 'avconv -f x11grab -r {} -s {}x{} -i :{} -codec {}'.format(
        rate, width, height, display, codec)

    if options:
        cmd += ' ' + ' '.join(options)

    cmd += ' ' + file + ' >/dev/null 2>&1'
    cmd = wrap_async(cmd)

    rc, stdout, stderr = module.run_command(cmd, check_rc=True)
    module.exit_json(cmd=cmd, rc=rc, stderr=stderr, stdout=stdout)


if __name__ == '__main__':
    main()
