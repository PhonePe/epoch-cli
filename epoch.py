#!/usr/bin/python3 -u

import argparse
import traceback
import epochcli


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="epoch_cli")
    parser.add_argument("--file", "-f", help="Configuration file for epoch client")
    parser.add_argument("--cluster", "-c", help="Cluster name as specified in config file")
    parser.add_argument("--endpoint", "-e", help="Epoch endpoint. (For example: https://epoch.test.com)")
    parser.add_argument("--auth-header", "-t", dest="auth_header",
                        help="Authorization header value for the provided epoch endpoint")
    parser.add_argument("--insecure", "-i", help="Do not verify SSL cert for server")
    parser.add_argument("--username", "-u", help="Epoch cluster username")
    parser.add_argument("--password", "-p", help="Epoch cluster password")
    parser.add_argument("--debug", "-d", help="Print details of errors", default=False, action="store_true")
    return parser


def run():
    parser = build_parser()
    try:
        client = epochcli.EpochCli(parser)
        client.run()
    except (BrokenPipeError, IOError, KeyboardInterrupt):
        pass
    except Exception as e:
        print("Epoch CLI error: " + str(e))
        traceback.print_exc()


if __name__ == '__main__':
    run()
