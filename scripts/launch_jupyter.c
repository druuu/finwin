#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <pwd.h>
#include <sys/stat.h>


int create_file(char *argv[]) {
    FILE *fp;
    char buffer[500];

    char path[100] = "/home/";
    strcat(path, argv[2]);
    strcat(path, "/.jupyter");
    mkdir(path, 0755);
    strcat(path, "/jupyter_notebook_config.py");
    fp = fopen(path, "w+");
    snprintf(buffer, sizeof(buffer), "c.NotebookApp.ip = '*'\n"
            "c.NotebookApp.port = %s\n"
            "c.NotebookApp.open_browser = False\n"
            "c.NotebookApp.token = ''\n"
            "c.NotebookApp.allow_origin = '*'\n"
            "c.NotebookApp.disable_check_xsrf = True\n"
            "c.NotebookApp.base_url = '%s'\n"
            "c.NotebookApp.notebook_dir= '/home/%s'\n"
            "c.NotebookApp.tornado_settings = {\n"
            "    \"headers\": {\n"
            "        \"Content-Security-Policy\": \"frame-ancestors 'self' *\"\n"
            "    }\n"
            "}\n"
            "c.NotebookApp.iopub_data_rate_limit=10000000000;\n", argv[1], argv[3], argv[2]);

    fprintf(fp, "%s", buffer);
    fclose(fp);

    return 0;
}


void set_user(uid_t uid, gid_t gid) {
    if (setgid(gid)) {
        perror("setgid");
        exit(1);
    }
    if (setuid(uid)) {
        perror("setuid");
        exit(1);
    }
}


int main(int argc, char *argv[]) {
    char cmd[100];
    uid_t uid;
    gid_t gid;
    struct passwd *pd;

    snprintf(cmd, sizeof(cmd), "useradd -m %s", argv[2]);
    int status = system(cmd);
    if (status) {
        perror("system");
        exit(1);
    }

    if (NULL == (pd = getpwnam(argv[2]))) {
        perror("getpwnam() error.");
        exit(1);
    }
    uid = pd->pw_uid;
    gid = pd->pw_gid;
    
    /********************** cgroups memory setup ********************************/
    char cmd2[400];
    char cmd4[400];
    char cmd5[400];

    snprintf(cmd4, sizeof(cmd4), "mkdir /sys/fs/cgroup/memory/%s", pd->pw_name);
    int status2 = system(cmd4);
    if (status2) {
        perror("system");
        exit(1);
    }

    snprintf(cmd5, sizeof(cmd5), "echo %d > /sys/fs/cgroup/memory/%s/memory.limit_in_bytes", 500000000, pd->pw_name);
    int status3 = system(cmd5);
    if (status3) {
        perror("system");
        exit(1);
    }

    snprintf(cmd2, sizeof(cmd2), "echo %d > /sys/fs/cgroup/memory/%s/cgroup.procs", getpid(), pd->pw_name);
    int status4 = system(cmd2);
    if (status4) {
        perror("system");
        exit(1);
    }
    /********************************************************************/

    /******************************** cgroups pids setup *******************************/
    char cmd3[400];
    char cmd6[400];
    char cmd7[400];

    snprintf(cmd3, sizeof(cmd3), "mkdir /sys/fs/cgroup/pids/%s", pd->pw_name);
    int status5 = system(cmd3);
    if (status5) {
        perror("system");
        exit(1);
    }

    snprintf(cmd6, sizeof(cmd6), "echo %d > /sys/fs/cgroup/pids/%s/pids.max", 50, pd->pw_name);
    int status6 = system(cmd6);
    if (status6) {
        perror("system");
        exit(1);
    }

    snprintf(cmd7, sizeof(cmd7), "echo %d > /sys/fs/cgroup/pids/%s/cgroup.procs", getpid(), pd->pw_name);
    int status7 = system(cmd7);
    if (status7) {
        perror("system");
        exit(1);
    }
    /************************************************************************/

    /***************** switch user and create configs **************/
    set_user(uid, gid);
    create_file(argv);
    /**************************************************************/

    /************ exec jupyter-notebook **************/
    char *argv2[] = {"jupyter-lab", NULL};
    char xdg_runtime_dir[400];
    char path[400];

    snprintf(xdg_runtime_dir, sizeof(xdg_runtime_dir), "XDG_RUNTIME_DIR=/run/user/%u/jupyter", uid);
    snprintf(path, sizeof(path), "PATH=/home/%s/bin:/home/%s/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/snap/bin", pd->pw_name, pd->pw_name);

    char *envp[] = {
        path,
        "TERM=screen.xterm-256color",
        "LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:",
        "LANG=en_US.UTF-8",
        0
    };


    execve("/usr/local/bin/jupyter-lab", argv2, envp);
    /*********************************************************/

    return 0;
}
