import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/catherine-maglione/ros_home_ws_catherine/install/orient_to_north'