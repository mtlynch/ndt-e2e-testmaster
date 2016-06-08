# Copyright 2016 Measurement Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Provides a set of functions to calculate metrics for NDT results."""


def total_duration(result):
    """Calculates the total duration of an NDT result (in seconds).

    Args:
        result: An NdtResult instance.

    Returns:
        The total duration of the NDT result in seconds or None if the NDT test
        did not complete.
    """
    return _calculate_duration(result)


def c2s_duration(result):
    """Calculates the duration of the c2s test of an NDT result (in seconds).

    Args:
        result: An NdtResult instance.

    Returns:
        The duration of the NDT c2s test in seconds or None if the c2s test did
        not complete.
    """
    return _calculate_duration(result.c2s_result)


def s2c_duration(result):
    """Calculates the duration of the s2c test of an NDT result (in seconds).

    Args:
        result: An NdtResult instance.

    Returns:
        The duration of the NDT s2c test in seconds or None if the s2c test did
        not complete.
    """
    return _calculate_duration(result.s2c_result)


def _calculate_duration(event):
    """Calculates the duration of an event in seconds.

    Args:
        event: An object that has start_time and end_time properties that
            return datetime objects.

    Returns:
        The total duration of event in seconds.
    """
    if not event.start_time or not event.end_time:
        return None
    return (event.end_time - event.start_time).total_seconds()
