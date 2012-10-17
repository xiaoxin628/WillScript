#!/usr/bin/perl
use strict;
use warnings;
use HTML::TreeBuilder;
use LWP::Simple;
use HTTP::Cookies;
use File::Basename;
use Data::Dumper;

our $url = 'http://passport.xiaomi.com/index.php?appid=2&goto=http%3A%2F%2Fdz2.xiaomi.com%2Fextra.php%3Fmod%3Dxiaomi%2Fauthcallback';
our $host = 'http://dz2.xiaomi.com/';
our $forknum = '10';
our $savePath = $ENV{'PWD'}."/data/";
################Agent##########################
our $agent = LWP::UserAgent->new();
$agent->timeout(30);
$agent->agent('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0');
$agent->default_header('Referer' => 'http://dz2.xiaomi.com/forum.php?mod=post&action=newthread&fid=10');
our $cookie_jar = HTTP::Cookies->new(file => "$ENV{'PWD'}/bbscookies.txt", 'autosave' => 1);
$agent->cookie_jar($cookie_jar);
$agent->show_progress(1);
################Request##########################
my @form = [
	"LoginForm[username]" =>"someuser",
	"LoginForm[password]" => unpack('u', "-;&ES:'5Z=34Q,2%`(P``"),
	"LoginForm[rememberMe]" =>1,
	"yt0" => "登录",
];
my $response = $agent->post($url, \@form);
if ($response->content =~ /恭喜你，登录成功/) {
	my $tree = new HTML::TreeBuilder;
	$tree->parse_content($response->content);
	my @loginhref = $tree->find_by_tag_name('a');
	if ($loginhref[1]->attr("href")) {
		my $loginResponse = $agent->get($loginhref[1]->attr("href"));
		print($loginResponse->code."\n");
	}
	$tree = $tree->delete;	
	print("login sucessfull!\n");
}else{
	print("login failed!\n");
}
$url = $host.'forum.php?mod=post&action=newthread&fid=10';

our $bbsResponse = $agent->get($url);

if ($bbsResponse->is_success) {
	&newThread($bbsResponse->content, *agent);
}else{
	print $response->status_line, "\n";
	print $response->is_redirect, "\n";
	
}

sub newThread{
	my ($html) = @_;
	my $formhash = '';
	if ($html =~ /formhash.+value="(.+)"/){
		$formhash = $1;
	}
	my %form = (
	'albumcatid'=>'',
	'allownoticeauthor'=>1,
	'formhash'=>$formhash,
	'message'=>$ARGV[1],
	'newalbum'=>'',
	'posttime'=>time(),
	'price'=>'',
	'readperm'=>'',
	'replycredit_extcredits'=>0,
	'replycredit_membertimes'=>1,
	'replycredit_random'=>100,
	'replycredit_times'=>1,
	'rewardfloor'=>'',
	'rushreplyfrom'=>'',
	'rushreplyto'=>'',
	'save'=>'',
	'stopfloor'=>'',
	'subject'=>$ARGV[0],
	'tags'=>'',
	'typeid'=>'17',
	'uploadalbum'=>'38249',
	'usesig'=>1,
	'wysiwyg'=>0,
	);
	my $formdata = '';
	foreach my $key (keys(%form)){
		$formdata .="$key=$form{$key}&";
	}
	my $req = HTTP::Request->new(POST => $host.'forum.php?mod=post&action=newthread&fid=10&extra=&topicsubmit=yes');
	$req->content_type('application/x-www-form-urlencoded');
	$req->content($formdata);
	my $res = $agent->request($req);	
	if ($res->code == 301) {
		print ("发帖成功\n");
	}
}

