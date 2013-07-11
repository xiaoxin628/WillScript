//unfollow
//select
javascript:var as = document.getElementsByTagName('div');
for (var i=0; i < as.length; i++) {
     if (as[i].getAttribute('action-type') == 'user_item') {
               var evt = document.createEvent("MouseEvents"); 
               evt.initEvent("click", true, true);
               as[i].dispatchEvent(evt);
     };
};
//cancel
var cancelbtns = document.getElementsByTagName('a');
for (var i=0; i < cancelbtns.length; i++) {
     if (cancelbtns[i].getAttribute('action-type') == 'cancel_follow') {
               var evt = document.createEvent("MouseEvents"); 
               evt.initEvent("click", true, true);
               cancelbtns[i].dispatchEvent(evt);
     };
};
//ok
var okbtns = document.getElementsByTagName('a');
for (var i=0; i < okbtns.length; i++) {
     if (okbtns[i].getAttribute('node-type') == 'OK') {
               var evt = document.createEvent("MouseEvents"); 
               evt.initEvent("click", true, true);
               okbtns[i].dispatchEvent(evt);
     };
};
//next page
var okbtns = document.getElementsByTagName('a');
for (var i=0; i < okbtns.length; i++) {
     if (okbtns[i].getAttribute('action-type') == 'switchType') {
               var evt = document.createEvent("MouseEvents");
               evt.initEvent("click", true, true);
               okbtns[i].dispatchEvent(evt);
     };
};





//follow

javascript:var as = document.getElementsByTagName('a');
for (var i=0; i < as.length; i++) {
     if (as[i].getAttribute('item-func') != null) {
               var evt = document.createEvent("MouseEvents"); 
               evt.initEvent("click", true, true);
               as[i].dispatchEvent(evt);

     };
};
for(var i = 0; i < pairs.length; i++) {
  var pos = pairs[i].indexOf('=');
             // Look for "name=value"
             if (pos == -1) continue;
                    // If not found, skip
                var argname = pairs[i].substring(0,pos);// Extract the name
                var value = pairs[i].substring(pos+1);// Extract the value
                value = decodeURIComponent(value);// Decode it, if needed
                args[argname] = value;
                        // Store as a property
} 