import argparse

import bottle

from shibumi import model


def configure_database():
    bottle.Bottle().install(model.db)
    model.create_tables()


def main():
    parser = argparse.ArgumentParser(prog='shibumi')
    subparsers = parser.add_subparsers(dest='cmd')
    db_parser = subparsers.add_parser('initdb')
    args = parser.parse_args()

    if args.cmd == 'initdb':
        configure_database()
