import argparse
import os
import nibabel as nib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statannotations.Annotator import Annotator

DATA = "./data/ds007067"
ALL_SUBJECTS = ["sub-093", "sub-094", "sub-095", "sub-096", "sub-098", "sub-099", "sub-100",
                "sub-101", "sub-102", "sub-103", "sub-104", "sub-105", "sub-106", "sub-107"]

# Same subject selection as the bash scripts (see scripts/subjects.sh)
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-n", type=int, help="run on the first N subjects")
group.add_argument("-s", nargs="+", metavar="SUB", help="run on the given subjects only")
args = parser.parse_args()

if args.n is not None:
    if args.n < 1:
        parser.error("-n expects a positive integer")
    SUBJECTS = ALL_SUBJECTS[:args.n]
elif args.s:
    SUBJECTS = [s if s.startswith("sub-") else f"sub-{s}" for s in args.s]
    unknown = [s for s in SUBJECTS if s not in ALL_SUBJECTS]
    if unknown:
        parser.error(f"unknown subjects: {unknown}")
else:
    SUBJECTS = ALL_SUBJECTS
print("Subjects:", " ".join(SUBJECTS))


def rmse(fmap):
    voxels = fmap[np.isfinite(fmap)]
    values, counts = np.unique(voxels, return_counts=True)
    max_index = np.argmax(counts)
    most_represented = values[max_index]
    # Voxels outside the mask all share the same constant value: drop them
    if counts[max_index] > 30:
        voxels = voxels[voxels != most_represented]

    return np.sqrt(np.mean(voxels**2)) if voxels.size > 1 else np.nan


def roi(fmap):
    # Voxels of a shimmed output that are not the constant outside-mask value
    values, counts = np.unique(fmap, return_counts=True)
    return np.isfinite(fmap) & (fmap != values[np.argmax(counts)])


rmse_baseline_per_slice = {}
rmse_volume_per_slice = {}
rmse_slice_wise_per_slice = {}

for sub in SUBJECTS:
    fmap = nib.load(os.path.join(DATA, sub, "fmap", "fmap.nii.gz")).get_fdata()
    volume_dir = os.path.join(DATA, sub, "shim", "volume")
    volume_file = [f for f in os.listdir(volume_dir) if f.startswith("fieldmap_calculated") and f.endswith(".nii.gz")][0]
    volume = nib.load(os.path.join(volume_dir, volume_file)).get_fdata()
    slice_wise_dir = os.path.join(DATA, sub, "shim", "slice_wise")
    slice_wise_file = [f for f in os.listdir(slice_wise_dir) if f.startswith("fieldmap_calculated") and f.endswith(".nii.gz")][0]
    slice_wise = nib.load(os.path.join(slice_wise_dir, slice_wise_file)).get_fdata()

    mask = roi(volume)

    n_slices = fmap.shape[2]
    rmse_baseline_per_slice[sub] = np.full(n_slices, np.nan)
    rmse_volume_per_slice[sub] = np.full(n_slices, np.nan)
    rmse_slice_wise_per_slice[sub] = np.full(n_slices, np.nan)
    for slice in range(n_slices):
        baseline_slice = fmap[:, :, slice][mask[:, :, slice]]
        if baseline_slice.size > 0:
            rmse_baseline_per_slice[sub][slice] = np.sqrt(np.mean(baseline_slice**2))
        rmse_volume_per_slice[sub][slice] = rmse(volume[:, :, slice])
        rmse_slice_wise_per_slice[sub][slice] = rmse(slice_wise[:, :, slice])

print(f"{'subject':<10}{'baseline':>12}{'volume':>12}{'slice_wise':>12}")
for sub in SUBJECTS:
    baseline = np.sqrt(np.nanmean(rmse_baseline_per_slice[sub]**2))
    volume = np.sqrt(np.nanmean(rmse_volume_per_slice[sub]**2))
    slice_wise = np.sqrt(np.nanmean(rmse_slice_wise_per_slice[sub]**2))
    print(f"{sub:<10}{baseline:>12.3f}{volume:>12.3f}{slice_wise:>12.3f}")

# Plot 1: baseline RMSE per subject, distribution over slices
df_baseline = pd.concat([pd.DataFrame({'Value': rmse_baseline_per_slice[sub], 'Subject': sub}) for sub in SUBJECTS], ignore_index=True)

sns.set_theme(style="ticks")
fig, ax = plt.subplots(figsize=(8, 4), dpi=200)

sns.violinplot(
    data=df_baseline, x='Subject', y='Value',
    color="#18659D", inner='quartile', cut=0, linewidth=0.8, ax=ax
)

ax.set_xlabel('Subject')
ax.set_ylabel('RMSE (Hz)')
ax.set_title('Baseline B0 RMSE per slice in the spinal cord')
sns.despine(ax=ax)
ax.tick_params(axis='x', labelsize=8, rotation=45)

os.makedirs("./figures", exist_ok=True)
fig.savefig("./figures/baseline_per_slice.png", bbox_inches="tight")

# Plot 2: volume (3D) vs slice-wise shim, every dot is a subject
df_volume = pd.DataFrame({'Value': [np.sqrt(np.nanmean(rmse_volume_per_slice[sub]**2)) for sub in SUBJECTS], 'Group': '3D'})
df_slice_wise = pd.DataFrame({'Value': [np.sqrt(np.nanmean(rmse_slice_wise_per_slice[sub]**2)) for sub in SUBJECTS], 'Group': 'Slice-wise'})

for d in (df_volume, df_slice_wise):
    d['Subject'] = range(len(d))

df = pd.concat([df_volume, df_slice_wise], ignore_index=True)
fig, ax = plt.subplots(figsize=(4, 4), dpi=200)

sns.lineplot(
    data=df, x='Group', y='Value', units='Subject',
    estimator=None, color='gray', alpha=0.15, linewidth=0.7,
    legend=False, ax=ax, zorder=3
)

sns.swarmplot(
    data=df, x='Group', y='Value', hue='Group',
    palette=["#18659D", "#D1495B"],
    size=4.5, alpha=1, ax=ax, zorder=3
)

sns.boxplot(
    showmeans=False,
    medianprops={'color': 'k', 'ls': '-', 'lw': 1.4},
    whiskerprops={'visible': False},
    zorder=10,
    x="Group",
    y="Value",
    data=df,
    showfliers=False,
    showbox=False,
    showcaps=False,
    ax=ax
)

ax.set_xlabel('Shimming method')
ax.set_ylabel('RMSE (Hz)')
ax.set_title(f'3D vs slice-wise B0 shimming in the spinal cord (n={len(SUBJECTS)})')
sns.despine(ax=ax)
ax.tick_params(axis='x', labelsize=8)

pairs = [("3D", "Slice-wise")]

annotator = Annotator(ax, pairs, data=df, x="Group", y="Value")
annotator.configure(
    test='Wilcoxon',
    text_format='star',
    loc='inside'
)
annotator.apply_test()
annotator.annotate()
fig.savefig("./figures/volume_vs_slice_wise.png", bbox_inches="tight")

plt.show()
