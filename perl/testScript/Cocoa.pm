package Cocoa;
require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(setImports, declareMain, closeMain);
sub setImports{
	my $class = shift @_;
	my @names = @_;
	foreach (@names){
		print "import".$_.";\n";
	}
}

sub declareMain{
	my $class = shift @_;
	my(@name, $extends, $implements) = @_;
	print "\n public class $name";
	if ($extends) {
		print "extends".$extends;	
	}
	if($implements){
		print "implements".$implements;
	}
	print "{ \n";
}

sub closeMain{
	print"} \n";
}

sub new{
	print "\n /*\n ** Created by Cocoa.pm \n ** Use at own risk";
	print "\n ** Did this code even get pass the javac compler?";
	print "\n **/ \n";
	#my $type = shift;
	my %parm = @_;
	my $this = {};

	$this->{'Name'} = $parm{'Name'};
	$this->{'x'} = $parm{'x'};
	$this->{'y'} = $parm{'y'};
	bless $this ,$type;
	#foreach $value (keys(%parm)){
	#	print($parm{$value}.":$value\n");
	#}
	return $this;
}

