# coding:utf-8


import os
import time
import logging.handlers


class Glogger:

    logger = None

    levels = {"n": logging.NOTSET,
              "d": logging.DEBUG,
              "i": logging.INFO,
              "w": logging.WARN,
              "e": logging.ERROR,
              "c": logging.CRITICAL}

    log_level = "n"
    log_suffix = time.strftime("%Y%m%d", time.localtime())
#     log_name = "italk_runner_" + str(os.getpid()) + ".log"
    log_name = "deploy" + log_suffix + ".log"
    log_dir = "log"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_file = os.path.join(log_dir, log_name)
    log_max_byte = 10 * 1024 * 1024
    log_backup_count = 5

    @staticmethod
    def getLogger():
        if Glogger.logger is not None:
            return Glogger.logger
        Glogger.logger = logging.Logger("oggingmodule.Glogger")
        log_handler = logging.handlers.RotatingFileHandler(
            filename=Glogger.log_file,
            maxBytes=Glogger.log_max_byte,
            backupCount=Glogger.log_backup_count
        )
        log_fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        log_handler.setFormatter(log_fmt)
        Glogger.logger.addHandler(log_handler)
        Glogger.logger.setLevel(Glogger.levels.get(Glogger.log_level))
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)
        Glogger.logger.addHandler(consoleHandler)
        return Glogger.logger
    
    
if __name__ == '__main__':
    logger = Glogger.getLogger()
    logger.info('TEST!!!')

