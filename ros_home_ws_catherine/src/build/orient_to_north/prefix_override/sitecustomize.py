import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/catherine-maglione/combined_ws/ros_home_ws_catherine/src/install/orient_to_north'
