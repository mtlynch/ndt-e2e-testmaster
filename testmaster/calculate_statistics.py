#!/usr/bin/python
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
"""Calculates aggregate statistics from a set of NDT result files.

Given a pattern of files, finds the NDT result files (JSON) or result packages
(zips of JSON) and parses their contents to dump out aggregate statistics on
each each metric.
"""

import argparse
import csv
import glob
import io
import logging

import read_results
import result_statistics


def print_simple(stats):
    for metric in sorted(stats.keys()):
        metric_stats = stats[metric]
        print metric
        print '    Minimum: %.1f' % metric_stats.minimum
        print '    Maximum: %.1f' % metric_stats.maximum
        print '    Mean:    %.1f' % metric_stats.mean
        print '    Median:  %.1f' % metric_stats.median
        print '    StdDev:  %.3f' % metric_stats.standard_deviation
        print '    Samples: %d' % metric_stats.sample_count


def print_csv(stats):
    output = io.BytesIO()
    fields = ['Metric', 'Minimum', 'Maximum', 'Mean', 'Median', 'StdDev']
    csv_file = csv.DictWriter(output, fieldnames=fields)
    csv_file.writeheader()
    for metric, metric_stats in stats.iteritems():
        csv_file.writerow({
            'Metric': metric,
            'Minimum': metric_stats.minimum,
            'Maximum': metric_stats.maximum,
            'Mean': metric_stats.mean,
            'Median': metric_stats.median,
            'StdDev': metric_stats.standard_deviation,
            'Samples': metric_stats.sample_count,
        })
    print output.getvalue()


def print_statistics(stats, output_format):
    if output_format == 'simple':
        print_simple(stats)
    elif output_format == 'csv':
        print_csv(stats)
    else:
        raise ValueError('Invalid output format: %s' % output_format)


def main(args):
    matching_files = glob.glob(args.pattern)
    if not matching_files:
        logging.error('No files matched pattern %s', args.pattern)
        return
    results = read_results.parse_files(matching_files)
    stats = result_statistics.calculate_statistics(results)
    print_statistics(stats, args.format)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='NDT Result Aggregate Statistic Calculator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--pattern',
                        required=True,
                        help='Glob pattern of input files')
    parser.add_argument('--format',
                        choices=('simple', 'csv'),
                        default='simple',
                        help='Output format')
    main(parser.parse_args())
