# ing8100-reproductibility-project

## Data

This dataset was choosen because it has a CC0 liscense allowing us to work with them. They come from collaborators: Alexandre D'Astous, PhD candidate at Neuropoly, Polytechnique Montreal and Julien Cohen-Adad, Professor at Polytechnique Montraal, co-director from Neuropoly. It was taken from OpenNeuro: https://openneuro.org/datasets/ds007067/versions/4.0.0.

This data were acquired in the spinal cord and we want to do a shimming simulation using the fielmap data in order to compare two methods: volume 
slice shimming and slice-wise shimming. This dataset is revelevant for ING8100 beccause it's an open source dataset with a complex structure already organized according to the BIDS format.


## Data Download

The data was also uploaded on Borealis:
https://demo.borealisdata.ca/dataset.xhtml?persistentId=doi:10.80240/FK2/KRFTCT

Only the `fmap` folders are needed for the shimming simulation. A Python script is provided to download them automatically via the Dataverse API.

### Setup

First step is to create an environment with the right dependencies:

```bash
conda create -n spineHomogeneity python=3.11
conda activate spineHomogeneity
pip install requests
```

> Note: for now just installing `requests` works, but a `environment.yml` will be added at the end of the project.

### Download

```bash
python scripts/download_fmap.py
```

The script queries the Borealis API, filters files whose path contains `fmap`, and saves them under the `data/` folder while preserving the original BIDS directory structure.

---

### Preprocessing

Files downloaded from Borealis have a `-2` suffix before their extension (e.g. `sub-093_magnitude1-2.json`). Run the renaming script to fix this:

```bash
python scripts/rename_fmap.py
```