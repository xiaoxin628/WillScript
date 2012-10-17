var grapAction = function( urlArray ){
	if (!isArray(urlArray)) return;
	var grapUrl = "api/xiaomi/grapUrl.php";
	var i  = 0, len = urlArray.length;
	//document.cookie = cookiesValue;
	//console.log(document.cookie);
	//console.log(len);

	for(;i < len; i++){
	   //iframeLink(urlArray[i]);
	   //console.log(document.cookie);
	   $j.ajax({
	      url     : grapUrl,
	      type    : "post",
	      data    : {"url": urlArray[i]},
	      success : function(html){
		var alink = getLink(html),
		    j     = 0,
	            jLen  = alink.length;
		for(;j < jLen; j++){
		//   console.log(alink[i]);
		   //if (parseInt(alink.eq(j).attr("id")) > 4000);
		   iframeLink(alink[j].attr("href"));
		};
	      }
	   });   
	};
	
};

var iframeLink = function(link){
   var iframeTmp = document.createElement("iframe");
   //console.log(link.attr("href"));
   //return;
   iframeTmp.src = link;
   iframeTmp.style.display = "none";
   if (iframeTmp.attachEvent){
	iframeTmp.attachEvent("onload", function(){
	  document.body.removeChild(this);
	});
   } else {
	iframeTmp.onload = function(){
	   document.body.removeChild(this);
        };
   };
   document.body.appendChild(iframeTmp); 
   //console.log(iframeTmp.src);
   //document.body.removeChild(iframeTmp);
};

var getLink = function(html){
   if ( html && html.length === 0 ) return;
   var linkArray = $j(html).find(".EC_mr15"),
       linkContent = [];
   //console.log(linkArray);
   for(var i=0;i<linkArray.size();i++){
      var link = linkArray.eq(i);
      if (link.attr("id")){
	var ecpp = link.find(".EC_PP>a:first");
	var domainValue = ecpp.find("font:last"), domainText  = domainValue.text();
	var whiteTrue = false;
	for(var p = 0, len = whiteName.length; p < len; p++){
	   if (whiteName[p] == domainText){
		whiteTrue = true;
		break;
	   };
	};
	if(!whiteTrue){
	    sendDomain(domainText);
	    linkContent.push(ecpp);
        };

	//console.log(domainValue.text());
	//console.log(link.find(".EC_PP>a").html());
	//console.log(linkArray.eq(i).attr("id"));
      };
   };
   return linkContent;
   //return linkArray;
	
};

var sendDomain = function(domainUrl){
	if ( domainUrl && domainUrl.length === 0) reuturn;
	document.domain = "xiaomi.com";
	$j.ajax({
	   url: "http://oss.xiaomi.com/index.php?r=bbsApi/domainCounter/index/",
	   type: "post",
	   data: {"domain": domainUrl}
	});
};
var isArray = function(obj){
	return Object.prototype.toString.call(obj) === '[object Array]'
};

// start

var $j = jQuery.noConflict();
var whiteName = ["www.360buy.com","www.qualcomm.cn"];
$j(function(){
   var grepArray = ["http://www.baidu.com/s?wd=%D0%A1%C3%D7&rsv_bp=0&rsv_spt=3&inputT=1719","http://www.baidu.com/s?wd=%D0%A1%C3%D7%CA%D6%BB%FA&rsv_bp=0&rsv_spt=3&inputT=2679"];
   grapAction(grepArray);
});


