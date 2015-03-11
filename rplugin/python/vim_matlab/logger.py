import logging
import os

log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'vim-matlab.log')

log_format = '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d in ' \
             '%(funcName)s, pid %(process)s (%(processName)s):\n%(message)s\n'

logging.basicConfig(filename=log_path, level=logging.INFO, format=log_format)
log = logging.getLogger('')