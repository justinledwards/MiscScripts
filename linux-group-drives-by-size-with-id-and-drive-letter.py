#!/usr/bin/env python3

import os
import re
from pathlib import Path

def get_drive_ids(drive):
    drive_ids = []
    preferred_drive_id = None
    by_id_path = Path('/dev/disk/by-id/')
    for symlink in by_id_path.glob('*'):
        if symlink.is_symlink() and not re.search(r'part\d+$', str(symlink)):
            target = os.readlink(symlink)
            if re.search(rf'/{drive}$', target) and not re.match(r'wwn-', symlink.name) and not re.match(r'scsi-\d+', symlink.name):
                if re.match(r'scsi-SATA', symlink.name):
                    preferred_drive_id = symlink.name
                else:
                    drive_ids.append(symlink.name)
    return [preferred_drive_id] if preferred_drive_id else drive_ids

def main():
    drives = []
    for drive in Path('/dev').glob('sd*'):
        if re.match(r'sd[a-z]+$', drive.name):
            size = os.popen(f'lsblk -dn -o SIZE -b {drive}').read().strip()
            size = int(size) // (2 ** 30)
            drive_ids = get_drive_ids(drive.name)
            for drive_id in drive_ids:
                drives.append((size, drive.name, drive_id))

    drives.sort()
    print("size, dev, by-id")
    for size, drive_name, drive_id in drives:
        print(f"{size}GiB, {drive_name}, {drive_id}")

if __name__ == "__main__":
    main()
