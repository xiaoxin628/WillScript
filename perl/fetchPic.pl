#!/usr/bin/perl
=head
	多线程抓取网页图片脚本。可以按照分页抓取 自己填写page的数量
	作者Willlee will.li.628@gmail.com
	fetch Image from 500px Site.
	example:
	topit.me
	./fetchPic.pl --url=http://www.topit.me/tag/诱惑?p=%d --savePath=/Users/lixiaoxin/Pictures/fetchImage/ --pages=10 --maxThread=5 --type=site_topit
	500px.com
	./fetchPic.pl --url="http://500px.com/search?page=%d&q=coffee&type=photos&utf8=✓" --savePath=/Users/lixiaoxin/Pictures/fetchImage/ --pages=50 --maxThread=10 --type=site_500px
	normal
 	./fetchPic.pl --url="http://www.topit.me" --savePath=/Users/lixiaoxin/Pictures/fetchImage/ --pages=1 --maxThread=10
	./fetchPic.pl --url=http://www.topit.me/tag/coffee?p=%d --savePath=/media/WILL_SATA/fetchImage/ --pages=4 --maxThread=2 --maxPageRequest=2 --type=site_topit --saveFolder=coffee
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
use File::Path;

#############Config Start######################
#初始化配置
our %CONFIG = ();
#抓取的url 后边page是数量
#$CONFIG{'url'} = 'http://www.topit.me/tag/诱惑?p=%d';
$CONFIG{'url'} = '';
#our $savePath = $ENV{'HOME'}."/Pictures/fetchImage/500px/";
#our $savePath = "/home/will/data/fetchdata/topit.me/youhuo/";
#存储目录 一定需要读写
$CONFIG{'savePath'} = "$ENV{'HOME'}/fetchData/";
#存储目录下的自定义文件夹
$CONFIG{'saveFolder'} = "Pictures";
#总页数
$CONFIG{'pages'}= 10;
#每次请求多少页
$CONFIG{'maxPageRequest'}= 10;
#当前从多少页开始抓取
$CONFIG{'currentPage'}= 1;
#最大线程数
$CONFIG{'maxThread'}= 10;
#请求超时时间
$CONFIG{'requestTimeout'}= 60;
#请求agent
$CONFIG{'requestAgent'}= "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)";
#请求Referer
$CONFIG{'requestReferer'}= "http://www.google.com";
#特殊类型的网站 site_500px site_topit
$CONFIG{'type'}= "site_normal";
#############Config######################

#############Input ARGV######################
#输入参数
&checkARGV(@ARGV);
#############Input######################

#############Init Start######################
#clear ob cache
$|=1;
#下载队列
our @downqueue :shared = ();
#下载文件名称
our @downfile :shared = ();
#下载队列中的任务id
our $qnum :shared = 0;
#正在运行的子线程总数量
our $taskNum :shared = 0;
#当前从多少页开始抓取
our $currentPage = $CONFIG{'currentPage'};
#调用分析src函数
our $type = \&{$CONFIG{'type'}};
#脚本停止标记
our $stop = 0;
#############Init######################


#############Queue Start######################
#队列
my $q = Thread::Queue->new();
#############Queue######################

#############Agent Start######################

my $agent = LWP::UserAgent->new();
#超时时间
$agent->timeout($CONFIG{'requestTimeout'});
$agent->agent($CONFIG{'requestAgent'});
my $cookie_jar = HTTP::Cookies->new(file => "$ENV{'PWD'}/cookies.txt", 'autosave' => 1);
$agent->cookie_jar($cookie_jar);
my %httpHeader  = ("Referer"=>$CONFIG{'requestReferer'});
$agent->default_header(%httpHeader);
$agent->show_progress(1);
#############Agent######################



#############Function Start######################
sub fetchHTML{
	my($url, $agent) = @_;
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
		#取需要的图片并重新命名
		my %formateSrc = &formateSrc($src);
		if($formateSrc{'src'} && $formateSrc{'filename'}){
				my $filename = $formateSrc{'filename'};
				$src = $formateSrc{'src'};
				if (-e ($CONFIG{'savePath'}.$filename)) {
					&writeLog("the file [$filename] is exist!\n");
				}else{
					$qnum ++;
					$downqueue[$qnum] = $src;
					$downfile[$qnum] = $filename;
					$q->enqueue($qnum);
					&writeLog("save [$filename] to the queue!\n");
				}
		}else{
			&writeLog("[$src] is not good picture!\n");
		}
	
	}
	$tree = $tree->delete;	
}
#把图片url 更改为需要下载的url 返回相应的要存储的文件名称
sub formateSrc{
	my %data = ();
	my($src) = @_;
	return $type->($src);
	return %data;
}
#普通模式 一般网站
sub site_normal{
		my %data = ();
		my($src) = @_;
		my $filename = basename($src);
		$data{'src'} = $src;
		$data{'filename'} = $filename;
		return %data;
}
#500px.com
sub site_500px{
		my $filename = '';
		my %data = ();
		my($src) = @_;
		$src =~ s/(\d{1}\.jpg)?(\?t=\d*)?$/4.jpg/;
		my @path = split("/", $src);

		if (defined($path[4] && defined($path[5]))) {
			$filename = $path[4]."_".$path[5];
		}

		if($filename ne '_' && $path[4] && $path[5]){
				$data{'src'} = $src;
				$data{'filename'} = $filename;
		}
		return %data;
}

sub site_topit{
		my %data = ();
		my($src) = @_;
		$src =~ /(.*)([0-9a-zA-z]{18}m\.jpg)$/;
		if($2 && ($2 eq basename($src))){
				$src =~ s/m.jpg/l.jpg/;
				my $filename = basename($src);
				$data{'src'} = $src;
				$data{'filename'} = $filename;
		}
		return %data;
}

sub download{
	my($filename ,$src, $httpcode) = '';
	my($qnum) = @_;
		if ($qnum) {
			
			$src = $downqueue[$qnum];
			$filename = $downfile[$qnum];
			if($src && $filename){
				&writeLog("Down from [$src]\n");
				&writeLog("[$filename] download complete!\n");
				$httpcode = getstore($src, $CONFIG{'savePath'}.$filename);
				#system "wget -c -b -q -T 3600 -t 5 -a ".$savePath."../500px.log -O ".$savePath.$filename." \"$src\"";
				$taskNum --;
				delete $downqueue[$qnum];
				delete $downfile[$qnum];
				if (defined($httpcode)) {
					&writeLog("httpcode:[$httpcode] /Task-$qnum is done!\n");
				}
			}else{
				&writeLog("Down from [$src],but the src is not write\n");
			}
		}
}

sub doRequest{
	local(*currentPage, *CONFIG, *agent) = @_;
	my $pages = $CONFIG{'pages'};
	my $maxPageRequest = $CONFIG{'maxPageRequest'};
	my($toPage, $fromPage) = '';
	if($currentPage < $pages){
		if($currentPage == 1){
			$toPage = $pages == 1 ? 1: $currentPage + $maxPageRequest -1;
			$fromPage = $currentPage;
		}else{
			$toPage = $currentPage + $maxPageRequest;
			$fromPage = $currentPage+1;
		}
		if ($toPage > $pages) {
			$toPage = $pages;
		}
		&writeLog("Page [$currentPage-$toPage)]   Start!\n");
		my @fetchHtmlThread = [];
		for (my $i = $fromPage; $i <= $toPage; $i++) {
			my $targeturl = sprintf($CONFIG{'url'}, $i);
			$fetchHtmlThread[$i] = threads->create(\&fetchHTML,$targeturl, $agent);
			$fetchHtmlThread[$i]->join();
		}
		&writeLog("Page [$currentPage-$toPage)]   Done!\n");
		$currentPage = $toPage;
	}elsif($pages == 1){
			$toPage = $pages;
			my $targeturl = sprintf($CONFIG{'url'}, $currentPage);
			my $fetchHtmlThread = threads->create(\&fetchHTML,$targeturl, $agent);
			$fetchHtmlThread->join();
			&writeLog("Page [$currentPage/$pages]   Done!\n");
			$stop = 1;
	}elsif($currentPage == $pages && $pages != 1){
		$stop = 1;
		&writeLog("Page [$currentPage/$pages]   Done!\n");
	}else{
		&writeLog("Page [$currentPage/$pages]   Done!\n");
	
	}
}

sub checkARGV{
	local(@ARGV) = @_;
	my %params = ();
	foreach my $value (@ARGV){
		if ($value) {
			$value =~ /^--(\w*)=(.*)/o;
			print($1."\n",$2."\n");	
			print("====================\n");
			if ($2) {
				$params{$1} = $2;
			}
		}
	}
	if (!exists($params{'url'}) || !exists($params{'savePath'})) {
			print("url and savePath must is not null!");
			&doHelp();
	}

	foreach my $key (keys(%params)){
		if ($key eq 'savePath') {
			$params{'url'} =~ /(http:\/\/)?([\d\w\.]*).*/;
			my $folder = $2,;
			my $path = $params{'savePath'}.$folder."/".$CONFIG{'saveFolder'}."/";
			unless(-e $path) {
				my $res = mkpath($path,0,0777);
				if ($res) {
					print("create dir $path\n");
					$CONFIG{'savePath'} = $path;
				}else{
					print("Without the permission $path. please chmod the path\n");	
					exit();
				}
			}
			
			$CONFIG{'savePath'} = $path;
		}else{
			$CONFIG{$key} = $params{$key};
		}
	}
}

sub doHelp{
	print("\n");
	print(" "x5,"HELP:\n");
	foreach my $k (keys(%CONFIG)){
		print("--$k"."        ". "ex:--$k=$CONFIG{$k}\n");
	}
	exit;
}


sub writeLog{
	my ($log) = @_;
	printf($log);
}

#############Function######################


#############Doman Start######################
while(1){
	if ($taskNum < $CONFIG{'maxThread'}) {
		if($q->pending()){
			my $qnum = $q->dequeue();
			my $downThread = threads->create(\&download, $qnum);
			$downThread->detach();
			#the task left num
			$taskNum ++;
			&writeLog("Down Task is left [".$q->pending()."]!\n");
		}elsif($stop == 1){
			for (my $i = 10; $i >=0; $i--) {
				print("the downqueue is empty, the script will stop after $i seconds!");
				print("\r");
				sleep(1);
			}
			print("\nexit!\n");
			exit();
		}else{
			doRequest(*currentPage, *CONFIG, *agent);
		}
	}else{
			sleep(1);
			&writeLog("Running Task :[$taskNum]\n");
	}
}

#############Doman######################
