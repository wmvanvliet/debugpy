# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root
# for license information.

from __future__ import absolute_import, division, print_function, unicode_literals

import io
import os
import pytest_timeout
import sys

from ptvsd.common import log


def dump():
    if log.log_dir is None:
        return
    log.info("Dumping logs from {0!j}", log.log_dir)

    for dirpath, dirnames, filenames in os.walk(log.log_dir):
        for name in sorted(filenames):
            if not name.startswith("ptvsd") and not name.startswith("pydevd"):
                continue
            try:
                path = os.path.join(dirpath, name)
                with io.open(path, encoding="utf-8", errors="backslashreplace") as f:
                    s = f.read()
            except Exception:
                pass
            else:
                path = os.path.relpath(path, log.log_dir)
                pytest_timeout.write_title(path)
                print(s, file=sys.stderr)
