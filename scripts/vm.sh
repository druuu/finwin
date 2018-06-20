#!/bin/sh

id="$1";
server="server""$1";

touch /home/notebook/heartbeat/"$server";

while true;
do
    last_modified=$(stat -c %Y /home/notebook/heartbeat/"$server");
    now=$(date +%s);
    diff=$((now - last_modified));
    reset() {
        echo "resetting" "$server";
        virsh destroy "$server" &&
        virsh undefine "$server" &&
        virt-clone --name "$server" --mac 52:54:00:6c:3c:"$server" --original bnbs --file "$server".img &&
        virsh start "$server" &&
        touch /home/notebook/heartbeat/"$server" || exit 1;
    };
    check_diff_and_reset() {
        [[ diff -gt 30 ]] && reset || exit 1;
    };
    check_state_and_reset() { 
        virsh domstate "$server" | grep running && diff_reset || exit 1;
    };

    check_state_and_reset && check_diff_and_reset || exit 1;
    sleep 1
done
