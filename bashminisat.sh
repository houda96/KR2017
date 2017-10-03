#!/bin/bash

## DataDIMACS NormOut
## DataDIMACSEFF effOut
## DataDIMACSMIN minOut
  ## (Large/Mini/Normal)E/M/H

folder=DataDIMACSMIN/
folder2=MiniE/
folder3=minOutND/

for file in $folder/$folder2*.txt
do
      name=${file##*/}
      ## deterministic
      #./minisat -no-luby $file > $folder3$folder2$name
      ## non deterministic
      ./minisat -rnd-init -luby -rnd-freq=0.3 $file > $folder3$folder2$name
done
