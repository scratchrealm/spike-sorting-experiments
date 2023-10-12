# Concerning the limited accuracy of widely-used spike sorters

While directly assessing the accuracy of spike sorting proves challenging without ground-truth firing data for reference, it is possible to estimate an upper bound on the accuracy level for a specific algorithm applied to a particular dataset. This can be achieved by evaluating the algorithm's stability, or self-consistency, by executing the algorithm repeatedly on the identical dataset and then contrasting the outcomes. However, to ensure variety in the case of a deterministic method, the algorithm isn't run in the same manner every time. Initially, it is run on the entire dataset, followed by a separate run on the dataset's first half. The two results from the first half of the data are then compared.

https://dandiarchive.org/dandiset/000409

https://viz.internationalbrainlab.org/app

https://protocaas.vercel.app/project/0be4a197?tab=project-files

## NYU-37 83d85891-bd75-4557-91b4-1cbb5f8bfc9d

* DOB	2020-08-31
* Lab	angelakilab
* N clusters	173 good, 1347 overall
* N spikes	4113991
* N trials	443
* Probe name	probe00
* Probe type	3B2
* Recording date	2021-01-27
* Recording length	53 minutes
* Subject	NYU-37
* dset_bwm	true
* dset_rs	false
* eid	83d85891-bd75-4557-91b4-1cbb5f8bfc9d
* pid	16ad5eef-3fa6-4c75-9296-29bf40c5cfaa



## 	CSHL059 37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0

* DOB	2019-10-15
* Lab	churchlandlab
* N clusters	45 good, 457 overall
* N spikes	1547039
* N trials	630
* Probe name	probe01
* Probe type	3A
* Recording date	2020-03-08
* Recording length	72 minutes
* Subject	CSHL059
* dset_bwm	true
* dset_rs	false
* eid	37e96d0b-5b4b-4c6e-9b29-7edbdc94bbd0
* pid	50f1512d-dd41-4a0c-b3ab-b0564f0424d7