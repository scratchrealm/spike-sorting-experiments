import h5py
import numpy as np
import spikeinterface as si
import protocaas.client as prc
import remfile
from NwbSorting import NwbSorting

def main():
    # Load project "test slurm compute resource"
    project = prc.load_project('4b4d3486')
    
    sorting1 = load_sorting(project, 'generated/000409/sub-CSH-ZAD-001/sub-CSH-ZAD-001_ses-3e7ae7c0-fe8b-487c-9354-036236fa1010_behavior+ecephys+image_desc-mountainsort5-10min-training100-b.nwb')
    sorting2 = load_sorting(project, 'generated/000409/sub-CSH-ZAD-001/sub-CSH-ZAD-001_ses-3e7ae7c0-fe8b-487c-9354-036236fa1010_behavior+ecephys+image_desc-mountainsort5-20min-training100.nwb')

    # sorting1 = load_sorting(project, 'generated/000409/sub-CSH-ZAD-001/sub-CSH-ZAD-001_ses-3e7ae7c0-fe8b-487c-9354-036236fa1010_behavior+ecephys+image_desc-kilosort3-20min.nwb')
    # sorting1 = load_sorting(project, 'generated/000409/sub-CSH-ZAD-001/sub-CSH-ZAD-001_ses-3e7ae7c0-fe8b-487c-9354-036236fa1010_behavior+ecephys+image_desc-kilosort3-keepall.nwb')

    # sorting2 = load_sorting(project, 'generated/000409/sub-CSH-ZAD-001/sub-CSH-ZAD-001_ses-3e7ae7c0-fe8b-487c-9354-036236fa1010_behavior+ecephys+image_desc-kilosort3.nwb')

    unit_ids_1 = sorting1.get_unit_ids()
    unit_ids_2 = sorting2.get_unit_ids()

    print(f'Number of units: {len(unit_ids_1)}, {len(unit_ids_2)}')

    agreement_matrix = np.zeros((len(unit_ids_1), len(unit_ids_2)), dtype=np.float32)
    for ii1, unit_id_1 in enumerate(unit_ids_1):
        print(f'Unit {ii1 + 1} of {len(unit_ids_1)}')
        for ii2, unit_id_2 in enumerate(unit_ids_2):
            st1 = sorting1.get_unit_spike_train(unit_id_1)
            st2 = sorting2.get_unit_spike_train(unit_id_2)

            st2 = st2[st2 < 10 * 60 * sorting2.get_sampling_frequency()] # only compare first portion
            
            agreement = _get_spike_train_agreement(st1, st2)
            agreement_matrix[ii1, ii2] = agreement
    
    best_agreements = []
    best_matches = []
    for ii1, unit_id_1 in enumerate(unit_ids_1):
        best_agreement = np.max(agreement_matrix[ii1, :])
        best_match = np.argmax(agreement_matrix[ii1, :])
        best_agreements.append(best_agreement)
        best_matches.append(unit_ids_2[best_match])
    
    # Sort best_agreement in descending order
    best_agreements = np.array(best_agreements)
    order = np.argsort(best_agreements)[::-1]
    best_agreements = best_agreements[order]
    sorted_unit_ids_1 = unit_ids_1[order]
    sorted_best_matches = np.array(best_matches)[order]

    # Print best agreements
    print('Best agreements:')
    for ii, best_agreement in enumerate(best_agreements):
        print(f'{ii + 1}: {best_agreement} [{sorted_unit_ids_1[ii]} -> {sorted_best_matches[ii]}]')

    

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

def _unit_test_spike_train_agreement():
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

if __name__ == "__main__":
    _unit_test_spike_train_agreement()
    main()