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

import argparse
import glob

import csv_convert
import read_results


def main(args):
    results = read_results.parse_files(glob.glob(args.pattern))
    print csv_convert.ndt_results_to_csv(results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='NDT Result JSON to CSV converter',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--pattern',
                        required=True,
                        help="Glob pattern of input files")
    main(parser.parse_args())