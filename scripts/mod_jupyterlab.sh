#/bin/sh

set -o posix &&
POSIXLY_CORRECT=1 &&
echo 'path /usr/local/share/jupyter/lab/static/index.html' &&
printf "\n" &&
echo '<script type="text/javascript" src="https://notebook.micropyramid.com/lab/static/manifest.efef0e1cf0d326b57c62.js"></script><script type="text/javascript" src="https://notebook.micropyramid.com/lab/static/vendor.17b64ee294d1cf4007bb.js"></script><script type="text/javascript" src="https://notebook.micropyramid.com/lab/static/main.75795a75c2b565285208.js"></script><script id='base_url' type="text/javascript" data-base_url="{{ base_url }}" src="https://notebook.micropyramid.com/lab/static/refactored.js"></script>' &&
printf "\n" &&
echo "mod notebook package" &&
echo "yarn install and build"
