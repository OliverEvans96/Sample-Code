#!/bin/bash
#restore_backup.sh

dir=../restored

#Delete ~/chiari/restored
rm -rf $dir

#Restore one .tar.gz archive to ~/chiari/restored
mkdir $dir
tar -xvf ../backup/$1.tar.gz -C $dir

