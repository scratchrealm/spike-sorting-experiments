import os
import json
import time
import numpy as np
import protocaas.client as prc
import spikeinterface as si
from NwbSorting import NwbSorting
from common import load_sorting, _get_spike_train_agreement


project_id = '0be4a197'

def main():
    # NYU-37 kilosort3
    path1 = 'generated/000409/sub-NYU-37/sub-NYU-37_ses-83d85891-bd75-4557-91b4-1cbb5f8bfc9d_behavior+ecephys+image_desc-kilosort3.nwb'
    path2 = 'generated/000409/sub-NYU-37/sub-NYU-37_ses-83d85891-bd75-4557-91b4-1cbb5f8bfc9d_behavior+ecephys+image_desc-kilosort3-30min.nwb'
    output_fname = 'NYU-37_kilosort3_comparison.json'
    do_comparison(
        project_id=project_id,
        path1=path1,
        path2=path2,
        output_fname=output_fname
    )

    # NYU-37 kilosort2_5
    path1 = 'generated/000409/sub-NYU-37/sub-NYU-37_ses-83d85891-bd75-4557-91b4-1cbb5f8bfc9d_behavior+ecephys+image_desc-kilosort2-5.nwb'
    path2 = 'generated/000409/sub-NYU-37/sub-NYU-37_ses-83d85891-bd75-4557-91b4-1cbb5f8bfc9d_behavior+ecephys+image_desc-kilosort2-5-30min.nwb'
    output_fname = 'NYU-37_kilosort2_5_comparison.json'
    do_comparison(
        project_id=project_id,
        path1=path1,
        path2=path2,
        output_fname=output_fname
    )

    # NYU-37 mountainsort5
    path1 = 'generated/000409/sub-NYU-37/sub-NYU-37_ses-83d85891-bd75-4557-91b4-1cbb5f8bfc9d_behavior+ecephys+image_desc-mountainsort5.nwb'
    path2 = 'generated/000409/sub-NYU-37/sub-NYU-37_ses-83d85891-bd75-4557-91b4-1cbb5f8bfc9d_behavior+ecephys+image_desc-mountainsort5-30min.nwb'
    output_fname = 'NYU-37_mountainsort5_comparison.json'
    do_comparison(
        project_id=project_id,
        path1=path1,
        path2=path2,
        output_fname=output_fname
    )

    # CSHL059 kilosort3
    path1 = 'generated/000409/sub-CSHL059/sub-CSHL059_ses-37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0_behavior+ecephys+image_desc-kilosort3.nwb'
    path2 = 'generated/000409/sub-CSHL059/sub-CSHL059_ses-37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0_behavior+ecephys+image_desc-kilosort3-30min.nwb'
    output_fname = 'CSHL059_kilosort3_comparison.json'
    do_comparison(
        project_id=project_id,
        path1=path1,
        path2=path2,
        output_fname=output_fname
    )

    # CSHL059 kilosort2_5
    path1 = 'generated/000409/sub-CSHL059/sub-CSHL059_ses-37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0_behavior+ecephys+image_desc-kilosort2-5.nwb'
    path2 = 'generated/000409/sub-CSHL059/sub-CSHL059_ses-37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0_behavior+ecephys+image_desc-kilosort2-5-30min.nwb'
    output_fname = 'CSHL059_kilosort2_5_comparison.json'
    do_comparison(
        project_id=project_id,
        path1=path1,
        path2=path2,
        output_fname=output_fname
    )

    # CSHL059 mountainsort5
    path1 = 'generated/000409/sub-CSHL059/sub-CSHL059_ses-37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0_behavior+ecephys+image_desc-mountainsort5.nwb'
    path2 = 'generated/000409/sub-CSHL059/sub-CSHL059_ses-37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0_behavior+ecephys+image_desc-mountainsort5-30min.nwb'
    output_fname = 'CSHL059_mountainsort5_comparison.json'
    do_comparison(
        project_id=project_id,
        path1=path1,
        path2=path2,
        output_fname=output_fname
    )

    # NYU-37 kilosort3 vs kilosort2_5
    path1 = 'generated/000409/sub-NYU-37/sub-NYU-37_ses-83d85891-bd75-4557-91b4-1cbb5f8bfc9d_behavior+ecephys+image_desc-kilosort3.nwb'
    path2 = 'generated/000409/sub-NYU-37/sub-NYU-37_ses-83d85891-bd75-4557-91b4-1cbb5f8bfc9d_behavior+ecephys+image_desc-kilosort2-5.nwb'
    output_fname = 'NYU-37_kilosort3_vs_kilosort2_5_comparison.json'
    do_comparison(
        project_id=project_id,
        path1=path1,
        path2=path2,
        output_fname=output_fname
    )

    # NYU-37 kilosort3 vs mountainsort5
    path1 = 'generated/000409/sub-NYU-37/sub-NYU-37_ses-83d85891-bd75-4557-91b4-1cbb5f8bfc9d_behavior+ecephys+image_desc-kilosort3.nwb'
    path2 = 'generated/000409/sub-NYU-37/sub-NYU-37_ses-83d85891-bd75-4557-91b4-1cbb5f8bfc9d_behavior+ecephys+image_desc-mountainsort5.nwb'
    output_fname = 'NYU-37_kilosort3_vs_mountainsort5_comparison.json'
    do_comparison(
        project_id=project_id,
        path1=path1,
        path2=path2,
        output_fname=output_fname
    )

    # NYU-37 kilosort2_5 vs mountainsort5
    path1 = 'generated/000409/sub-NYU-37/sub-NYU-37_ses-83d85891-bd75-4557-91b4-1cbb5f8bfc9d_behavior+ecephys+image_desc-kilosort2-5.nwb'
    path2 = 'generated/000409/sub-NYU-37/sub-NYU-37_ses-83d85891-bd75-4557-91b4-1cbb5f8bfc9d_behavior+ecephys+image_desc-mountainsort5.nwb'
    output_fname = 'NYU-37_kilosort2_5_vs_mountainsort5_comparison.json'
    do_comparison(
        project_id=project_id,
        path1=path1,
        path2=path2,
        output_fname=output_fname
    )

    # CHSL059 kilosort3 vs kilosort2_5
    path1 = 'generated/000409/sub-CSHL059/sub-CSHL059_ses-37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0_behavior+ecephys+image_desc-kilosort3.nwb'
    path2 = 'generated/000409/sub-CSHL059/sub-CSHL059_ses-37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0_behavior+ecephys+image_desc-kilosort2-5.nwb'
    output_fname = 'CSHL059_kilosort3_vs_kilosort2_5_comparison.json'
    do_comparison(
        project_id=project_id,
        path1=path1,
        path2=path2,
        output_fname=output_fname
    )

    # CHSL059 kilosort3 vs mountainsort5
    path1 = 'generated/000409/sub-CSHL059/sub-CSHL059_ses-37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0_behavior+ecephys+image_desc-kilosort3.nwb'
    path2 = 'generated/000409/sub-CSHL059/sub-CSHL059_ses-37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0_behavior+ecephys+image_desc-mountainsort5.nwb'
    output_fname = 'CSHL059_kilosort3_vs_mountainsort5_comparison.json'
    do_comparison(
        project_id=project_id,
        path1=path1,
        path2=path2,
        output_fname=output_fname
    )

    # CHSL059 kilosort2_5 vs mountainsort5
    path1 = 'generated/000409/sub-CSHL059/sub-CSHL059_ses-37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0_behavior+ecephys+image_desc-kilosort2-5.nwb'
    path2 = 'generated/000409/sub-CSHL059/sub-CSHL059_ses-37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0_behavior+ecephys+image_desc-mountainsort5.nwb'
    output_fname = 'CSHL059_kilosort2_5_vs_mountainsort5_comparison.json'
    do_comparison(
        project_id=project_id,
        path1=path1,
        path2=path2,
        output_fname=output_fname
    )

def do_comparison(*,
    project_id: str,
    path1: str,
    path2: str,
    output_fname: str
):
    if os.path.exists(output_fname):
        print(f'Output file already exists: {output_fname}')
        return

    print('')
    print('')
    print(f'Comparison: {path1} vs {path2}')

    # Load project "test slurm compute resource"
    project = prc.load_project(project_id)
    
    sorting1: NwbSorting = load_sorting(project, path1)
    sorting2: NwbSorting = load_sorting(project, path2)

    start_time_frame = min(sorting1.start_time_frame, sorting2.start_time_frame)
    end_time_frame = max(sorting1.end_time_frame, sorting2.end_time_frame)

    compare_sortings(
        sorting1,
        sorting2,
        start_time_frame=start_time_frame,
        end_time_frame=end_time_frame,
        output_fname=output_fname
    )

def compare_sortings(
    sorting1: si.BaseSorting,
    sorting2: si.BaseSorting, *,
    start_time_frame: int,
    end_time_frame: int,
    output_fname: str
):
    unit_ids_1 = sorting1.get_unit_ids()
    unit_ids_2 = sorting2.get_unit_ids()

    print(f'Number of units: {len(unit_ids_1)}, {len(unit_ids_2)}')

    agreement_matrix = np.zeros((len(unit_ids_1), len(unit_ids_2)), dtype=np.float32)
    timer = time.time()
    for ii1, unit_id_1 in enumerate(unit_ids_1):
        elapsed = time.time() - timer
        if elapsed > 5:
            print(f'Unit {ii1 + 1} of {len(unit_ids_1)}')
            timer = time.time()
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
    sorted_best_agreements = best_agreements[order]
    sorted_unit_ids_1 = unit_ids_1[order]
    sorted_best_matches = np.array(best_matches)[order]

    print('Top 50 best agreements:')
    for ii, best_agreement in enumerate(sorted_best_agreements[0:50]):
        print(f'{ii + 1}: {best_agreement} [{sorted_unit_ids_1[ii]} -> {sorted_best_matches[ii]}]')
    
    x = {
        'units': [
            {
                'unit_id': int(sorted_unit_ids_1[ii]),
                'best_agreement': float(sorted_best_agreements[ii]),
                'best_match': int(sorted_best_matches[ii])
            }
            for ii in range(len(sorted_unit_ids_1))
        ]
    }

    with open(output_fname, 'w') as f:
        json.dump(x, f, indent=4)

if __name__ == '__main__':
    main()