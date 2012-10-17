#!/usr/bin/perl
use threads;
use threads::shared;
use strict;
my $var   :shared  = 0;       # use :share tag to define 
my @array :shared = (); # use :share tag to define 
my %hash = (); 
share(%hash);                  # use share() funtion to define 
sub start { 
	$var = 100; 

	@array[0] = 200; 
	@array[1] = 201; 

	$hash{'1'} = 301; 
	$hash{'2'} = 302; 
} 

sub verify { 
	sleep(1);                      # make sure thread t1 execute firstly 
		printf("var = $var\n");     # var=100 

		for(my $i = 0; $i < scalar(@array); $i++) { 
			printf("array[$i] = $array[$i]\n");    # array[0]=200; array[1]=201 
		} 

	foreach my $key ( sort( keys(%hash) ) ) { 
		printf("hash{$key} = $hash{$key}\n"); # hash{1}=301; hash{2}=302 
	} 
} 

my $t1 = threads->create( \&start ); 
my $t2 = threads->create( \&verify ); 

$t1->join(); 
$t2->join();
