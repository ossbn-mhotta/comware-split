''' pythonでバッチスクリプトを書くときの雛形 https://qiita.com/fetaro/items/77cb5571c472eac85031
'''
import logging
import os
import sys
from pathlib import Path

import click

# set parent directory to application home(${app_home})
app_home = str(Path(__file__).parents[1])
# add ${app_home} to the library load path
sys.path.append(app_home)

# load self-created libraries
from lib.my_lib import MyLib

# load configuration class
from conf.my_batch_conf import MyBatchConf

# handle command line arguments.
@click.command()
@click.argument('filepath')
@click.option('--verbose', '-v', is_flag=True, default=False)
@click.option('--verbose2', '-vv', is_flag=True, default=False)
def cli(filepath, verbose, verbose2):
    # remove extention from this source filename and make it to program name(${prog_name})
    prog_name = os.path.splitext(os.path.basename(__file__))[0]

    # set logger
    # format
    log_format = logging.Formatter("%(asctime)s [%(levelname)8s] %(message)s")
    # level
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # handler to log file
    file_handler = logging.FileHandler(os.path.join(app_home, "log", prog_name + ".log"), "a+")
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    # handler to stdout
    # stdout_handler = logging.StreamHandler(sys.stdout)
    # stdout_handler.setFormatter(log_format)
    # logger.addHandler(stdout_handler)

    # start from here
    try:
        logger.info("start")        # log output

        # use command line arguments
        logger.info(f"filepath = {filepath}")
        logger.info(f"verbose = {verbose}")
        logger.info(f"verbose2 = {verbose2}")

        # call libraries
        mylib = MyLib(verbose, verbose2)
        logger.info(mylib.get_name())
        mylib.read_file(filepath)

        # use configuration settings
#       logger.info(MyBatchConf.textfile)
#       logger.info(MyBatchConf.key2)

        # if an exception occurs,
#       raise Exception("My Exception")

    except Exception as e:
        # catch an exception and record to log
        logger.exception(e)
        sys.exit(1)

if __name__ == '__main__':
    cli()
