import os
import zipfile

from ndt_e2e_clientworker.client_wrapper import result_decoder


def parse_files(result_filenames):
    """Parses a list of files for the NDT results they contain.

    Reads a list of raw files and/or result file packages and parses their
    contents into NdtResult instances. Any non-result files in the list or
    within specified packages are ignored.

    Note that if multiple files in the list have the same basename, but
    different contents results are undefined.

    Args:
        result_filenames: A list of filenames to parse for results. These may
            be a combination of raw results (JSON files) and result packages
            (a compressed archive of raw results).

    Returns:
        A dictionary of NdtResult instances, keyed by filename (only the
        basename).
    """
    result_files = _read_result_files(result_filenames)
    return _decode_results(result_files)


def _is_raw_result(filename):
    return os.path.splitext(filename)[1] == '.json'


def _is_result_package(filename):
    return zipfile.is_zipfile(filename)


def _read_results_from_package(result_package_filename):
    """Loads the raw contents of each result file in a result package.

    Opens a result package file and, for each raw result file in the package,
    reads the raw, decompressed contents of the file into memory. Any filenames
    in the package that are not result files are ignored.

    Args:
        result_package_filename: Filename of result package from which to read
            file contents.

    Returns:
        A dictionary where each key is a file basename and the value is a string
        containing the contents of the corresponding file.
    """
    results = {}
    with zipfile.ZipFile(result_package_filename) as result_package:
        for filename in result_package.namelist():
            if not _is_raw_result(filename):
                continue
            results[os.path.basename(filename)] = result_package.read(filename)
    return results


def _read_result_files(result_filenames):
    """Loads the raw contents of each result file in result files and packages.

    Given a list of filenames, finds files that looks like either a raw NDT
    result file or a package of NDT result files. For raw files, we read the
    file contents into memory directly. For result packages, we open the package
    and read the contents of each raw result file in the package into memory. We
    return the results in a dictionary mapping filenames to file contents.

    Args:
        result_filenames: A list of filenames to parse for results. These may
            be a combination of raw results (JSON files) and result packages
            (a compressed archive of raw results).

    Returns:
        A dictionary where each key is a file basename and the value is a string
        containing the contents of the corresponding file.
    """
    result_files = {}
    for filename in result_filenames:
        if _is_raw_result(filename):
            with open(filename) as result_file:
                result_files[os.path.basename(filename)] = result_file.read()
        elif _is_result_package(filename):
            result_files.update(_read_results_from_package(filename))
    return result_files


def _decode_results(result_files):
    """Converts a dictionary of raw strings into a dictionary of parsed results.

    Given a dictionary of filenames -> file content strings, parses the a
    content strings to produce a dictionary of filenames -> NdtResult objects.

    Args:
        result_files: A dictionary of raw strings to parse into NdtResult
            objects, keyed by their original filename.

    Returns:
        A dictionary of NdtResult objects, keyed by the name of the file from
        which they were parsed.
    """
    results = {}
    decoder = result_decoder.NdtResultDecoder()
    for filename, raw_contents in result_files.iteritems():
        results[filename] = decoder.decode(raw_contents)
    return results
