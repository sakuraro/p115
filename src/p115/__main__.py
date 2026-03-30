import argparse

from p115.app import main


parser = argparse.ArgumentParser(description='Python 115')
parser.add_argument('method', type=str, default='help', help='Method type. Example: upload, help...')
parser.add_argument('-l', '--local_path', type=str, help='Local path')
parser.add_argument('-r', '--remote_path', type=str, help='Remote path')

args = parser.parse_args()

main(method=args.method, local_path=args.local_path, remote_path=args.remote_path)
