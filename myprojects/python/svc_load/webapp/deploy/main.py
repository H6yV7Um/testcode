#coding:utf-8

from fabric.api import *
from fabric.network import disconnect_all
from .deploy_settings import venv_fab, scripts_path, cmd_map


def main(cmd_code, path=None):
    '''Func Doc'''
    if cmd_code not in cmd_map:
        raise ValueError("Invalid op code")
    cmd = cmd_map[cmd_code]
    if path is not None:
        cmd_line = "{} --show=debug -f {} {}:{}".format(venv_fab,scripts_path, cmd, path)
    else:
        cmd_line = "{} --show=debug -f {} {}".format(venv_fab,scripts_path, cmd)
    local(cmd_line)
    #释放所有ssh连接
    disconnect_all()



if __name__ == '__main__':
    main(1)