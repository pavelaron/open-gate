#!/bin/sh
# ./build_rpi_pico_w.sh v1.22.2 PicoWExample

MPCONFIG_PATH=./micropython/ports/rp2/boards/RPI_PICO_W/mpconfigboard.h

git clone --depth 1 --branch $1 https://github.com/micropython/micropython.git

SEDOPTION="-i"
if [[ "$OSTYPE" == "darwin"* ]]; then
  SEDOPTION="-i ''"
fi

sed $SEDOPTION 's/(#define MICROPY_PY_NETWORK_HOSTNAME_DEFAULT.*)".*"/\1"'$2'"/g' $MPCONFIG_PATH

make -C ./micropython/mpy-cross/ -j 16
make -C ./micropython/ports/rp2 BOARD=RPI_PICO_W clean
make -C ./micropython/ports/rp2 BOARD=RPI_PICO_W submodules
make -C ./micropython/ports/rp2 BOARD=RPI_PICO_W -j 16
