#!/bin/sh

#定义MYSQL路径，备份用户、密码等
MYSQLBIN=/opt/soft/mysql/bin/mysql

MYSQLDUMP=/opt/soft/mysql/bin/mysqldump


##备份账号权限
#SELECT, RELOAD, SHOW DATABASES, SUPER, LOCK TABLES, REPLICATION #CLIENT
MYSQLUSER=root
MYSQLPASSWORD=89487bda8ec96121d8b47d41a0e6487d

#备份文件命名(本机ip)
MYSQLBACKNM=180.186.35.81


#定义MySQL本地备份路径
LOCALPATH=/data/backup/mysql-backup

if [ ! -d $LOCALPATH ];then
        mkdir -p $LOCALPATH
fi

#备份时间
LOCALTM=`date +%Y-%m-%d-%HH`



#不需要备份的数据库列表
NOBACKUP="information_schema|Database|^test"

#获取库名列表
DATANAME_LIST=`echo 'show databases'|$MYSQLBIN -u$MYSQLUSER -p$MYSQLPASSWORD |grep -v -E $NOBACKUP`

cd $LOCALPATH

for dbname in $DATANAME_LIST
do

        $MYSQLDUMP  -u$MYSQLUSER -p$MYSQLPASSWORD --master  --opt $dbname > ${dbname}_${LOCALTM}.sql
        gzip -9 ${dbname}_${LOCALTM}.sql

done

##压缩当天备份sql文件
tar cf  ${MYSQLBACKNM}_${LOCALTM}.tar  *${LOCALTM}.sql.gz
##删除临时文件
rm *${LOCALTM}.sql.gz


serverip="192.168.0.213"
username="backup"
password="02b96c3d"

##创建数据存放目录
ftp -nvi << open $serverip
user $username $password
bin
prompt
cd ${MYSQLBACKNM}
put ${MYSQLBACKNM}_${LOCALTM}.tar
close
bye
open


##保留7天以内备份
/usr/bin/find $LOCALPATH -type f -mtime +3 -exec rm {} \;

