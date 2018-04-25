#!/bin/sh

port=$1
base_url=$2

mkdir ~/.jupyter && \
echo 'import os


c.NotebookApp.ip = "*"
c.NotebookApp.port = '$port'
c.NotebookApp.open_browser = False
c.NotebookApp.token = ""
c.NotebookApp.allow_origin = "*"
c.NotebookApp.disable_check_xsrf = True
c.NotebookApp.base_url = "'$base_url'"

c.NotebookApp.tornado_settings = {
    "headers": {
        "Content-Security-Policy": "frame-ancestors '"'"self"'"' *"
    }
}

c.NotebookApp.iopub_data_rate_limit=10000000000' > ~/.jupyter/jupyter_notebook_config.py && \
jupyter-notebook --config=~/.jupyter/jupyter_notebook_config.py
