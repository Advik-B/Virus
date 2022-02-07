import subprocess
import typing
import sys
import os


def run_hidden(
    command: typing.Union[str, list],
    shell: bool = True,
    stdout: typing.TextIO = sys.stdout,
    stderr: typing.TextIO = sys.stderr,
    stdin: typing.TextIO = sys.stdin,
    cwd: str = os.getcwd(),
) -> subprocess.CompletedProcess:
    SW_HIDE = 0
    info = subprocess.STARTUPINFO()
    info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = SW_HIDE
    return subprocess.Popen(
        command,
        startupinfo=info,
        shell=shell,
        stderr=stderr,
        stdout=stdout,
        stdin=stdin,
        cwd=cwd,
    )

