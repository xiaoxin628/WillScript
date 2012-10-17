#!/usr/bin/perl
use File::Basename;
=src500px
#my $src = "http://pcdn.500px.net/7892886/bd427cc08997a481562033f4f0733fc4796757ee/3.jpg?t=1337837863";
my $src = "http://pcdn.500px.net/7892886/bd427cc08997a481562033f4f0733fc4796757ee/3.jpg";
$src =~ s/(\d{1}\.jpg)?(\?t=\d*)?$/4.jpg/;
@filename = split("/", $src);
print($filename[4]);

print $src."\n";
=cut
my $src = "http://i2.topit.me/2/de/44/1136822432b0f44de2m.jpg";
#my $src = "http://i12.topit.me/m139/101393125947237899.jpg";
my $src = "http://f0.topit.me/m/201009/09/12840211227115.jpg";
#my $src = "http://i12.topit.me/m091/1009138933a3403050.jpg";
#my $src = "http://i.topit.me/O/4/3Ny2284Om.jpg";
$src =~ /(.*)([0-9a-zA-z]{18}m\.jpg)$/;
if($2){
	$src =~ s/m.jpg/l.jpg/;
	print $src."\n";
	print "11111111111111\n";
}

