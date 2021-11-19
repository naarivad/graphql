import re
import setuptools


extras_require = {
    'docs': [
        'sphinx',
        'sphinxcontrib_trio',
        'sphinx-rtd-theme',
    ],
}

with open('requirements.txt', 'r') as file:
    install_requires = file.read().splitlines()

packages = [
    'graphql',
    'graphql.client',
]

_version_regex = re.compile(
    r'^__version__\s*=\s*["\']((?:[0-9]+\.)*[0-9]+(?:\.?([a-z]+)(?:\.?[0-9])?)?)["\']$',
    re.MULTILINE,
)

with open('graphql/__init__.py') as file:
    match = _version_regex.search(file.read())

version = match.group(1)

if match.group(2) is not None:
    try:
        import subprocess

        process = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'], stdout=subprocess.PIPE)
        out, _ = process.communicate()
        if out:
            version += out.decode('utf-8').strip()

        process = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE)
        out, _ = process.communicate()
        if out:
            version += '+g' + out.decode('utf-8').strip()
    except Exception as e:
        pass


setuptools.setup(
    author='Varun J',
    description='An async Python library to interact with GraphQL APIs.',
    extras_require=extras_require,
    include_package_data=True,
    install_requires=install_requires,
    license='Hippocratic License',
    name='graphql',
    packages=packages,
    python_requires='>=3.6.0',
    url='https://github.com/naarivad/graphql',
    version=version,
)
