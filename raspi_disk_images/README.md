# make an image

time sudo dd if=/dev/sdc conv=sync,noerror bs=64K | gzip -c  > raspbian.img.gz

# expand the image

time gunzip -c raspbian.img.gz | sudo dd of=/dev/sdc bs=64K 

## problems

I had problems using conv=sync,noerror,notrunc on the expansion. Corrupt
partition tables
