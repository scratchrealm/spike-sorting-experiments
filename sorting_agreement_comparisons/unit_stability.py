import numpy as np
import protocaas.client as prc
import spikeinterface as si
from common import load_sorting, _get_spike_train_agreement


project_id = '4b4d3486'

# kilosort3 first 40 minutes
sorting1_path = 'generated/000409/sub-CSH-ZAD-001/sub-CSH-ZAD-001_ses-3e7ae7c0-fe8b-487c-9354-036236fa1010_behavior+ecephys+image_desc-kilosort3-keepall.nwb'

# kilosort3 entire session
sorting2_path = 'generated/000409/sub-CSH-ZAD-001/sub-CSH-ZAD-001_ses-3e7ae7c0-fe8b-487c-9354-036236fa1010_behavior+ecephys+image_desc-kilosort3-40min.nwb'

def main():
    # Load project "test slurm compute resource"
    project = prc.load_project(project_id)
    
    sorting1: si.BaseSorting = load_sorting(project, sorting1_path)
    sorting2: si.BaseSorting = load_sorting(project, sorting2_path)

    start_time_frame = min(sorting1.start_time_frame, sorting2.start_time_frame)
    end_time_frame = max(sorting1.end_time_frame, sorting2.end_time_frame)

    compare_sortings(sorting1, sorting2, start_time_frame=start_time_frame, end_time_frame=end_time_frame)

def compare_sortings(sorting1: si.BaseSorting, sorting2: si.BaseSorting, *, start_time_frame: int, end_time_frame: int):
    unit_ids_1 = sorting1.get_unit_ids()
    unit_ids_2 = sorting2.get_unit_ids()

    print(f'Number of units: {len(unit_ids_1)}, {len(unit_ids_2)}')

    agreement_matrix = np.zeros((len(unit_ids_1), len(unit_ids_2)), dtype=np.float32)
    for ii1, unit_id_1 in enumerate(unit_ids_1):
        print(f'Unit {ii1 + 1} of {len(unit_ids_1)}')
        for ii2, unit_id_2 in enumerate(unit_ids_2):
            st1 = sorting1.get_unit_spike_train(unit_id_1)
            st2 = sorting2.get_unit_spike_train(unit_id_2)
            st1 = st1[(st1 >= start_time_frame) & (st1 < end_time_frame)]
            st2 = st2[(st2 >= start_time_frame) & (st2 < end_time_frame)]
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

if __name__ == '__main__':
    main()