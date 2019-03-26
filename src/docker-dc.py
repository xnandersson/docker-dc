#!/usr/bin/env python
import docker
import os
import shutil
import uuid

BUILD_DIR = '/tmp/{uuid}/'.format(uuid=uuid.uuid4().hex)

def mkdir_build_dir():
  try:
    os.mkdir(BUILD_DIR)
  except FileExistsError as e:
    pass

def copy_files_to_build_dir():
    shutil.copyfile('Dockerfile', os.path.join(BUILD_DIR, 'Dockerfile')
    shutil.copyfile('dcpromo.py', os.path.join(BUILD_DIR, 'dcpromo.py')
    proc = subprocess.Popen(['chmod', '+x', os.path.join(BUILD_DIR, 'dcpromo.py'])
    proc.wait()

if __name__ == '__main__':
  mkdir_build_dir()
  copy_files_to_build_dir()
  client = docker.DockerClient(base_url='unix://var/run/docker.sock')
  client.images.build(path=BUILD_DIR, tag='xnandersson/samba-ad-dc', rm=True, pull=True)
