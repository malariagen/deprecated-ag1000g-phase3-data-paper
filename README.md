# Ag1000G phase 3 data resource paper

This repository is for building a manuscript describing the Ag1000G
phase 3 data resource.

**This is a work in progress. Any data made available via this
repository are subject to the [Ag1000G terms of
use](https://www.malariagen.net/data/terms-use/ag1000g-terms-use).**

## Contributor setup

Fork this repository to your own github user account, then clone
locally, e.g.:

```
git clone --recursive git@github.com:{myusername}/ag1000g-phase3-data-paper.git
```

Run the conda environment installation script:

```
cd /path/to/local/clone/of/ag1000g-phase3-data-paper
./binder/install-conda.sh
```

Once conda is installed, activate the conda environment:

```
source binder/env.sh
```

Run a jupyter notebook server, e.g.:

```
jupyter notebook
```

...or:

```
jupyter lab
```

## Approach

- This is a public repo. Meaning no personal information, _e.g._, no email addresses, no reviewer comments or comments from consortium 
- This repo uses CI (continuous integration) to build the paper, the build must pass before PR can be merged, ensure no-one breaks the paper

## Structure of repo

- `notebooks` contains Jupyter notebooks, perhaps organised in subdirectories if analysis encompasses several steps.
- `artwork` contains image files (PNGs) etc included 
- Files named _descriptively_ not by likely figure position.

## Style

### Images

- Prefer PNG or PDF (vector). 
- Preferred format may depend on whether using latex or pandoc (manubot) - PDF figures are good with latex but maybe not with pandoc
- Prefer 120-300 DPI
- Style rules
  - Max 8 inches wide
  - Min 6 pt font size
  - Max 10 pt font size

### Code

- All code should be reproducible by all contributors on DataLab _i.e._ read data directly from GCS
- Python module or setup notebook to hold common code and variables (avoid copying boilerplate) TBA
- Avoid too much indirection - max one level (import Python module or %run setup notebook)

## Writing code and review process

1. Work in your own fork preferred (but not essential).
  - if branch is in main repo, prefix with your username
  - branches should include the number of the quire issue they are addressing
  - branch title marked as WIP
2. Submit PRs.
  - Check CI passes
  - remove WIP label
  - link to PR from relevant quire issue(s)
  - request review
  - No further pushes to branch (to avoid conflicts)
  - upon merge, quire issue can be closed.
3. Review.
  - Reviews should check notebooks by rerunning on datalab
  - Minor changes can be requested using "request changes"
  - More substantive changes can be made by making a PR to the branch in question. Avoid pushing directly to avoid conflicts.


