#coding:utf-8


from optparse import OptionParser
import signal
import data_runners
from data_runners import LocalRunner, MasterRunner, SlaveRunner
from rpc.Glogger import Glogger

logger = Glogger.getLogger()

def parse_options():
    """
    Handle command-line options with optparse.OptionParser.

    Return list of arguments, largely for use in `parse_arguments`.
    """

    # Initialize
    parser = OptionParser(usage="python [options]")

    # if this process should be run in distributed mode as master
    parser.add_option(
        '--master',
        action='store_true',
        dest='master',
        default=False,
        help="Set locust to run in distributed mode with this process as master"
    )

    # if locust should be run in distributed mode as slave
    parser.add_option(
        '--slave',
        action='store_true',
        dest='slave',
        default=False,
        help="Run in distributed mode with this process as slave"
    )
    
    # master host options
    parser.add_option(
        '--master-host',
        action='store',
        type='str',
        dest='master_host',
        default="127.0.0.1",
        help="Host or IP address of locust master for distributed load testing. Only used when running with --slave. Defaults to 127.0.0.1."
    )
    
    parser.add_option(
        '--master-port',
        action='store',
        type='int',
        dest='master_port',
        default=6666,
        help="The port to connect to that is used by the locust master for distributed load testing. Only used when running with --slave. Defaults to 5557. Note that slaves will also connect to the master node on this port + 1."
    )

    parser.add_option(
        '--master-bind-host',
        action='store',
        type='str',
        dest='master_bind_host',
        default="*",
        help="Interfaces (hostname, ip) that locust master should bind to. Only used when running with --master. Defaults to * (all available interfaces)."
    )
    
    parser.add_option(
        '--master-bind-port',
        action='store',
        type='int',
        dest='master_bind_port',
        default=6667,
        help="Port that locust master should bind to. Only used when running with --master. Defaults to 5557. Note that Locust will also use this port + 1, so by default the master node will bind to 5557 and 5558."
    )
    opts, args = parser.parse_args()
    return parser, opts, args

def main():
    '''func doc'''
    parser, options, arguments = parse_options()
    if not options.master and not options.slave:
        data_runners.global_runner = LocalRunner()
    elif options.master:
        data_runners.global_runner = MasterRunner()
    elif options.slave:
        logger.error("start init slave")
        data_runners.global_runner = SlaveRunner()
        logger.info("init success!")
    
    def handle_sig_term():
        global_runner.state = STATE_STOPPED
        logger.info("stop all threads!")
    signal.signal(signal.SIGTERM, handle_sig_term)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        logger.info("client quit!")
