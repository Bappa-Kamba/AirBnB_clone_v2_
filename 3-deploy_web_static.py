#!/usr/bin/python3
from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime

env.hosts = ['54.197.82.225', '54.157.180.23']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder.

    Returns:
        Path to the created archive on success, None on failure.
    """
    try:
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_path = 'versions/web_static_{}.tgz'.format(timestamp)
        local('mkdir -p versions')
        local('tar -czvf {} web_static'.format(archive_path))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.

    Args:
        archive_path: The path to the archive to deploy.

    Returns:
        True if all operations have been done correctly, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the temporary directory on the web server
        put(archive_path, '/tmp/')

        # Extract the archive to a new folder on the web server
        archive_filename = archive_path.split('/')[-1]
        archive_foldername = archive_filename.split('.')[0]
        run('sudo mkdir -p /data/web_static/releases/{}'.format(
            archive_foldername))
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_filename, archive_foldername))

        # Delete the archive from the web server
        run('sudo rm /tmp/{}'.format(archive_filename))

        # Move the contents of the extracted folder to the web server's
        # web_static directory and delete the extracted folder
        run('sudo mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(
                archive_foldername, archive_foldername))
        run('sudo rm -rf /data/web_static/releases/{}/web_static'
            .format(archive_foldername))

        # Delete the symbolic link to the current web server version
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link to the new version of the web server
        run('sudo ln -s /data/web_static/releases/{}/ '
            '/data/web_static/current'.format(archive_foldername))

        return True

    except:
        return False


def deploy():
    """
    Creates and distributes an archive to your web servers.

    Returns:
        True if all operations have been done correctly, False otherwise.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
