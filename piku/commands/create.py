import os
from jinja2 import Template
from piku.core import utils
from piku.commands.version import get_version


def create_command(args):
    # build template context
    project_path = f'./{args.project}'
    toml_path = os.path.join(project_path, 'piku.toml')
    context = {
        'project': args.project,
        'piku': get_version(),
        'bundle': '7',
        'device': '',
        'serial': ''
    }

    # show piku version
    print(f'Piku v{context["piku"]}')

    # check that path doesnt exist
    if os.path.exists(project_path):
        print(f'Unable to create project: directory {project_path} already exists.')
        return

    # # select board
    # print('Please enter the name of your CircuitPython board:')
    # context['board'] = input().strip()

    # select device
    print('Please enter the usb drive path of your device CircuitPython enabled device:')
    context['device'] = input().strip()

    # select serial port
    print('Please enter the serial port for your CircuitPython device:')
    context['serial'] = input().strip()

    # create project from template
    src = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../template')
    utils.copy(src, project_path, contents=True)

    # template piku.toml
    with open(toml_path, 'r') as f:
        template = Template(f.read())
    with open(toml_path, 'w') as f:
        f.write(template.render(**context))

    # in the future allow loading an example and dependencies for a specific board

    print('Done.')
