# post-processing range/consistency check algorithm for post_process_id = 1

import workflow_methods_master as methods
import config


def r1(value):
    value = methods.pressure_range(value)