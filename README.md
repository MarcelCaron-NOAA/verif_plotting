# verif_plotting

# NCEP EMC PYTHON PLOTTING OF CAM VERIFICATION

## CONTRIBUTORS:     
Marcel Caron, marcel.caron@noaa.gov, NOAA/NWS/NCEP/EMC-VPPPGB

## PURPOSE:          
Create plots from METplus output statistics

## DESCRIPTION:      
Edit a py_plotting.config configuration file to 
define a plotting task and then execute the configuration file 
to create one or more images from METplus statistics files. 

## BEFORE YOU BEGIN: 
Make sure to set up verif_plotting if you haven't already.  To set up,
clone the Github repository:

```
git clone https://github.com/MarcelCaron-NOAA/verif_plotting
```

or, if on the NOAA WCOSS2 supercomputer, choose any directory that will house verif_plotting.  As an example, 
we'll call that directory `PY_PLOT_DIR`.  Then on the command line:

```
PY_PLOT_DIR="/path/to/my/verif/plotting/home/directory"
mkdir -p ${PY_PLOT_DIR}/out/logs ${PY_PLOT_DIR}/data ${PY_PLOT_DIR}/ush
BASE_DIR="/lfs/h2/emc/vpppg/noscrub/marcel.caron/verif_plotting"
cp -r ${BASE_DIR}/ush/* ${PY_PLOT_DIR}/ush/.
cp ${BASE_DIR}/py_plotting.config ${PY_PLOT_DIR}/.
```

### Requirements
These scripts use python v3.6+.  To set up the environment to run verif_plotting on
some of the NCEP supercomputers, use the following commands:

#### WCOSS2
```
module purge
ml intel/19.1.3.304
ml python/3.8.6
```

#### Hera
```
module purge
ml hpc/1.2.0
ml hpc-intel/18.0.5.274
module use /contrib/anaconda/modulefiles
ml anaconda/latest
```

## CONFIGURATION:    
After setting up verif_plotting, edit the configuration variables in py_plotting.config.  Each
variable contains a string that will be ingested by the python code.  You'll need to
be able to point to a correctly structured metplus statistics archive (see the
comment for Directory Settings in py_plotting.config for details).

### Limitations
In some cases, possible values for configuration variables will be limited to what is listed in the
metplus .stat files or the statistics archive you are using (e.g., values for `FCST_LEAD` or `MODEL`).  In
others, possible values will be limited to what has been predefined elsewhere in verif_plotting 
(e.g., values for `EVAL_PERIOD`).  Finally, some settings must match certain
allowable settings, which are hard-coded to prevent unexpected behaviors 
and are defined in ${USH_DIR}/settings.py in the `case_type` attribute of the `Reference()` class.  
Two asterisks (\*\*) mark these latter settings in the comments in py_plotting.config.

### Configuring Plot Type
The plot type is requested via the last configuration variable in py_plotting.config.  
Replace the value with the desired plot type as explained in the comment.  Most plots will
include all of the listed values in each user-defined configuration; 
for example, the python code will attempt to
plot all of the listed models in `MODEL` on the same plot, as well as all of the
init/valid hours in `FCST_INIT/VALID_HOUR` and lead times in `FCST_LEAD`.
Exceptions to this are any listed `var_name`s and listed domains (`VX_MASK_LIST`),
for which individual plots will be made. Listed levels are also plotted
separately unless the plot type is stat_by_level.

## EXECUTION:        
After configuring py_plotting.config, it can be run on the command line:

```
/bin/sh ${PY_PLOT_DIR}/py_plotting.config
```

... which will set the environment variables and run the python code. The python
code then follows these steps:
1. Store environment variables as global python variables. Check these 
variables and throw an error if an issue is encountered and throw warnings as
needed. Make sure the datatype for each variable is correct
2. Send the settings to df_preprocessing.py, which pulls and prunes the .stat
files--creating temporary data files in the process and storing those in
PRUNE_DIR--then loads the data as pandas dataframes, which are filtered
several times according to user settings.
3. Send the dataframe and user settings to a plotting function, which creates a
figure object, filters the data, plots the data, adjusts plot features, then
saves the plot in SAVE_DIR as a png.

## DEBUGGING:        
Part of the configuration in py_plotting.config involves setting a logfile path.
Running the script will print the logfile path for your specific task, which you
can check for debugging.  The lowest log level that is currently functional is
"DEBUG". More "DEBUG" statements may be included in a later implementation.

## ADDITIONAL SETTINGS:
Most changes in the plotting configuration are made in py_plotting.config, but a few other aspects 
of the plotting task may be changed in ${USH_DIR}/settings.py if needed.  These aspects include
the template used to find .stat files in OUTPUT_BASE_DIR, axis max/min limits, confidence level for
confidence intervals, bootstrap settings, verification time range presets, model display specs, 
and allowable plotting requests.  Comments in ${USH_DIR}/settings.py describe how most of these 
aspects can be changed.
