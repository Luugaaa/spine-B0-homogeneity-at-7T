---
# Spine B0 homogeneity at 7T: comparison of 3D and slice-wise scanner shimming
*An ING8100 project*
## Background
### Background - Magnetic field inhomogeneities
MRI relies on a uniform main magnetic field (B0) to produce high-quality images. In practice, when a patient is inside the scanner bore, field inhomogeneities appear.
- **Static inhomogeneities** are constant over time and come from magnetic susceptibility differences between adjacent tissues (e.g., air–tissue interfaces at the lungs, throat, and sinuses).

### Background - B0 shimming techniques
Fortunately, shimming, a process that adjusts the currents in a set of conducting coils (or shims), generates additional magnetic fields that compensate for the main field inhomogeneities. There are multiple ways to perform shimming, depending on how many regions of interest (ROIs) are shimmed separately:
- **Volume (3D) shimming** uses one set of shim coefficients for the entire acquisition. It is also called static shimming.
- **Slice-wise (2D) shimming** uses one set of shim coefficients per slice, updated for every slice during the acquisition.

### Background - Limitations of 2D shimming
In practice, 2D shimming should outperform 3D shimming, or at worst perform equally, since the same shim degrees of freedom are used to correct smaller regions (Bréheret A. et al., 2025). However, some acquisitions are incompatible with slice-wise shimming, such as any 3D sequence (e.g., 3D multi-echo GRE). 3D sequences encode the signal from the whole volume at once rather than slice by slice, so slice-wise shimming is not possible. They are nevertheless very useful to obtain a higher SNR, which is important for small ROIs such as the spinal cord.

## Main question
Given that slice-wise shimming cannot be used with 3D sequences, it is important to quantify the difference between 3D shimming and slice-wise shimming in the cervical spinal cord.

![Research Question](https://img.shields.io/badge/Research-Question-brightgreen)  
How large is the difference in B0 field homogeneity after slice-wise shimming compared with volume shimming?


## Methods

### Data
The data is subset of the dataset from the open dataset *spine_fMRI_7T* (D'Astous et al.), available on OpenNeuro under a CC0 license ([ds007067, v4.0.0](https://openneuro.org/datasets/ds007067/versions/4.0.0), doi:10.18112/openneuro.ds007067.v4.0.0) and mirrored on [Borealis](https://demo.borealisdata.ca/dataset.xhtml?persistentId=doi:10.80240/FK2/KRFTCT). 

The B0 field maps were acquired on a Siemens 7T scanner (syngo MR E12) with a 20-channel receive coil for the cervical spine, using a dual-echo 2D gradient-echo field mapping sequence with the following parameters:

| Parameter | Value |
|---|---|
| Echo times (TE1 / TE2) | 2.83 ms / 3.85 ms |
| Repetition time | 329 ms |
| Flip angle | 21° |
| Matrix | 64 × 64 |
| Number of slices | 60 (axial, tilted toward coronal) |
| Voxel size | 3.0 × 3.0 × 2.5 mm³ |
| Multiband factor | 2 |
| Pixel bandwidth | 910 Hz/pixel |

### Dataset Summary

| Dataset | N |
|---|---|
| ds007067 (v4.0.0) | 14 | 

The 14 subjects included are sub-093 to sub-107 (sub-097 is not part of the dataset).


### Spinal cord segmentation
The spinal cord was segmented automatically on the first magnitude image with the contrast-agnostic deep learning model of the Spinal Cord Toolbox. The  mask was then dilated by 2 voxels with a ball-shaped kernel to include the tissue surrounding the cord.(`scripts/create_sc_masks.sh`).

### Shimming simulation
Shimming was simulated with the Shimming Toolbox (D'Astous et al., 2023) using `st_b0shim dynamic` (`scripts/compare_shim.sh`). For each subject, the baseline field map was used both as the input field and as the target, and the spinal cord mask defined the ROI to optimize. Both methods used the same settings, so that the only difference between them is the number of shim regions:
- **Shim system**: scanner coils of order 0 and 1, i.e., the center frequency (f0) and the three linear gradients (x, y, z), for a total of 4 degrees of freedom.
- **Optimizer**: pseudo-inverse (unconstrained least squares).
- **Mask dilation kernel size**: 3.
- **Volume (3D) shimming**: `--slices volume`, a single set of shim coefficients optimized over the whole mask.
- **Slice-wise (2D) shimming**: `--slices auto`, one set of shim coefficients per slice group, the groups being determined automatically from the slice acquisition order (slices excited simultaneously with multiband share the same coefficients).

For each method, Shimming Toolbox outputs the predicted shimmed field map inside the mask (`fieldmap_calculated_shim_masked.nii.gz`) together with the shim coefficients.

### Analysis
B0 homogeneity was quantified with the root mean square error (RMSE) of the field, in Hz, inside the spinal cord ROI (`scripts/analysis.py`). Since the target field is 0 Hz, the RMSE measures how far the remaining field is from a perfectly homogeneous field(0 everywhere):

$$\text{RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^{N} \Delta B_{0,i}^2}$$

where $N$ is the number of voxels in the ROI and $\Delta B_{0,i}$ is the field offset in voxel $i$.


## Results

### Baseline B0 inhomogeneity
![Baseline B0 RMSE per slice](figures/baseline_per_slice.png)
*Figure 1. Distribution of the baseline (unshimmed) B0 RMSE across slices in the spinal cord ROI, for each subject. Dashed lines show the median and quartiles.*

### Volume (3D) vs slice-wise shimming
Both shimming methods reduced the field inhomogeneity compared with the baseline, but slice-wise shimming performed far better (Figure 2 and Table 1):
- **Volume shimming** reduced the RMSE to 120.7 ± 23.5 Hz (range 63.7–157.3 Hz), a mean reduction of 28.6% relative to the baseline.
- **Slice-wise shimming** reduced the RMSE to 26.3 ± 8.0 Hz (range 12.9–41.9 Hz), a mean reduction of 84.1% relative to the baseline.

Slice-wise shimming outperformed volume shimming in all 14 subjects. The RMSE was lower by 94.3 ± 20.8 Hz in absolute terms, or 78.0 ± 6.3% relative to volume shimming. This difference was statistically significant (Wilcoxon signed-rank test, W = 0, p = 1.2 × 10⁻⁴).

![3D vs slice-wise shimming](figures/volume_vs_slice_wise.png)
*Figure 2. per subject B0 RMSE in the spinal cord after volume (3D) and slice-wise shimming. Black lines show the median. \*\*\*: p < 0.001 (Wilcoxon signed-rank test).*

*Table 1. B0 RMSE (Hz) in the spinal cord ROI for each subject.*

| Subject | Baseline | Volume (3D) | Slice-wise |
|---|---|---|---|
| sub-093 | 267.2 | 107.3 | 23.6 |
| sub-094 | 138.8 | 119.3 | 34.6 |
| sub-095 | 180.8 | 125.6 | 25.4 |
| sub-096 | 154.7 | 129.1 | 21.9 |
| sub-098 | 130.2 | 104.8 | 41.9 |
| sub-099 | 228.5 | 154.0 | 40.4 |
| sub-100 | 183.2 | 145.8 | 26.8 |
| sub-101 | 225.6 | 126.1 | 24.9 |
| sub-102 | 273.0 | 157.3 | 28.2 |
| sub-103 | 197.7 | 118.3 | 18.2 |
| sub-104 | 120.6 | 109.7 | 22.3 |
| sub-105 | 107.8 | 63.7 | 12.9 |
| sub-106 | 127.7 | 118.8 | 27.0 |
| sub-107 | 143.4 | 109.5 | 20.4 |
| **Mean ± SD** | **177.1 ± 54.4** | **120.7 ± 23.5** | **26.3 ± 8.0** |


Before shimming, the B0 field in the spinal cord ROI was highly inhomogeneous, with a per-subject RMSE of 177.1 ± 54.4 Hz (mean ± SD; range 107.8–273.0 Hz). The inhomogeneity was also very uneven along the cord (Figure 1). Most slices had a moderate RMSE (median of all slices: 62.1 Hz), but every subject had slices with a much larger offset, up to 293–859 Hz. In 10 of the 14 subjects, the worst slice was the most inferior one, closest to the lungs.

### Why volume shimming performs poorly
Volume shimming only reduced the RMSE by 28.6%, while slice-wise shimming reduced it by 84.1%. This gap comes mostly from the size of the region each set of coefficients has to correct. The volume ROI spans 56–60 slices (about 150 mm along the cord), whereas each slice-wise region is a single multiband group of 2 slices, i.e., about 30 times fewer voxels. With only 4 degrees of freedom (f0 and three linear gradients), a single set of coefficients cannot follow a field that varies non-linearly along the cord and rises sharply in the inferior slices near the lungs. The  solution is then a compromise driven by these large offsets, which leaves the other slices poorly corrected. In contrast, with slice-wise shimming.

### Trade-off between shimming and SNR
Even though slice-wise shimming gives a much more homogeneous field, this does not mean that 2D sequences should always be preferred. 3D sequences remain attractive for the spinal cord because of their higher SNR. For the same voxel size and readout bandwidth, the SNR is proportional to the square root of the number of times each voxel is sampled:

$$\text{SNR}_{2D} \propto \Delta V \sqrt{\frac{N_y \, N_{avg}}{BW}}, \qquad \text{SNR}_{3D} \propto \Delta V \sqrt{\frac{N_y \, N_z}{BW}}$$

where $\Delta V$ is the voxel volume, $N_y$ the number of phase-encoding lines, $N_z$ the number of partitions, $N_{avg}$ the number of averages and $BW$ the readout bandwidth. With a single average, the 3D acquisition therefore has an SNR advantage of about $\sqrt{N_z}$, at the cost of a longer acquisition per volume.

The better homogeneity of slice-wise shimming may thus not compensate for the SNR penalty of a 2D acquisition. This trade-off should be investigated for acquisitions that benefit from shimming but are SNR limited, such as quantitative susceptibility mapping (QSM) of the spinal cord, which typically relies on 3D multi-echo GRE.

### Limitations
- **Simulated shimming**: the shimmed field maps are predictions from Shimming Toolbox. They assume that the shim coils produce exactly the modeled fields and, for slice-wise shimming, that the currents can be switched instantly between slices, without eddy currents.
- **Unconstrained optimizer**: the pseudo-inverse does not enforce the scanner's current limits, so some coefficients, especially the slice-wise ones that vary rapidly, may not be achievable in practice. The reported slice-wise RMSE is therefore a best case.
- **Shim order**: only the f0 and linear terms were used. Using the scanner's second-order shims, or a dedicated spinal cord shim array (Topfer et al., 2016), may reduce the gap between the two methods.

### Future work
Further investigation should compare the SNR in the spinal cord between specific 3D and 2D sequences, combining the SNR scaling of each acquisition with the signal loss predicted from the residual through-slice gradient after volume and slice-wise shimming. Acquiring the shimmed sequences in vivo would also confirm whether the simulated improvement translates to the images.

## References
- Alonso Ortiz, E., Tous, C., Topfer, R., & Cohen-Adad, J. (2020, August). Real-time z-shimming for magnetic resonance imaging of the spinal cord [Paper]. ISMRM & SMRT annual Meeting & Exhibition (ISMRM 2020). https://archive.ismrm.org/2020/3717.html
- Bréheret A. et al. *Impact of through-slice gradient optimization for dynamic slice-wise shimming in the cervico-thoracic spinal cord.* Magn Reson Med, 2025.
- D'Astous A. et al. *Shimming toolbox: An open-source software toolbox for B0 and B1 shimming in MRI.* Magn Reson Med, 2023;89:1401-1417.
- D'Astous A., Landelle C., Bréhéret A., Guénette A., Doyon J., Alonso-Ortiz E., Cohen-Adad J. *spine_fMRI_7T.* OpenNeuro, ds007067, v4.0.0. doi:10.18112/openneuro.ds007067.v4.0.0
- Topfer R. et al. *A 24-channel shim array for the human spinal cord: design, evaluation, and application.* Magn Reson Med, 2016;76:1604-1611.

‌
