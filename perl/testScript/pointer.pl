#!/usr/bin/perl
#$variavle = 22;
#$pointer = \$variable;
#$ice = "jello";
#$iceprt = \$ice;
#print($variavle, $pointer, $ice, $iceprt);
$pointer = \@ARGV;
printf "\n Pointer Address of ARGB = $pointer\n";
$i = scalar(@$pointer);
printf "\n Number of arguments :$i \n";
$i = 0;
foreach (@$pointer){
	printf "$i :$$pointer[$i++]; \n";
}
