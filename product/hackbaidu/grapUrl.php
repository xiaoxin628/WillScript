<?php
@header("Content-type: text/html; charset=gbk");	
//$url = 'http://www.baidu.com/s?bs=%D0%A1%C3%D7&f=8&rsv_bp=1&rsv_spt=3&wd=%B2%E8%D2%B6&inputT=1539';
$url = $_POST['url'] ? $_POST['url'] : "";
$headers = array(
"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language: zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
"Cache-Control: max-age=0",
"Connection: keep-alive",
"Cookie:BAIDUID=2EF4C28830D5B7362B34D7ED7C5828B9:FG=1;",
"Host:www.baidu.com",
);
if($url){
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_HEADER, 0);
	curl_setopt($ch, CURLOPT_HTTPHEADER, $headers); 
	curl_setopt($ch, CURLOPT_TIMEOUT, '60');
	//curl_setopt($ch, CURLOPT_COOKIE, $cookie);
	curl_setopt($ch, CURLOPT_REFERER, 'http://www.baidu.com/s?bs=configure%3A+error%3A+cannot+find+the+flags+to+link+with+Boost+thread&f=8&rsv_bp=1&rsv_spt=3&wd=%D0%A1%C3%D7&inputT=4668');
	curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:11.0) Gecko/20100101 Firefox/11.0');
	$return =  curl_exec($ch);
	echo $return;
}
exit;
?>
