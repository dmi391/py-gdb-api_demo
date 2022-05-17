#!/bin/bash

source ../paths

ELF="$1"


OPENOCD_LAUNCH="$OPENOCD -f $OPENOCD_CFG_HW"
GDB_LAUNCH="$GDB -x $GDB_SCRIPT --silent $ELF"


#Launch: Hardware + OpenOCD + GDB
xfce4-terminal \
--tab --title=OpenOCD -e "$OPENOCD_LAUNCH" \
--tab --title=GDB --hold -e "$GDB_LAUNCH"

exit 0
