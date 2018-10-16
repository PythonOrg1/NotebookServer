#
#Custom pattern by JayYin for deeplearning
#
#for auto save .py file & .html file to the path when user save code in notebook
#
# Based off of 
# https://github.com/jupyter/notebook/blob/master/docs/source/extending/savehooks.rst

import io
import os
from notebook.utils import to_api_path
from nbconvert.exporters.script import ScriptExporter
from nbconvert.exporters.html import HTMLExporter

_script_exporter = None
_html_exporter = None

def script_post_save(model, os_path, contents_manager, **kwargs):
    if (model['type'] != 'notebook'):
        return

    # auto save .py
    global _script_exporter
    if _script_exporter is None:
        _script_exporter = ScriptExporter(parent=contents_manager)
    log_py = contents_manager.log

    base, ext = os.path.splitext(os_path)
    script, resources = _script_exporter.from_filename(os_path)
    script_fname = base + resources.get('output_extension', '.txt')
    log_py.info("Saving script /%s", to_api_path(script_fname, contents_manager.root_dir))
    with io.open(script_fname, 'w', encoding='utf-8') as f:
        f.write(script)


    # auto save html
    global _html_exporter
    if _html_exporter is None:
        _html_exporter = HTMLExporter(parent=contents_manager)
    log_h5 = contents_manager.log

    base, ext = os.path.splitext(os_path)
    script, resources = _html_exporter.from_filename(os_path)
    script_fname = base + resources.get('output_extension', '.txt')
    log_h5.info("Saving html /%s", to_api_path(script_fname, contents_manager.root_dir))
    with io.open(script_fname, 'w', encoding='utf-8') as f:
        f.write(script)

c.FileContentsManager.post_save_hook = script_post_save
