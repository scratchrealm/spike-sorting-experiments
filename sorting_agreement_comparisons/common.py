import numpy as np
import h5py
import remfile
import spikeinterface as si
import protocaas.client as prc
from NwbSorting import NwbSorting


def _get_spike_train_agreement(st1: np.ndarray, st2: np.ndarray, tol=15) -> float:
    # Create labels and sort by times
    labels = np.zeros(len(st1) + len(st2), dtype=np.int32)
    labels[0:len(st1)] = 1
    labels[len(st1):] = 2
    times = np.concatenate((st1, st2))
    order = np.argsort(times)
    labels = labels[order]
    times = times[order]

    # Find matches within tolerance for 1 coming before 2
    diffs = np.diff(times)
    match_count = 0
    inds_where_label_one_is_before_label_two_within_tolerance = np.where((labels[0:-1] == 1) & (labels[1:] == 2) & (diffs <= tol))[0]
    match_count += len(inds_where_label_one_is_before_label_two_within_tolerance)
    
    # now delete these before we test in the other direction
    labels[inds_where_label_one_is_before_label_two_within_tolerance] = -1
    labels[inds_where_label_one_is_before_label_two_within_tolerance + 1] = -1
    inds_to_delete = np.where(labels == -1)[0]
    labels = np.delete(labels, inds_to_delete)
    times = np.delete(times, inds_to_delete)
    diffs = np.diff(times)

    # Find matches within tolerance for 2 coming before 1
    inds_where_label_two_is_before_label_one_within_tolerance = np.where((labels[0:-1] == 2) & (labels[1:] == 1) & (diffs <= tol))[0]
    match_count += len(inds_where_label_two_is_before_label_one_within_tolerance)

    agreement = match_count / (len(st1) + len(st2) - match_count)
    return agreement

def _test_spike_train_agreement():
    a = _get_spike_train_agreement(np.array([1, 2, 3]), np.array([4, 5, 6]), tol=1)
    assert a == 1 / 5, f'Got {a}'
    a = _get_spike_train_agreement(np.array([1, 2, 3]), np.array([1, 2.5]), tol=1)
    assert a == 2 / 3, f'Got {a}'
    a = _get_spike_train_agreement(np.array([1, 2, 3]), np.array([1, 2.5]), tol=0.2)
    assert a == 1 / 4, f'Got {a}'
    a = _get_spike_train_agreement(np.array([1, 2, 3]), np.array([1, 2.5, 3.1]), tol=0.2)
    assert a == 2 / 4, f'Got {a}'
    a = _get_spike_train_agreement(np.array([1, 2, 3]), np.array([1, 2.5, 3.1, 3.15]), tol=0.2)
    assert a == 2 / 5, f'Got {a}'

def load_sorting(project: prc.Project, path: str) -> si.BaseSorting:
    print(f'Loading sorting: {path}')
    nwb_file = project.get_file(path)
    nwb_url = nwb_file.get_url()
    dc = remfile.DiskCache('/tmp/remfile_cache')
    nwb_remf = remfile.File(nwb_url, disk_cache=dc)
    nwb_h5 = h5py.File(nwb_remf, 'r')
    sorting = NwbSorting(nwb_h5)
    return sorting