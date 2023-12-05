#!/bin/env python3
# coding: utf8

import logging
from pathlib import Path

from typer import Typer, Option, echo, style

from alist_sync.models import AlistServer

from alist_sync.run_copy import CopyToTarget
from alist_sync.run_mirror import Mirror
from alist_sync.run_sync import Sync
from alist_sync.run_sync_incr import SyncIncr

app = Typer()


@app.command()
def copy(
        base_url: str = Option('http://localhost:5244',
                               '--host', '-h', help="Base URL for Alist Host", ),
        username: str = Option('', "--username", "-u",
                               help="Alist Admin Username"),
        password: str = Option('', "--password", "-p",
                               help="Alist Admin Password"),
        token: str = Option('', "--token", "-t", help="Alist Admin Token"),
        verify: bool = Option(True, "--verify", "-v",
                              help="Verify SSL Certificates"),
        source: str = Option(..., "--source", "-s", help="Source Path"),
        target: list[str] = Option(..., "--target", "-t", help="Target Path"),
):
    """复制任务"""
    alist_info = AlistServer(base_url=base_url, username=username,
                             password=password, token=token, verify=verify)
    echo(
        f"Will Be Copy '{source}' -> {target} on {alist_info.base_url} [{alist_info.username}]")
    return CopyToTarget(alist_info, source_path=source, targets_path=target).run()


@app.command('mirror')
def mirror(
        base_url: str = Option('http://localhost:5244',
                               '--host', '-h', help="Base URL for Alist Host", ),
        username: str = Option('', "--username", "-u",
                               help="Alist Admin Username"),
        password: str = Option('', "--password", "-p",
                               help="Alist Admin Password"),
        token: str = Option('', "--token", "-t", help="Alist Admin Token"),
        verify: bool = Option(True, "--verify", "-v",
                              help="Verify SSL Certificates"),
        source: str = Option(..., "--source", "-s", help="Source Path"),
        target: list[str] = Option(..., "--target", "-t", help="Target Path"),
):
    """镜像"""
    alist_info = AlistServer(base_url=base_url, username=username,
                             password=password, token=token, verify=verify)
    echo(f"Will Be Mirror '{source}' -> {target} "
         f"on {alist_info.base_url} [{alist_info.username}]"
         )
    return Mirror(alist_info, source_path=source, targets_path=target).run()


@app.command()
def sync(
        base_url: str = Option('http://localhost:5244',
                               '--host', '-h', help="Alist Host", ),
        username: str = Option('', "--username", "-u",
                               help="Alist Admin Username"),
        password: str = Option('', "--password", "-p",
                               help="Alist Admin Password"),
        token: str = Option('', "--token", "-t", help="Alist Admin Token"),
        verify: bool = Option(True, "--verify", "-v",
                              help="Verify SSL Certificates"),
        sync_group: list[str] = Option(..., "--sync", "-s", help="Sync Group"),
):
    """同步任务"""
    alist_info = AlistServer(base_url=base_url, username=username,
                             password=password, token=token, verify=verify)
    echo(style("Hello Sync", fg="green", bg="black", bold=True))
    return Sync(alist_info, sync_group)


@app.command(name='sync-incr')
def sync_incr(
        config_dir: str = Option(..., "--name", "-n", help="在Alist上存储的配置目录"),
        cache_dir: str = Option(Path(), "--cache-dir", "-c", help="配置缓存目录"),
        base_url: str = Option('http://localhost:5244',
                               '--host', '-h', help="Alist Host", ),
        username: str = Option('', "--username", "-u",
                               help="Alist Admin Username"),
        password: str = Option('', "--password", "-p",
                               help="Alist Admin Password"),
        token: str = Option('', "--token", "-t", help="Alist Admin Token"),
        verify: bool = Option(True, "--verify", "-v",
                              help="Verify SSL Certificates"),
        sync_group: list[str] = Option(..., "--sync", "-s", help="Sync Group"),

):
    """增量同步"""
    alist_info = AlistServer(base_url=base_url, username=username,
                             password=password, token=token, verify=verify)
    echo(f"增量同步：{sync_group}")
    return SyncIncr(
        alist_info,
        config_dir,
        cache_dir,
        sync_group
    ).run()


if __name__ == '__main__':
    # logging.basicConfig(level='INFO')
    logger = logging.getLogger('alist-sync')
    hander = logging.StreamHandler()
    hander.setLevel("DEBUG")
    # hander.setFormatter("")
    logger.addHandler(hander)
    logger.setLevel("DEBUG")
    app()
