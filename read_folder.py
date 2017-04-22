#!/usr/bin/env python3

import os

def read_folder(folder, surename):
    files = []
    file_index = 0
    for filename in os.listdir(folder):
        if filename.endswith(surename):
            files.append('\\'.join([folder,filename]))
    return files
