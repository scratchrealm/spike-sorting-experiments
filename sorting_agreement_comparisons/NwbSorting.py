import numpy as np
import h5py
import spikeinterface as si


def NwbSorting(file: h5py.File) -> None:
    # Load unit IDs
    ids = file['units']['id'][:]

    # Load spike times index
    spike_times_index = file['units']['spike_times_index'][:]

    # Load spike times
    spike_times = file['units']['spike_times'][:]

    units_dict = {}
    sampling_frequency = 30000 # TODO: get this from the NWB file
    for i in range(len(ids)):
        if i == 0:
            s = spike_times[0:spike_times_index[0]]
        else:
            s = spike_times[spike_times_index[i - 1]:spike_times_index[i]]
        units_dict[ids[i]] = (s * sampling_frequency).astype(np.int32)
    
    try:
        # different versions of spikeinterface
        sorting = si.NumpySorting.from_dict(
            [units_dict], sampling_frequency=sampling_frequency
        )
    except:
        sorting = si.NumpySorting.from_unit_dict(
            [units_dict], sampling_frequency=sampling_frequency
        )
    return sorting