import sys
from os import path
from argparse import ArgumentParser
from setproctitle import setproctitle
from loadconfig import Config
import logging

def get_config(opt_vars):
    """ Merge configuration from 'config.py' of ListenBrainz, commandline arguments and \
        the default values with order of preference

        ConfigFile > CommandlineArguments > DefaultConfig
    """

    config = {  "KAFKA_CONNECT": "localhost:9092",
                "CASSANDRA_SERVER": "localhost",
                "CASSANDRA_KEYSPACE": "listenbrainz",
                "CASSANDRA_REPLICATION_FACTOR": "1",
                "SQLALCHEMY_DATABASE_URI": "postgresql://listenbrainz@/listenbrainz"
             }
    config.update(opt_vars)

    try:
        opt_vars['CONFIG'] = path.abspath(opt_vars['CONFIG'])
        custom_config = Config(path.dirname(__file__)).from_pyfile(opt_vars['CONFIG'])
        config.update(custom_config)
    except Exception, e:
        log = logging.getLogger(__name__)
        log.error(e)

    return config


def argparse_factory(desc):
    opt_parser = ArgumentParser(description=desc)
    opt_parser.add_argument('-c', '--config',
                            dest='CONFIG',
                            default=path.dirname(__file__) + "/../../config.py",
                            help='/path/to/config.py for configuration of listenstore')
    opt_parser.add_argument('-l', '--loglevel',
                            dest='LOGLEVEL',
                            default='INFO',
                            help='DEBUG | INFO | WARNING | ERROR | CRITICAL')
#    opt_parser.add_argument('-v',
#                            dest='VERBOSE',
#                            action='store_true',
#                            help='Enable logging to stdout',
#                            default=False)
    return opt_parser


def parse_args_and_config(opt_parser):
    conf = get_config(vars(opt_parser.parse_args()))
    set_process_title(conf)
    return conf


def get_process_name():
    return path.basename(sys.argv[0]).split('.')[0]


def set_process_title(config):
    setproctitle("%s" % (get_process_name()))
