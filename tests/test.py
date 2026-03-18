import sys
import os
import unittest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from datetime import datetime, timedelta
from src import *


class TestVersion(unittest.TestCase):
  """Test cases for the Version class."""


if __name__ == '__main__':
  unittest.main()