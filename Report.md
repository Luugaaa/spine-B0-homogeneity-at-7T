---
# Spine B0 homogeneity at 7T and scanner shimming comparisonfor 3D vs slice-wise
*An ING8100 project*
## Background
### Background - Magnetic field inhomogeneities
MRI relies on a uniform magnetic field (B0) to produce images of greater quality. In practice, when a patient is present inside the scanner bore's homogenites appears.
- **Static inhomogeneities** are constant through times and comes from susceptibility variation between adjacent tissues (e.g., air–tissue interfaces at the lungs, throat, and sinuses).

### Background - B0 shimming techniques
Fortunatelty, shimming, a processe of adjusting current in conducting coils(or shims) allows to genarate exgternal magnetic fields that compensate for the main field inhomogeneities. There are multiple ways to perform shimming, based on how many different ROI you want to shim separatly:
- **Volume(3D) shimming** uses one set of shim coefficients for the entire acquistion, also called static shimming.
- **Slice-wise(2D) shimming** uses one set of shim coefficient per slices, changing for every slice during the aquisition

### Background - Limitations with 2D shimming
In practice 2D shimming should outperform 3D or be eqaul as we can use more DOF of shimming for smaller regions (Insert paper here). However, some acquistion are incompatible with slice-wise shimming like any 3D sequences(ex: 3D MeGRE). 3D sequence use signal from a full volume and not in a per slices manner, therefore slice-wise shimming is not possible, but are very usefull to obtaine a higher SNR, which is important for small ROI like the spinal-cord.

## Main question
Considering the limitations for slice-wise shimming for 3D sequence it is important to quantify the difference between 3D shimming and slice-wise shimming in the cervical spinal-cord.

![Research Question](https://img.shields.io/badge/Research-Question-brightgreen)  
How important is the difference in B0 field homogeneity after slice-wise shimming versus volume shimming ?
    

## Methods
Available on open neuro:

### Data
Available on open neuro:
### Dataset Summary

| Dataset | N | Male | Female | Age (mean ± SD) | 
|---|---|---|---|---|---|---|---|

## Results


## Discussion

## Conclusion  


## Acknowledgments



## References
- Alonso Ortiz, E., Tous, C., Topfer, R., & Cohen-Adad, J. (2020, August). Real-time z-shimming for magnetic resonance imaging of the spinal cord [Paper]. ISMRM & SMRT annual Meeting & Exhibition (ISMRM 2020). https://archive.ismrm.org/2020/3717.html
- Bréheret A. et al. *Impact of through-slice gradient optimization for dynamic slice-wise shimming in the cervico-thoracic spinal cord.* Magn Reson Med, 2025.
- D'Astous A. et al. *Shimming toolbox: An open-source software toolbox for B0 and B1 shimming in MRI.* Magn Reson Med, 2023;89:1401-1417.
- Topfer R. et al. *A 24-channel shim array for the human spinal cord: design, evaluation, and application.* Magn Reson Med, 2016;76:1604-1611.

‌

