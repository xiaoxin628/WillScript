#!/usr/bin/perl
use strict;
use LWP;
my $url = "http://bbs.xiaomi.cn";
my $agent=LWP::UserAgent->new();
my $request = HTTP::Request->new(GET=>$url); 
my $response= $agent->request($request);
#--检查是否有error发生
$response->is_success or die "$url: ",$response->message,"\n";
##--显示responser的内容
print $response->content;
#
