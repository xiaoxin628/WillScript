#!/usr/bin/perl
use strict;
use warnings;
use HTML::TreeBuilder;
use LWP::Simple;
use HTTP::Cookies;
use File::Basename;
use Data::Dumper;

our $url = 'http://www.diandian.com/login';
our $forknum = '10';
our $savePath = $ENV{'PWD'}."/data/";
################Agent##########################
my $agent = LWP::UserAgent->new();
$agent->timeout(30);
$agent->agent('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0');
$agent->from('http://www.diandian.com/');
my $cookie_jar = HTTP::Cookies->new(file => "$ENV{'PWD'}/cookies.txt", 'autosave' => 1);
$agent->cookie_jar($cookie_jar);
$agent->show_progress(1);
################Request##########################
my @form = [
	"account" =>'lishuzu@gmail.com',
	"password" =>"9527212412",
	"persistent" =>1,
];
my $response = $agent->post($url, \@form);

$url = 'http://www.diandian.com/home';

my $bbsResponse = $agent->get($url);

#print Dumper($bbsResponse);
exit;
if ($response->is_success) {
	#&fetchImage($response->content);
}else{
	print $response->status_line, "\n";
	print $response->status_code, "\n";
	print $response->is_redirect, "\n";
	
}

sub fetchImage{
	my($html) = @_;
	my $tree = new HTML::TreeBuilder;
	$tree->parse_content($html);
	my @imgs = $tree->find_by_tag_name('img');
	foreach my $img (@imgs){
		my $src = $img->attr('src');
		if ($src) {
			my $filename = basename($src);
			#system "curl -o ".$savePath.$filename." $src";	
			print "[$filename] download complete!\n";
		}
	
	}
	$tree = $tree->delete;	
}

