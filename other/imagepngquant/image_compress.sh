#!/bin/bash

#使用教程
#到https://pngquant.org安装pngquant的Command-line，如（Binary for Mac OS X ）
#到~/.bash_profile配置环境环境变量

#export PNGQUANT=/Users/wza/Documents/pngquant(这里修改成自己的路径)
#export PATH=$PNGQUANT:$PATH

#执行./image_compress.sh path(path是要压缩的路径)，完毕

function compress {
    local DIR=$1
    declare -a filelist
    for item in `ls $DIR` ;do
        if [ -f $DIR/$item ]  ;then
            if [ "${item:0,-4}" == ".png" ] ;then
                filelist[${#filelist[@]}]=$DIR/$item
            fi
        elif [ -d $DIR/$item ]; then
            echo $DIR/$item
            compress $DIR/$item
        fi
    done 
   # echo ${filelist[*]}
   if [ ${#filelist[*]} -gt 0 ];then
        pngquant 256 --ext .png ${filelist[*]} --force --skip-if-larger 
   fi
}  

path=$1
if [ ! $path ];then
    echo 路径不能为空！
    exit
else
    if [ ! -d $path ];then
        echo 路径不存在！
        exit
    fi
fi
echo 正在压缩 ... 
du -sh $path
compress $path
echo 压缩完毕！
du -sh $path