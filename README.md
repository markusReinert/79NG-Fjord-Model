# 79NG Fjord Model

This repository contains the code to create a realistic, three-dimensional, high-resolution, numerical **ocean model of the 79° North Glacier (79NG) fjord** located in Northeast Greenland, using the General Estuarine Transport Model [**GETM**](https://getm.eu/).
The model is based on the idealized 2D-vertical setup by Reinert et al. (2023) of the same fjord, which has been extended to 3D, equipped with realistic topography and forced by temporally-averaged ocean conditions from a global model.

Developed by Markus Reinert ([ORCID: 0000-0002-3761-8029](https://orcid.org/0000-0002-3761-8029)) at the Leibniz Institute for Baltic Sea Research Warnemünde (IOW) in the research project [GROCE: Greenland Ice Sheet–Ocean Interaction](https://groce.de/).
Feel free to reach out if you have any questions or would like to collaborate.


## Instructions

### 1. Compile GETM

Follow the [instructions on the official GETM website](https://getm.eu/software.html) to download the code of GETM and GOTM, and to compile GETM into an executable for your machine.
This setup requires the `glacial_ice` branch of GETM, published by Klingbeil (2023) at [DOI: 10.5281/zenodo.7741925](https://doi.org/10.5281/zenodo.7741925).
Compilation consists (roughly) of running the following two commands in an (empty) build folder, with `GETMDIR` and `GOTMDIR` defined as the paths to the downloaded GETM and GOTM codes:
```bash
cmake $GETMDIR/src -DCMAKE_INSTALL_PREFIX=`pwd` -DGETM_EMBED_VERSION=ON -DGETM_USE_PARALLEL=ON -DGOTM_BASE=$GOTMDIR
make install
```
Put the GETM executable in the path `model/bin/getm` in (a clone or release of) this repository.

### 2. Create the setup

**Note:** This step can be skipped by downloading the files included in a [Release](https://github.com/markusReinert/79NG-Fjord-Model/releases).

The files to run the model exist or will be created in the directory [model](model).
At the end of this step, the model folder should contain:
- `adaptcoord6.inp` created by editscenario
- `bdy_2d.nc` created by the notebook for boundary conditions
- `bdy_3d.nc` created by the notebook for boundary conditions
- `bdyinfo.dat` created by the notebook for boundary conditions
- `bin/getm` compiled in step 1 above
- `getm.inp` created by editscenario
- `getm_fabm.inp` also created by editscenario but not needed here
- `gotmturb.nml` included in this repository
- `grounding_line_500m.txt` created by the notebook for topography
- `init_3d.nc` created by the notebook for initial conditions
- `output.yaml` included in this repository
- `parallel.inp` included in this repository
- `par_setup.dat` created by subdiv
- `store` empty directory
- `subglacial_runoff.nc` downloaded from Reinert (2023)
- `topography_500m.nc` created by the notebook for topography

#### Input files

To create the input files, run the notebooks of this repository in the following order:

1. [Create model grid and topography](Create_topography.ipynb)
2. [Create initial conditions](Create_initial_conditions.ipynb)
3. [Create boundary conditions](Create_boundary_conditions.ipynb)

The notebooks require external data files described in the notebook headers.
Make sure to download the necessary datasets and put them in the correct locations.

#### Runoff data

Download the file [`subglacial_runoff.nc`](https://github.com/markusReinert/GETM-setup_2DV-fjord/blob/main/subglacial_runoff.nc) from the setup by Reinert (2023) and put it in the model folder.

#### Namelists

Use [editscenario](https://github.com/BoldingBruggeman/editscenario/) (can be installed from the Python Package Index with pip) to create the namelist files that configure GETM.
Assuming that GETM was downloaded to `$HOME/tools/getm/code`, run the following command to create the namelists:
```
editscenario --schemadir $HOME/tools/getm/code/schemas -e nml model configuration.xml
```
To change the model configuration, modify the [configuration file](configuration.xml) directly or make temporary modifications in the command line, e.g., `export stop="2006-01-01 00:00:00"` to limit the simulation to six model years, before running editscenario.

#### Subdomain division

This GETM setup is usually run on a large number of CPU cores, say 150.
Use `subdiv` from the [GETM-utils](https://sourceforge.net/p/getm-utils/) to create the file `par_setup.dat` describing a subdomain division suitable for the number of CPU cores available on your machine.
Put this file also in the model folder.

#### Output folder

In the model folder, create a sub-directory with the name `store` to store the model output.

### 3. Run the model

Having compiled GETM and prepared the setup files, go to the model folder and run the GETM executable.
Assuming that the parallel setup file was created for 150 CPU cores, start GETM with the following command:
```
mpirun -n 150 bin/getm
```
The model output will be saved in `model/store`.
(The files named `fjord_79NG.3d.0???.nc` in this directory are not needed and can be removed.)
Use `ncmerge` from the [GETM-utils](https://sourceforge.net/p/getm-utils/) to combine the individual subdomain outputs into a big file covering the whole model domain.


## References
Reinert, M., Lorenz, M., Klingbeil, K., Büchmann, B., & Burchard, H. (2023). _High-Resolution Simulations of the Plume Dynamics in an Idealized 79°N Glacier Cavity Using Adaptive Vertical Coordinates._ Journal of Advances in Modeling Earth Systems. [DOI: 10.1029/2023MS003721](https://doi.org/10.1029/2023MS003721)

Reinert, M. (2023). _Setup files of the 2DV-model for the 79NG fjord (v1.0.1)._ Zenodo. [DOI: 10.5281/zenodo.7755753](https://doi.org/10.5281/zenodo.7755753)
