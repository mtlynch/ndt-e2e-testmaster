# NDT End-to-End TestMaster

[![Build
Status](https://travis-ci.org/m-lab/ndt-e2e-testmaster.svg?branch=master)](https://travis-ci.org/m-lab/ndt-e2e-testmaster)
[![Coverage
Status](https://coveralls.io/repos/m-lab/ndt-e2e-testmaster/badge.svg?branch=master&service=github)](https://coveralls.io/github/m-lab/ndt-e2e-testmaster?branch=master)

## Utilities

### JSON to CSV converter

The JSON to CSV converter takes a collection of raw NDT result JSON files
(created by the
[client\_wrapper](https://github.com/m-lab/ndt-e2e-clientworker)) and/or a
collection of NDT result file packages (created by the [Ansible
playbook](https://github.com/m-lab/ndt-e2e-ansible)) and gathers the results
together in a CSV file.

To run the converter:

```bash
python testmaster/json_to_csv.py --pattern "ndt-results/*" > results.csv
```

Where `ndt-results` is a folder containing raw JSON results, zips of results, or
both.

### Result Aggregate Statistics Calculator

The aggregate statistics calculator calculates the aggregate statistics of each
metric in the NDT results.

##### Print metric statistics in simple text format

```bash
python testmaster/calculate_statistics.py \
  --pattern "ndt-results/*" \
  --format=simple
```

##### Write metric statistics in CSV format

```bash
python testmaster/calculate_statistics.py \
  --pattern "ndt-results/*" \
  --format=csv > results.csv
```
