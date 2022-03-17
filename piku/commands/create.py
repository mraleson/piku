import os
from jinja2 import Template
from piku.core import utils, packages
from piku.commands.version import get_version


def template(path, context):
    with open(path, 'r') as f:
        template = Template(f.read())
    with open(path, 'w') as f:
        f.write(template.render(**context))

def create_command(args):
    # build template context
    project_path = f'./{args.project}'
    toml_path = os.path.join(project_path, 'pyproject.toml')
    readme_path = os.path.join(project_path, 'README.md')
    context = {
        'project': args.project,
        'piku': get_version(),
        'circuit_python': packages.latest_target(),
        'device': '',
        'serial': ''
    }

    # show piku version
    print(f'Piku v{context["piku"]} creating project {args.project}')

    # check that path doesnt exist
    if os.path.exists(project_path):
        print(f'Unable to create project: directory {project_path} already exists.')
        return

    # create project from template
    src = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../template')
    utils.copy(src, project_path, contents=True)

    # template files
    template(toml_path, context)
    template(readme_path, context)

    print('Done.')

    # in the future allow loading an example and dependencies for a specific board

    # # select board
    # print('Please enter the name of your CircuitPython board:')
    # context['board'] = input().strip()

    # # select device
    # print('Please enter the usb drive path of your device CircuitPython enabled device:')
    # context['device'] = input().strip()
    #
    # # select serial port
    # print('Please enter the serial port for your CircuitPython device:')
    # context['serial'] = input().strip()
