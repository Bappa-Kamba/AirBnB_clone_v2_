#!/usr/bin/python3
"""
Fabric script generates .tgz archive of all in web_static/ using func 'do_pack'
Usage: fab -f 1-pack_web_static.py do_pack

All files in the folder web_static must be added to the final archive
All archives must be stored in the folder 'versions' (create folder if none)
Create archive "web_static_<year><month><day><hour><minute><second>.tgz"
The function do_pack must return the archive path, else return None
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Packs the contents of the web_static folder into a tarball"""
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        filename = "versions/web_static_{}.tgz".format(now)
        local("tar -czvf {} web_static".format(filename))
        return filename
    except:
        return None
