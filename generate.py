import argparse
import yaml
import os

from jinja2 import Environment, FileSystemLoader

parser = argparse.ArgumentParser(description="generate my personal site.")
parser.add_argument("cv", type=str, help='A Yaml file representing the CV.')
parser.add_argument('template', type=str,
                    help='template file to generate Html from.')
parser.add_argument('-o', '--output', type=str,
                    help='final output file. stdout if not specified')
parser.add_argument('--shared', type=str, action='append', default=[],
                    help='YAML file with sections shared across languages; '
                    'may be repeated. Keys in the CV file take precedence.')
parser.add_argument('--lang', type=str, default='en',
                    help='language used to resolve localized fields.')

LANGS = {'en', 'zh'}


def localize(value, lang):
    """Resolve {en: ..., zh: ...} maps to the value for `lang`."""
    if isinstance(value, dict):
        if value and set(value) <= LANGS:
            if lang not in value:
                raise KeyError(f'missing {lang!r} translation in {value!r}')
            return localize(value[lang], lang)
        return {k: localize(v, lang) for k, v in value.items()}
    if isinstance(value, list):
        return [localize(v, lang) for v in value]
    return value


def main():
    result = parser.parse_args()
    cv = {}
    for path in result.shared:
        with open(path) as fd:
            cv.update(yaml.safe_load(fd))
    with open(result.cv) as fd:
        cv.update(yaml.safe_load(fd))
    cv = localize(cv, result.lang)

    env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.join(
        result.template, os.path.pardir))), trim_blocks=True, lstrip_blocks=True)
    tmpl = env.get_template(os.path.basename(result.template))

    if result.output is None:
        print(tmpl.render(**cv))
    else:
        with open(result.output, 'w') as fd:
            fd.write(tmpl.render(**cv))


if __name__ == '__main__':
    main()
