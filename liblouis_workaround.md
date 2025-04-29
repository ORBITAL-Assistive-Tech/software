# installing liblouis
these instructions assume you are using linux, if you are using windows please use WSL

Follow installation instructions from the [github](https://github.com/liblouis/liblouis#installation)
Detailed directions:

0. Ensure the prerequisites are installed with `sudo apt update && sudo apt install build-essential`
1. Download the latest release of liblouis from the [releases page](https://github.com/liblouis/liblouis/releases)
    - this can be done via the terminal by copying the url and using `wget <url>`
    - make sure to download the **non win** file, either tar.gz or zip is fine but these directions will assume you are downloading the tar
2. Extract the file into the current directory with `tar xf <file>`
    - the file will be called `liblouis-<version>.tar.gz`
3. Enter the extracted directory (will be named `liblouis-<version>`) and run the following commands in order
```
sudo ./configure --enable-ucs4u
sudo make
sudo make install
```
4. Ensure installed liblouis files are in `/usr/local/lib`
    - specifically make sure `liblouis.so.20` is in the directory

Then, install the python library with these directions
1. In the extracted directory again, enter `/python/louis`
2. Open `__init__.py` with your preferred text editor
    - you may have to use sudo to open it, if so a terminal text editor(like vim or nano) is strongly recommended
3. Replace the line `liblouis = _loader["liblouis.so.20"]` (around line 62) with the following
```python
import os
from ctypes import CDLL
liblouis = CDLL("/usr/local/lib/liblouis.so.20")
```
4. Navigate to the parent directory and run `sudo python3 setup.py install`
5. Test that the package was correctly installed with `sudo python3 tests/test_louis.py`