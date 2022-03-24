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
    project_path = args.directory or f'./{args.project}'
    toml_path = os.path.join(project_path, 'pyproject.toml')
    readme_path = os.path.join(project_path, 'README.md')
    gitignore_path = os.path.join(project_path, '.gitignore')
    code_path = os.path.join(project_path, 'project')
    template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../template')
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
    if os.path.exists(project_path) and not args.directory:
        print(f'Unable to create project: directory {project_path} already exists.')
        return
    os.makedirs(project_path, exist_ok=True)

    # create pyproject.toml if it doesn't exist (fail if it does)
    if not os.path.exists(toml_path):
        utils.copy(os.path.join(template_dir, 'pyproject.toml'), toml_path)
        template(toml_path, context)
    else:
        print(f'Unable to create project: {toml_path} already exists.')
        return

    # create readme if it doesn't exist
    if not os.path.exists(readme_path):
        utils.copy(os.path.join(template_dir, 'README.md'), readme_path)
        template(readme_path, context)

    # create gitignore if it doesn't already exist
    if not os.path.exists(gitignore_path):
        utils.copy(os.path.join(template_dir, '.gitignore'), gitignore_path)
        template(readme_path, context)

    # create default code folder if it doesn't exist
    if not os.path.exists(code_path):
        utils.copy(os.path.join(template_dir, 'project'), code_path, contents=True)

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
