#!/bin/bash
echo "
      K. Wardle 6/22/09, modified by H. Stadler Dec. 2013, minor fix Will Bateman Sep 2014.
      bash script to run reconstructPar in pseudo-parallel mode
      by breaking time directories into multiple ranges
     "
     
USAGE="
      USAGE: $0 -n <NP> -f fields -o <OUTPUTFILE>
        -f (fields) is optional, fields given in the form T,U,p; option is passed on to reconstructPar
  -t (times) is optional, times given in the form tstart,tstop
        -o (output) is optional 
"

#TODO: add flag to trigger deletion of original processorX directories after successful reconstruction
# At first check whether any flag is set at all, if not exit with error message
if [ $# == 0 ]; then
    echo "$USAGE"
    exit 1
fi

#Use getopts to pass the flags to variables
while getopts "f:n:o:t:" opt; do
  case $opt in
    f) if [ -n $OPTARG ]; then
  FIELDS=$(echo $OPTARG | sed 's/,/ /g')
  fi
      ;;
    n) if [ -n $OPTARG ]; then
  NJOBS=$OPTARG
  fi
      ;;
    o) if [ -n $OPTARG ]; then
  OUTPUTFILE=$OPTARG
       fi
      ;;
    t) if [ -n $OPTARG ]; then
  TLOW=$(echo $OPTARG | cut -d ',' -f1)
  THIGH=$(echo $OPTARG | cut -d ',' -f2)
  fi
      ;;
    \?)
      echo "$USAGE" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# check whether the number of jobs has been passed over, if not exit with error message
if [[ -z $NJOBS ]]
then
    echo "
      the flag -n <NP> is required!
       "
    echo "$USAGE"
    exit 1
fi

APPNAME="reconstructPar"

echo "running $APPNAME in pseudo-parallel mode on $NJOBS processors"

#count the number of time directories
NSTEPS=$(($(ls -d processor0/[0-9]*/ | wc -l)-1))
NINITAL=$(ls -d [0-9]*/ | wc -l) ##count time directories in case root dir, this will include 0

P=p
#find min and max time
TMIN=$(ls processor0 -1v | sed '/constant/d' | sort -g | sed -n 2$P) # modified to omit constant and first time directory
#TMIN=`ls processor0 | sort -nr | tail -1`
TMAX=$(ls processor0 -1v | sed '/constant/d' | sort -gr | head -1) # modified to omit constant directory
#TMAX=`ls processor0 | sort -nr | head -1`

#Adjust min and max time according to the parameters passed over
if [ -n "$TLOW" ]
  then
    TMIN=$(ls processor0 -1v | sed '/constant/d' | sort -g | sed -n 1$P) # now allow the first directory
    NLOW=2
    NHIGH=$NSTEPS
    # At first check whether the times are given are within the times in the directory
    if [ $(echo "$TLOW > $TMAX" | bc) == 1 ]; then
        echo "
      TSTART ($TLOW) > TMAX ($TMAX)
      Adjust times to be reconstructed!
      "
        echo "$USAGE"
        exit 1
    fi
    if [ $(echo "$THIGH < $TMIN" | bc) == 1 ]; then
        echo "
      TSTOP ($THIGH) < TMIN ($TMIN)
      Adjust times to be reconstructed!
      "
        echo "$USAGE"
        exit 1
    fi
  
    # Then set Min-Time
    until [ $(echo "$TMIN >= $TLOW" | bc) == 1 ]; do
      TMIN=$(ls processor0 -1v | sed -n $NLOW$P)
      NSTART=$(($NLOW))
      let NLOW=NLOW+1
    done

    # And then set Max-Time
    until [ $(echo "$TMAX <= $THIGH" | bc) == 1 ]; do
      TMAX=$(ls processor0 -1v | sed -n $NHIGH$P)
      let NHIGH=NHIGH-1
    done

    # Finally adjust the number of directories to be reconstructed
    NSTEPS=$(($NHIGH-$NLOW+3))

  else

    NSTART=2

fi

echo "reconstructing $NSTEPS time directories"

NCHUNK=$(($NSTEPS/$NJOBS))
NREST=$(($NSTEPS%$NJOBS))
TSTART=$TMIN

echo "making temp dir"
TEMPDIR="temp.parReconstructPar"
mkdir $TEMPDIR

PIDS=""
for i in $(seq $NJOBS)
do
  if [ $NREST -ge 1 ]
    then
      NSTOP=$(($NSTART+$NCHUNK))
      let NREST=$NREST-1
    else
      NSTOP=$(($NSTART+$NCHUNK-1))
  fi
  TSTOP=$(ls processor0 -1v | sed -n $NSTOP$P)


  if [ $i == $NJOBS ] 
  then
  TSTOP=$TMAX
  fi

  if [ $NSTOP -ge $NSTART ]
    then  
    echo "Starting Job $i - reconstructing time = $TSTART through $TSTOP"
    if [ -n "$FIELDS" ]
      then
        $($APPNAME -fields "($FIELDS)" -time $TSTART:$TSTOP > $TEMPDIR/output-$TSTOP &)
  echo "Job started with PID $(pgrep -n -x $APPNAME)"
  PIDS="$PIDS $(pgrep -n -x $APPNAME)" # get the PID of the latest (-n) job exactly matching (-x) $APPNAME
      else
        $($APPNAME -time $TSTART:$TSTOP > $TEMPDIR/output-$TSTOP &)
  echo "Job started with PID $(pgrep -n -x $APPNAME)"
  PIDS="$PIDS $(pgrep -n -x $APPNAME)"
    fi
   fi

  let NSTART=$NSTOP+1
  TSTART=$(ls processor0 -1v | sed -n $NSTART$P)
done

#sleep until jobs finish
#if number of jobs > NJOBS, hold loop until job finishes
NMORE_OLD=$(echo 0)
until [ $(ps -p $PIDS | wc -l) -eq 1 ]; # check for PIDS instead of $APPNAME because other instances might also be running 
  do 
    sleep 10
    NNOW=$(ls -d [0-9]*/ | wc -l) ##count time directories in case root dir, this will include 0
    NMORE=$(echo $NSTEPS-$NNOW+$NINITAL | bc) ##calculate number left to reconstruct and subtract 0 dir
    if [ $NMORE != $NMORE_OLD ]
      then
      echo "$NMORE directories remaining..."
    fi
    NMORE_OLD=$NMORE
  done

#combine and cleanup
if [ -n "$OUTPUTFILE" ] 
  then
#check if output file already exists
  if [ -e "$OUTPUTFILE" ] 
  then
    echo "output file $OUTPUTFILE exists, moving to $OUTPUTFILE.bak"
    mv $OUTPUTFILE $OUTPUTFILE.bak
  fi

  echo "cleaning up temp files"
  for i in $(ls $TEMPDIR)
  do
    cat $TEMPDIR/$i >> $OUTPUTFILE
  done
fi

rm -rf $TEMPDIR

echo "finished"
