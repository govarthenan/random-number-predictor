sudo apt-get install libopenblas-dev
echo 'export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH' >> ~/.bashrc
echo 'export OPENBLAS_NUM_THREADS=1  # You can adjust this based on your CPU cores' >> ~/.bashrc
source ~/.bashrc