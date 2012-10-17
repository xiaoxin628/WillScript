#!/usr/bin/perl
#use Config; 
#
#if( $Config{useithreads} ) { 
#	printf("Hello ithreads\n") 
#} 
#elsif( $Config{use5005threads} ) { 
#	printf("Hello 5005threads\n"); 
#} 
#else { 
#	printf("Can not support thread in your perl environment\n"); 
#	exit( 1 ); 
#}

use strict;
use threads;

sub subthread{
	my($id) = @_;
	sleep(($id*2));
	print("tast_$id");
	return "Id:".($id*3);
}

my $t1= threads->create(\&subthread, 2);
my $t2= threads->create(\&subthread, 4);
print "do something in the main thread\n";
#my $t1_res = $t1->join();
#my $t1_res = $t1->join();
#print("t1_res = $t1_res\nt2_res=$t2_res\n");
$t1->detach();
 $t2->detach();
sleep(15);
