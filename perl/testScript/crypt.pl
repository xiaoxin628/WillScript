#!/usr/bin/perl
=head
use Crypt::CBC;
my $key = "ffffffffffffffff";
my $pwd = 'lishuzu';
my $cipher =  Crypt::CBC->new(-key=>$key);
my $ciphertext = $cipher->encrypt("aaaaaaa");
#my $ciphertext = $cipher->encrypt("aaaaaaa");
print $ciphertext."\n";
my $deciphertext = $cipher->decrypt($ciphertext);
print $deciphertext."\n";
=cut
$str = 'lishuzu511!@#';
$packstr = pack('u', $str);
print $packstr;
print unpack("u", $packstr);

