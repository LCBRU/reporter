import importlib
import pkgutil


def get_sub_modules(path, prefix):
    result = []

    for m in pkgutil.iter_modules(path):
        new_module_name = prefix + m[1]
        result.append(new_module_name)
        result.extend(get_sub_modules(
            [path[0] + '/' + m[1]],
            new_module_name + '.'
        ))

    return result


for m in get_sub_modules(__path__, __name__ + '.'):
    importlib.import_module(m)
