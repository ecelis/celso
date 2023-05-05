import os


def make_dir(dir_fd):
    os.mkdir(dir_fd, 0o700)
