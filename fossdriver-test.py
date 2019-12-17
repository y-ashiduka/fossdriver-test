#!/usr/bin/python3

import os
import sys

args = sys.argv
argc = len(args)

if (argc != 3):
	print('Usage: %s <source file> <output spdx path>', args[0])
	quit()

print('scan source file=', args[1])
print('output spdx path=', args[2])
spdx = args[2] + '/' + args[1] + '.spdx'
print('spdx path=', spdx)

from fossdriver.config import FossConfig
from fossdriver.server import FossServer
from fossdriver.tasks import (CreateFolder, Upload, Scanners, Copyright, Reuse, BulkTextMatch, SPDXTV)

os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

config = FossConfig()
configPath = os.path.join(os.path.expanduser('~'),".fossdriverrc")
print('fossology scan test: fossfriver_setting_file_path= ', configPath)

config.configure(configPath)

server = FossServer(config)
server.Login()

# upload archive.zip to the new folder
Upload(server, args[1], "Software Repository").run()

# start the Monk and Nomos scanners
Scanners(server, args[1], "Software Repository").run()

# and export an SPDX tag-value file
SPDXTV(server, args[1], "Software Repository", spdx).run()
