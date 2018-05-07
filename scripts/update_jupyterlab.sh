#!/bin/sh

POSIXLY_CORRECT=1 &&

manifest='efef0e1cf0d326b57c62' &&
vendor='17b64ee294d1cf4007bb' &&
main='75795a75c2b565285208' &&
tmpdir='/tmp/jupyterlab' &&
tmpdir2='/tmp/lab' &&
dstdir='/usr/local/lib/python3.5/dist-packages/jupyterlab' &&
dstdir2='/usr/local/share/jupyter/lab' &&
uuid="$(uuidgen)" &&

[ -d "$tmpdir" ] && rm -r $tmpdir;
[ -d "$tmpdir2" ] && rm -r $tmpdir2;
[ -d "$tmpdir" ] || cp -r ../jupyterlab $tmpdir &&
[ -d "$tmpdir2" ] || cp -r ../lab $tmpdir2 &&

grep -iRl "manifest.""$manifest"".js" "$tmpdir"/static | xargs sed --posix -i "s#manifest.""$manifest"".js#manifest.""$uuid"".js#" &&
grep -iRl "vendor.""$vendor"".js" "$tmpdir"/static | xargs sed --posix -i "s#vendor.""$vendor"".js#vendor.""$uuid"".js#" &&
grep -iRl "main.""$main"".js" "$tmpdir"/static | xargs sed --posix -i "s#main.""$main"".js#main.""$uuid"".js#" &&

grep -iRl "manifest.""$manifest"".js" "$tmpdir2"/static | xargs sed --posix -i "s#manifest.""$manifest"".js#manifest.""$uuid"".js#" &&
grep -iRl "vendor.""$vendor"".js" "$tmpdir2"/static | xargs sed --posix -i "s#vendor.""$vendor"".js#vendor.""$uuid"".js#" &&
grep -iRl "main.""$main"".js" "$tmpdir2"/static | xargs sed --posix -i "s#main.""$main"".js#main.""$uuid"".js#" &&

sed --posix -i "s#{{base_url}}lab/static/manifest.""$uuid"".js#https://druuu.me/lab/static/manifest.""$uuid"".js#" "$tmpdir"/static/index.html &&
sed --posix -i "s#{{base_url}}lab/static/vendor.""$uuid"".js#https://druuu.me/lab/static/vendor.""$uuid"".js#" "$tmpdir"/static/index.html &&
sed --posix -i "s#{{base_url}}lab/static/main.""$uuid"".js#https://druuu.me/lab/static/main.""$uuid"".js#" "$tmpdir"/static/index.html &&

sed --posix -i "s#{{base_url}}lab/static/manifest.""$uuid"".js#https://druuu.me/lab/static/manifest.""$uuid"".js#" "$tmpdir2"/static/index.html &&
sed --posix -i "s#{{base_url}}lab/static/vendor.""$uuid"".js#https://druuu.me/lab/static/vendor.""$uuid"".js#" "$tmpdir2"/static/index.html &&
sed --posix -i "s#{{base_url}}lab/static/main.""$uuid"".js#https://druuu.me/lab/static/main.""$uuid"".js#" "$tmpdir2"/static/index.html &&

mv "$tmpdir"/static/manifest."$manifest".js "$tmpdir"/static/manifest."$uuid".js &&
mv "$tmpdir"/static/manifest."$manifest".js.map "$tmpdir"/static/manifest."$uuid".js.map &&
mv "$tmpdir"/static/vendor."$vendor".js "$tmpdir"/static/vendor."$uuid".js &&
mv "$tmpdir"/static/vendor."$vendor".js.map "$tmpdir"/static/vendor."$uuid".js.map &&
mv "$tmpdir"/static/main."$main".js "$tmpdir"/static/main."$uuid".js &&
mv "$tmpdir"/static/main."$main".js.map "$tmpdir"/static/main."$uuid".js.map &&

mv "$tmpdir2"/static/manifest."$manifest".js "$tmpdir2"/static/manifest."$uuid".js &&
mv "$tmpdir2"/static/manifest."$manifest".js.map "$tmpdir2"/static/manifest."$uuid".js.map &&
mv "$tmpdir2"/static/vendor."$vendor".js "$tmpdir2"/static/vendor."$uuid".js &&
mv "$tmpdir2"/static/vendor."$vendor".js.map "$tmpdir2"/static/vendor."$uuid".js.map &&
mv "$tmpdir2"/static/main."$main".js "$tmpdir2"/static/main."$uuid".js &&
mv "$tmpdir2"/static/main."$main".js.map "$tmpdir2"/static/main."$uuid".js.map &&


rm -r "$dstdir" &&
cp -r "$tmpdir" "$dstdir" &&

rm -r "$dstdir2"/static &&
cp -r "$tmpdir2"/static "$dstdir2"/static
