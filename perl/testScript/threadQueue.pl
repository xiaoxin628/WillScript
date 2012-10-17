#!/usr/bin/perl
use threads; 
use Thread::Queue; 

my $q = Thread::Queue->new(); 

sub produce { 
	my $name = shift; 
	for($i=0;$i<=100;$i++){
		my $r = int(rand(100)); 
		$q->enqueue($r); 
		printf("$name produce $r\n"); 
		sleep(int(rand(3))); 
	} 

	#while(1) { 
	#	my $r = int(rand(100)); 
	#	$q->enqueue($r); 
	#	printf("$name produce $r\n"); 
	#	sleep(int(rand(3))); 
	#} 
} 

sub consume { 
	my $name = shift; 
	while(my $r = $q->dequeue()) { 
		printf("consume $r\n"); 
		printf("total:".$q->pending()."\n");
	} 
} 

my $producer1 = threads->create(\&produce, "producer1"); 
my $producer2 = threads->create(\&produce, "producer2"); 
my $consumer1 = threads->create(\&consume, "consumer2"); 

$producer1->join(); 
$producer2->join(); 
$consumer1->join(); 
