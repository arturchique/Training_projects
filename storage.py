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
f = open(storage_path, "w")
f.close()

if args.key and args.val:
    with open(f"{storage_path}") as file:
        try:
            # при первом открытии пустого не .json файла не удается загрузить из него пустой дикт,
            # поэтому вылавливаем эту ошибку и избегаем ее (создаем новые данные)
            data = json.load(file)
            data[args.key] = args.val
            print(data)
        except JSONDecodeError:
            data = {args.key: args.val}
    with open(f"{storage_path}", "w") as file:
        json.dump(data, file)
        print(f"Запись сохранена успешно в {storage_path}")
elif args.key:
    with open(f"{storage_path}", 'r') as file:
        file = json.load(file)
        print(file.get(args.key))
