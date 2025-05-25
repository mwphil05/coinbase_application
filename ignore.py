"""
file to get rid of warning from openssl lib
"""
import warnings
warnings.filterwarnings("ignore", module="urllib3")
