# spine-B0-homogeneity-at-7T

## Research Question

Can slice-wise shimming provide a better B0 field homogeneity in the spinal cord compared to volume shimming?

---

## Data

This dataset was chosen because it has a CC0 license allowing us to work with it. It comes from collaborators: Alexandre D'Astous, PhD candidate at NeuroPoly, Polytechnique Montréal, and Julien Cohen-Adad, Professor at Polytechnique Montréal and co-director of NeuroPoly. It was taken from OpenNeuro: https://openneuro.org/datasets/ds007067/versions/4.0.0.

These data were acquired in the spinal cord and we want to do a shimming simulation using the fieldmap data in order to compare two methods: volume shimming and slice-wise shimming. This dataset is relevant for ING8100 because it's an open source dataset with a complex structure already organized according to the BIDS format.

---

## Prerequisites

Three external tools must be installed before running this pipeline.

### Spinal Cord Toolbox (SCT)

Used to segment the spinal cord and generate masks (`sct_deepseg`).

Go to the latest release: https://github.com/spinalcordtoolbox/spinalcordtoolbox/releases/ and download the version associated with your OS.

**Tested version:** SCT 7.3 (`sct_version`: `git-master-c428562d0b5fd3f386d656be89d31a61ade972a8`).
Other versions may produce different segmentation masks and therefore different results.

Full installation guide: https://spinalcordtoolbox.com/user_section/installation.html

### Shimming Toolbox

Used to generate fieldmaps and simulate shimming strategies (`st_prepare_fieldmap`, `st_b0shim`).

The installation depends on your OS.

Full installation guide: https://shimming-toolbox.org/en/latest/user_section/install.html

### FSL

`st_prepare_fieldmap` relies on FSL's `prelude` for phase unwrapping.

The Shimming Toolbox installer is supposed to install FSL, but sometimes it doesn't. If you get `FileNotFoundError: [Errno 2] No such file or directory: 'prelude'` when running `generate_fmap.sh`, install FSL manually.

Installation guide (macOS): https://fsl.fmrib.ox.ac.uk/fsl/docs/install/macos.html

Check that it's available with:

```bash
which prelude
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/mathisors/spine-B0-homogeneity-at-7T
cd spine-B0-homogeneity-at-7T
```

### 2. Create the conda environment

```bash
conda env create -f environment.yml
conda activate spineHomogeneity
```

> The `environment.yml` includes all Python dependencies. SCT and Shimming Toolbox must still be installed separately (see Prerequisites above).

---

## Reproducibility

All commands must be run from the root of the repository, since the scripts use relative paths (`./data/ds007067`).

> **Running on a subset of subjects:** every step takes `-n N` to run on the first N subjects, or `-s` followed by subject names to pick specific ones. Use the same selection for every step, otherwise later steps will look for files that were never generated. For example:
>
> ```bash
> bash scripts/download_data.sh -n 3          # sub-093, sub-094, sub-095
> bash scripts/create_sc_masks.sh -s sub-093 sub-100
> python scripts/analysis.py -s 093 100       # the sub- prefix is optional
> ```
>
> Without flag, all 14 subjects are used. Note that with fewer than 6 subjects the Wilcoxon test can't reach p < 0.05.

> **⚠️ Long processing time:** steps 2 to 4 process the 14 subjects one after the other and can take a long time to complete (fieldmap generation, deep learning segmentation and two shimming optimizations per subject). Expect the full pipeline to run for a significant amount of time, especially on a machine without a GPU. Each script prints the subject it is currently processing (`=========== sub-XXX ===========`) so you can follow its progress.

### 1. Download the data

Downloads the magnitude and phase data from OpenNeuro: https://openneuro.org/datasets/ds007067/versions/4.0.0

```bash
bash scripts/download_data.sh
```

### 2. Generate the fieldmap

Uses `st_prepare_fieldmap` from the Shimming Toolbox to generate the fieldmap from each subject's phase images.

```bash
bash scripts/generate_fmap.sh
```

### 3. Create spinal cord masks

Uses `sct_deepseg` from the Spinal Cord Toolbox to segment the spinal cord on each subject's magnitude image and generate a binary mask, dilated by 2 voxels.

```bash
bash scripts/create_sc_masks.sh
```

### 4. Run shimming simulations

Uses `st_b0shim` from the Shimming Toolbox to simulate both volume shimming and slice-wise shimming on each subject's fieldmap, using the masks generated in the previous step.

```bash
bash scripts/compare_shim.sh
```

### 5. Run the analysis

Computes the B0 field RMSE in the spinal cord for the baseline and both shimming methods, for each subject, and generates the comparison figures saved in `figures/`.

```bash
python scripts/analysis.py
```

---

## Folder Structure

```
spine-B0-homogeneity-at-7T/
├── figures/
│   ├── baseline_per_slice.png       # Baseline B0 RMSE per slice before shimming
│   └── volume_vs_slice_wise.png     # Comparison of both shimming methods
├── scripts/
│   ├── download_data.sh             # Download magnitude and phase data from OpenNeuro
│   ├── generate_fmap.sh             # Generate fieldmaps with st_prepare_fieldmap
│   ├── create_sc_masks.sh           # Generate spinal cord masks with sct_deepseg
│   ├── compare_shim.sh              # Run shimming simulations with st_b0shim
│   ├── analysis.py                  # Statistical analysis and figures
│   ├── rename_fmap.py               # Remove spurious -2 suffix (Borealis)
│   └── subjects.sh                  # Subject selection (-n / -s) shared by the bash scripts
├── .gitignore
├── AI_Prompts.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── Report.md
└── environment.yml
```

> **Note:** The `data/` folder is not tracked by Git (see `.gitignore`). Run `bash scripts/download_data.sh` to populate it locally.

---

## Note: Borealis Download Issue

Initially we wanted to download only the `fmap` folders from the Borealis mirror of the dataset:
https://demo.borealisdata.ca/dataset.xhtml?persistentId=doi:10.80240/FK2/KRFTCT

```bash
python scripts/download_fmap.py #(not existing anymore)
```

Then add a preprocessing step to remove the spurious -2 suffix added by Borealis:
```bash
python scripts/rename_fmap.py
```

However, the files uploaded to Borealis were symlinks from DataLad and not the actual data. We therefore download directly from OpenNeuro instead.

---

## Authors

Mathis Ors & Annaelle Sarrazin

---

## License

The dataset is released under a **CC0 1.0 Universal** license (public domain).
The code in this repository is released under the **MIT License**.
