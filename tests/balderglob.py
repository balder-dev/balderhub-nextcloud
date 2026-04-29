import logging
from balderplugin.junit import JunitPlugin


logging.basicConfig(format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', level=logging.DEBUG)
logging.getLogger('selenium').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)