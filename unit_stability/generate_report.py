import json


project_id = '0be4a197'

def main():
    aa = [
        {'session_name': 'NYU-37', 'name1': 'kilosort3', 'name2': 'kilosort3-30min'},
        {'session_name': 'NYU-37', 'name1': 'kilosort2_5', 'name2': 'kilosort2_5-30min'},
        {'session_name': 'NYU-37', 'name1': 'mountainsort5', 'name2': 'mountainsort5-30min'},
        {'session_name': 'NYU-37', 'name1': 'kilosort3', 'name2': 'mountainsort5'},
        {'session_name': 'NYU-37', 'name1': 'kilosort2_5', 'name2': 'mountainsort5'},
        {'session_name': 'NYU-37', 'name1': 'kilosort3', 'name2': 'kilosort2_5'},
        {'session_name': 'CSHL059', 'name1': 'kilosort3', 'name2': 'kilosort3-30min'},
        {'session_name': 'CSHL059', 'name1': 'kilosort2_5', 'name2': 'kilosort2_5-30min'},
        {'session_name': 'CSHL059', 'name1': 'mountainsort5', 'name2': 'mountainsort5-30min'},
        {'session_name': 'CSHL059', 'name1': 'kilosort3', 'name2': 'mountainsort5'},
        {'session_name': 'CSHL059', 'name1': 'kilosort2_5', 'name2': 'mountainsort5'},
        {'session_name': 'CSHL059', 'name1': 'kilosort3', 'name2': 'kilosort2_5'},
    ]

    report = ''
    report2 = '''
|Session|Comparison|Number of units with agreement > 70%|
|-------|----------|-------------------------------------|
'''
    for a in aa:
        md1, md2 = generate_report(project_id, a['session_name'], a['name1'], a['name2'])
        report += md1
        report2 += md2
    
    md = report2 + '\n\n' + report
    with open('report.md', 'w') as f:
        f.write(md)

def generate_report(
    project_id: str,
    session_name: str,
    name1: str,
    name2: str
):
    fname = f'{session_name}_{name1}_vs_{name2}.json'
    with open(fname, 'r') as f:
        data = json.load(f)
    md = f'''
<hr />

# {session_name} {name1} vs {name2}

|Unit Index|Best agreement|Unit ID|Best Match ID|
|----------|--------------|-------|-------------|
'''
    num_units_with_high_agreement = 0
    for ii, unit in enumerate(data['units']):
        unit_id = unit['unit_id']
        best_agreement = unit['best_agreement']
        best_match = unit['best_match']
        if best_agreement < 0.7:
            continue
        num_units_with_high_agreement += 1
        best_agreement_pct = int(best_agreement * 1000) / 10
        md += f'|{ii + 1}|{best_agreement_pct}%|{unit_id}|{best_match}|\n'
    md2 = f'|{session_name}|{name1} vs {name2}|{num_units_with_high_agreement}|\n'
    return md, md2

# def _get_path(project_id: str, name: str, session_name: str):
#     if session_name == 'NYU-37':
#         session_str = '83d85891-bd75-4557-91b4-1cbb5f8bfc9d_behavior+ecephys+image'
#     elif session_name == 'CSHL059':
#         session_str = '37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0_behavior+ecephys+image'
#     return f'generated/{project_id}/sub-{session_name}/sub-CSHL059_ses-{session_str}_desc-{name}.nwb''

if __name__ == '__main__':
    main()