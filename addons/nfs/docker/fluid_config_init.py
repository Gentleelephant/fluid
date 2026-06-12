#  Copyright 2022 The Fluid Authors.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

#!/usr/bin/env python

import json
import os


def shell_quote(value):
    return "'" + value.replace("'", "'\\''") + "'"


def parse_mount_options(options_text):
    options = {}
    if not options_text:
        return options
    for item in options_text.split(','):
        item = item.strip()
        if not item:
            continue
        if '=' in item:
            key, value = item.split('=', 1)
            options[key.strip()] = value.strip()
        else:
            options[item] = ''
    return options


def format_mount_options(options):
    items = []
    for key in sorted(options.keys()):
        value = options[key]
        if value:
            items.append("%s=%s" % (key, value))
        else:
            items.append(key)
    return ",".join(items)


def merge_options(*option_maps):
    merged = {}
    for options in option_maps:
        merged.update(options or {})
    return merged


def generate_mount_script(obj):
    mount = obj['mounts'][0]
    config_options = mount.get('options', {})
    runtime_options = obj.get('runtimeOptions', {})
    env_options = parse_mount_options(os.environ.get('MOUNT_OPTIONS', ''))
    merged_options = merge_options(env_options, runtime_options, config_options)
    formatted_options = format_mount_options(merged_options)

    script = """
#!/bin/bash
set -ex
MNT_FROM=$mountPoint
MNT_TO=$targetPath


trap "umount ${MNT_TO}" SIGTERM
mkdir -p ${MNT_TO}
if [ -n "$MOUNT_OPTIONS" ]; then
    mount -t nfs ${MNT_FROM} ${MNT_TO} -o ${MOUNT_OPTIONS}
else
    mount -t nfs ${MNT_FROM} ${MNT_TO}
fi
sleep inf
"""

    lines = [
        "mountPoint=\"%s\"\n" % mount['mountPoint'],
        "targetPath=\"%s\"\n" % obj['targetPath'],
    ]
    if formatted_options:
        lines.append("MOUNT_OPTIONS=%s\n" % shell_quote(formatted_options))
    lines.append(script)
    return "".join(lines)


def main():
    with open("/etc/fluid/config/config.json", "r") as f:
        rawStr = f.readlines()
    obj = json.loads(rawStr[0])
    with open("mount-nfs.sh", "w") as f:
        f.write(generate_mount_script(obj))


if __name__ == "__main__":
    main()
