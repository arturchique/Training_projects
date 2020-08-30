import sys
import os
import tempfile
import json
import argparse

from json import JSONDecodeError

parser = argparse.ArgumentParser()
parser.add_argument("--key", help="Enter --key [key] to read or --key [key] with --val [val] to write")
parser.add_argument("--val", help="Enter -key [key] with --val [val] to write")

args = parser.parse_args()

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

if args.key and args.val:
    try:
        with open(f"{storage_path}") as file:
            # при первом открытии пустого не .json файла не удается загрузить из него пустой дикт,
            # поэтому вылавливаем эту ошибку и избегаем ее (создаем новые данные)
            data = json.load(file)
            data.setdefault(args.key, []).append(args.val)
    except FileNotFoundError:
        data = {args.key: [args.val]}
    except JSONDecodeError:
        data = {args.key: [args.val]}
    with open(f"{storage_path}", "w") as file:
        json.dump(data, file)
        print("")
elif args.key:
    try:
        with open(f"{storage_path}", 'r') as file:
            try:
                file = json.load(file)
                print(", ".join(file.get(args.key)))
            except JSONDecodeError:
                print(None)
    except FileNotFoundError:
        f = open(storage_path, "w")
        f.close()
        print("")
    except TypeError:
        print(None)

