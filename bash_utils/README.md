## Bash utility script

I wrote qnode as an extention to qstat to show longer job names by default and, more importantly, which nodes each job is running on.

 Written for bethel.uakron.edu. Definitely not guaranteed work without minor tweaking on another cluster.

Sample output:
```
Job ID      Job Name      Owner   S  Node
------  ----------------  ------  -  ----
341896  Graph20mer460K    mtsige  R  n020,n025
342352  IsoPMMAGraph500K  mtsige  R  n018,n022,n033
342353  IsoPmmaOnSilica   mtsige  R  n014,n017
342483  Abhinav3          mtsige  R  n004,n005,n013,n015,n023,n028
342671  SynPmmaOnSilica   mtsige  R  n001,n021
342687  SynPMMAGraph500K  mtsige  R  n012,n029
342723  PmmaSilica460     mtsige  R  n007,n008
342724  PMMAGraph460K     mtsige  R  n011,n027,n030
342725  Saph_Et_C5        ar86    R  n009,n010
342734  PmmaN20S460K      mtsige  R  n002,n026
```

