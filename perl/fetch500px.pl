#!/usr/bin/perl
=head
	fetch Image from 500px Site.
=cut
use strict;
use warnings;
use threads;
use Thread::Queue;
use HTML::TreeBuilder;
use LWP::Simple;
use HTTP::Cookies;
use File::Basename;
use Data::Dumper;

#############Config Start######################
#our $url = 'http://500px.com/photos?page=%d';
our $url = 'http://500px.com/search?page=%d&q=coffee&type=photos&utf8=✓';
#our $savePath = $ENV{'HOME'}."/Pictures/fetchImage/500px/";
our $savePath = "/Users/lixiaoxin/Pictures/fetchImage/500px/";
#our $savePath = "/media/01CD300E376A6F50/fetchImage/500px/";
our $pages = 50;

#############Config######################

#############Init Start######################
our @downqueue :shared = ();
our $qnum :shared = 0;
our $taskNum :shared = 0;
our $maxThread :shared = 10;
#############Init######################

#############Queue Start######################
my $q = Thread::Queue->new();
#############Queue######################

#############Agent Start######################
my $agent = LWP::UserAgent->new();
$agent->timeout(3600);
$agent->agent('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0');
$agent->from('http://www.500px.com/');
my $cookie_jar = HTTP::Cookies->new(file => "$ENV{'PWD'}/cookies.txt", 'autosave' => 1);
$agent->cookie_jar($cookie_jar);
$agent->show_progress(1);
#############Agent######################


#############Request Start######################
my @fetchHtmlThread = [];
for (my $i = 1; $i <= $pages; $i++) {
	my $targeturl = sprintf($url, $i);
	$fetchHtmlThread[$i] = threads->create(\&fetchHTML,$targeturl, $agent);
}

#############Request######################

#############Function Start######################
sub fetchHTML{
	my($url, $agent) = @_;
	print "Fetch HTML ...", "\n";
	my $response = $agent->get($url);
	if ($response->is_success) {
		&fetchImage($response->content);
	}else{
		print $response->status_line, "\n";
	}
}

sub fetchImage{
	my($html) = @_;
	my $tree = new HTML::TreeBuilder;
	$tree->parse_content($html);
	my @imgs = $tree->find_by_tag_name('img');
	foreach my $img (@imgs){
		my $src = $img->attr('src');
		if ($src) {
			# change the filename 3.jpg to 4.jpg
			$src =~ s/(\d{1}\.jpg)?(\?t=\d*)?$/4.jpg/;
			my @path = split("/", $src);
			my $filename = $path[4]."_".$path[5];
			if($filename ne '_' && $path[4] && $path[5]){
				if (-e $savePath.$filename) {
					printf("the file [$filename] is exist!\n");
				}else{
					$qnum ++;
					$downqueue[$qnum] = $src;
					$q->enqueue($qnum);
					print "save [$filename] to the queue!\n";
				}
			}
		}
	
	}
	$tree = $tree->delete;	
}

sub download{
	my($qnum) = @_;
		if ($qnum) {
				my $src = $downqueue[$qnum];
				printf("down $src\n");
				my @path = split("/", $src);
				my $filename = $path[4]."_".$path[5];
				print "[$filename] download complete!\n";
				delete $downqueue[$qnum];
				my $httpcode = getstore($src, $savePath.$filename);
				#system "wget -c -b -q -T 3600 -t 5 -a ".$savePath."../500px.log -O ".$savePath.$filename." \"$src\"";
				$taskNum --;
				print "httpcode:[$httpcode] /Task-$qnum is done!\n";
				
		}
}

#############Function######################


#############queue end######################
for (my $i = 1; $i <= $pages; $i++) {
	$fetchHtmlThread[$i]->join();
}

while(1){
	if ($taskNum < $maxThread) {
		my $qnum = $q->dequeue();
		print($qnum);
		if ($qnum) {
			my $downThread = threads->create(\&download, $qnum);
			$downThread->detach();
			#the task left num
			$taskNum ++;
			print("Down Task is left [".$q->pending()."]!\n");
		}else{
			sleep(1);
			print("the downqueue is empty, you can stop the script now!\n");
		}
	}else{
		sleep(1);
		print "Running Task :[$taskNum]\n";
	}
}
