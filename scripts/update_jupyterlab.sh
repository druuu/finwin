#!/bin/sh

POSIXLY_CORRECT=1 &&

manifest='efef0e1cf0d326b57c62' &&
vendor='17b64ee294d1cf4007bb' &&
main='75795a75c2b565285208' &&
tmpdir='/tmp/jupyterlab' &&
appdir='/usr/local/share/jupyter/lab' &&
dstdir='/usr/local/lib/python3.5/dist-packages/jupyterlab' &&
uuid="$(uuidgen)" &&

[ -d "$tmpdir" ] && rm -r $tmpdir;
[ -d "$tmpdir" ] || cp -r ../jupyterlab $tmpdir &&

grep $manifest "$tmpdir"/static/index.html &&
grep $vendor "$tmpdir"/static/index.html &&
grep $main "$tmpdir"/static/index.html &&

sed --posix -i "s#{{base_url}}lab/static/manifest.""$manifest"".js#https://druuu.me/lab/static""$uuid""/manifest.""$manifest"".js#" "$tmpdir"/static/index.html &&
sed --posix -i "s#{{base_url}}lab/static/vendor.""$vendor"".js#https://druuu.me/lab/static""$uuid""/vendor.""$vendor"".js#" "$tmpdir"/static/index.html &&
sed --posix -i "s#{{base_url}}lab/static/main.""$main"".js#https://druuu.me/lab/static""$uuid""/main.""$main"".js#" "$tmpdir"/static/index.html &&

sed --posix -i "s#{{base_url}}lab/static/manifest.""$manifest"".js#https://druuu.me/lab/static""$uuid""/manifest.""$manifest"".js#" "$appdir"/static/index.html &&
sed --posix -i "s#{{base_url}}lab/static/vendor.""$vendor"".js#https://druuu.me/lab/static""$uuid""/vendor.""$vendor"".js#" "$appdir"/static/index.html &&
sed --posix -i "s#{{base_url}}lab/static/main.""$main"".js#https://druuu.me/lab/static""$uuid""/main.""$main"".js#" "$appdir"/static/index.html &&

mv "$tmpdir"/static2 "$tmpdir"/static"$uuid" &&

rm -r "$dstdir" &&
rm -r "$appdir" &&
cp -r "$tmpdir" "$dstdir" &&
cp -r "$tmpdir"/static"$uuid" "$appdir"/
