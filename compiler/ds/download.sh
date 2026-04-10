#!/bin/bash

for i in {1..3}
do
  wget -O mihoyobbs.apk "http://appstore.vivo.com.cn/appinfo/downloadApkFile-h5appstore?id=2808879"
  if [ $? -eq 0 ]; then
    break
  fi
done
ls -l
