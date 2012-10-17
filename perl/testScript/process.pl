#!/usr/bin/perl
## turn on perl's safety features
#use strict;
#use warnings;
## load the modules I need to know
#use Term::ProgressBar;
#use LWP::Simple qw(mirror);
## work out what pages we're getting
#my @users = qw( 2shortplanks acme pudge torgox mschwern );
## create a new progress bar
#my $no_pages = @users;
#my $progress = Term::ProgressBar->new({count => $no_pages});
## get all the pages
#my $got = 0;
#foreach my $user (@users)
#{
## work out the url
#		my $url = "http://use.perl.org/~".$user."/journal/rss";
## download the url and save it to disk
#		mirror( $url, "${user}.rss" );
## update the progress bar
#		$progress->update(++$got);
#}
##!/usr/bin/perl
=head
#1.简单实用
my $max = 100;
for(1..$max) {
        my $percent = $_/$max*100;
        print "$_ - $percent % OK!\n";
        sleep(1);
}
=cut
=head
#2.用点来表示进度，windows的经典模式
##!/usr/bin/perl -w

$| = 1;
my $max = 10;
for(1..$max) {
		print ".";
		print " Complete!" if ($_ == $max);
		sleep(1);
}
=cut
=head
#3.用斜杠在转动，有点程序的样子
#!/usr/bin/perl -w

local $| = 1;
my @progress_symbol = ('-','\\','|','/');
my $n = 0;
for(my $i=1;$i<=3000;$i++){ 
		print "\r $progress_symbol[$n] $i";
		 $n = ($n>=3)? 0:$n+1;
		select(undef, undef, undef, 0.1);
}
local $| = 0;
=cut

#4.时钟的显示方式
##!/usr/bin/perl -w
=head
local $| = 1;
while (1){
		&gettime;
		print "\r $now";
		sleep(1);
}
local $| = 0;
exit;

sub gettime {
		my ($sec,$min,$hour,$day,$mon,$year,$weekday,$yeardate,$savinglightday) = (localtime(time));
		$sec = ($sec < 10)? "0$sec":$sec;
		$min = ($min < 10)? "0$min":$min;
		$hour = ($hour < 10)? "0$hour":$hour;
		$day = ($day < 10)? "0$day":$day;
		$mon = ($mon < 9)? "0".($mon+1):($mon+1);
		$year += 1900;
		$now = "$year.$mon.$day $hour:$min:$sec";
}
=cut
#5.有进度条显示，最帅的了
##!/usr/bin/perl -w
# Author: Zhao
# Date: 2009.12.22
# Purpose: simulate the progress bar

$n = 30;
for($i=1;$i<=$n;$i++){
		proc_bar($i,$n);
		select(undef, undef, undef, 0.2);
}
;

sub proc_bar{
		local $| = 1;
		my $i = $_[0] || return 0;
		my $n = $_[1] || return 0;
		print "\r [ ".("\032" x int(($i/$n)*50)).(" " x (50 - int(($i/$n)*50)))." ] ";
		printf("%2.1f %%",$i/$n*100);
		local $| = 0;
}
