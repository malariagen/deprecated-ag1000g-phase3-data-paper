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
