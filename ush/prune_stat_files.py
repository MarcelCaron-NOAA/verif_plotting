
'''
Program Name: prune_stat_files.py
Contact(s): Marcel Caron, Mallory Row
Abstract: This script is run by all scripts in EMC_verif-global/scripts/.
          This prunes the MET .stat files for the
          specific plotting job to help decrease
          wall time.
'''

import glob
import subprocess
import os
import re
import numpy as np
from datetime import datetime, timedelta as td

def daterange(start, end, td):
   curr = start
   while curr <= end:
      yield curr
      curr+=td

def expand_met_stat_files(met_stat_files, data_dir, RUN_case, RUN_type, 
                          line_type, vx_mask, fcst_var_name, var_name, model, 
                          eval_period, valid):
    valid_string = valid.strftime('%Y%m%d')
    met_stat_files_out = np.concatenate((
        met_stat_files, 
        glob.glob(os.path.join(
            # edit below to define stats archive path. Use '*' as wildcard.
            data_dir, str(RUN_case).lower(), str(model), 
            valid_string[:-2], model+'_'+valid_string+'*'
        ))
    ))
    return met_stat_files_out

def prune_data(data_dir, prune_dir, tmp_dir, valid_range, eval_period, 
               RUN_case, RUN_type, line_type, vx_mask, fcst_var_name, var_name, 
               model_list):

   print("BEGIN: "+os.path.basename(__file__))
   # Get list of models and loop through
   for model in model_list:
      # Get input and output data
      met_stat_files = []
      for valid in daterange(valid_range[0], valid_range[1], td(days=1)):
         met_stat_files = expand_met_stat_files(
            met_stat_files, data_dir, RUN_case, RUN_type, line_type, vx_mask, 
            fcst_var_name, var_name, model, eval_period, valid
         ) 
      pruned_data_dir = os.path.join(
         prune_dir, line_type+'_'+var_name+'_'+vx_mask+'_'+eval_period, tmp_dir
      )
      if not os.path.exists(pruned_data_dir):
         os.makedirs(pruned_data_dir)
      if len(met_stat_files) == 0:
         continue
      with open(met_stat_files[0]) as msf:
         met_header_cols = msf.readline()
      all_grep_output = ''
      if RUN_type == 'anom' and 'HGT' in var_name:
         print("Pruning "+data_dir+" files for vx_mask "+vx_mask+", variable "
               +fcst_var_name+", line_type "+line_type+", interp "
               +os.environ['interp'])
         filter_cmd = (
            ' | grep "'+vx_mask
            +'" | grep "'+fcst_var_name
            +'" | grep "'+line_type
            +'" | grep "'+os.environ['interp']+'"'
         )
      else:
         print("Pruning "+data_dir+" files for vx_mask "+vx_mask+", variable "
               +fcst_var_name+", line_type "+line_type)
         filter_cmd = (
            ' | grep "'+vx_mask
            +'" | grep "'+fcst_var_name
            +'" | grep "'+line_type+'"'
         )
      # Prune the MET .stat files and write to new file
      for met_stat_file in met_stat_files:
         ps = subprocess.Popen('grep -R "'+model+'" '+met_stat_file+filter_cmd,
                               shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, encoding='UTF-8')
         grep_output = ps.communicate()[0]
         all_grep_output = all_grep_output+grep_output
      pruned_met_stat_file = os.path.join(pruned_data_dir,
                                          model+'.stat')
      with open(pruned_met_stat_file, 'w') as pmsf:
         pmsf.write(met_header_cols+all_grep_output)
   print("END: "+os.path.basename(__file__))
