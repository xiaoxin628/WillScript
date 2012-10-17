#!/usr/bin/perl

use DBI;
use Data::Dumper;

# Connect to target DB
my $dbh = DBI->connect("DBI:mysql:database=xiaomibbs;host=localhost","root","xiaomi123", {'RaiseError' => 1});

# query
my $sqr = $dbh->prepare("SELECT * FROM pre_common_member limit 10");
$sqr->execute();

while(my $ref = $sqr->fetchrow_hashref()) {
	print Dumper($ref)."\n";
}

$dbh->disconnect();
