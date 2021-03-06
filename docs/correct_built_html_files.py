import os
import json

this_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(this_dir, 'permitted_namespaces.json'), 'r') as file:
    PERMITTED_NAMESPACES = json.loads(file.read())


def trim_namespace(full_namespace):
    for namespace_to_check, permitted_namespace in PERMITTED_NAMESPACES.items():
        if namespace_to_check in full_namespace:
            return permitted_namespace
    return full_namespace


def modify_html_file(html_filepath):
    with open(html_filepath) as file:
        html_contents = file.read()
    html_contents = ''.join([char for i, char in enumerate(html_contents)
                             if not (char.isdigit() and html_contents[i+1:i+5] == '.png')])
    html_contents = ''.join([char for i, char in enumerate(html_contents)
                             if not (char.isdigit() and html_contents[i+1:i+5] == '.png')])
    html_contents = html_contents.replace('3.141592653589793', 'π')
    html_contents = html_contents.replace('docs/ivy.html', '../ivy"')
    html_contents = html_contents.replace('docs/ivy_mech.html', '../mech"')
    html_contents = html_contents.replace('docs/ivy_vision.html', '../vision"')
    html_contents = html_contents.replace('docs/ivy_robot.html', '../robot"')
    html_contents = html_contents.replace('docs/ivy_memory.html', '../memory"')
    html_contents = html_contents.replace('docs/ivy_gym.html', '../gym"')
    contents_split1 = html_contents.split('<code class="sig-prename descclassname">')
    contents_split2 = [item.split('</code>') for item in contents_split1]
    contents_split2_modded = [contents_split2[0]] +\
                             [[trim_namespace(item[0])] + item[1:] for item in contents_split2[1:]]
    contents_split1_modded = ['</code>'.join(item) for item in contents_split2_modded]
    html_contents_modded = '<code class="sig-prename descclassname">'.join(contents_split1_modded)
    with open(html_filepath, 'w') as file:
        file.write(html_contents_modded)


def modify_html_files(directory):
    items_in_dir = os.listdir(directory)
    paths = [os.path.join(directory, item) for item in items_in_dir]
    for item in paths:
        if item[-5:] == '.html':
            modify_html_file(item)
        elif os.path.isdir(item):
            modify_html_files(item)


modify_html_files('build')
print('\nParsed and corrected built html files\n')
