# -*- coding: UTF-8 -*-
import logging
import os

logging.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'), level=logging.WARN, filemode='w',
                    format='%(asctime)s - %(levelname)s: %(message)s')
logging.debug('debug')
logging.warning('warn')
