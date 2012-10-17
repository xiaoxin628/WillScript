mkdir $1tmp;
for i in find -name $1*.php;
 do echo $i;
 iconv -c -f gbk -t utf8 $i > $1tmp/iconv.tmp;
 mv $1tmp/iconv.tmp $i;
done
rm -rf $1tmp

