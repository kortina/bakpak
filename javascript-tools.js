/* Cross-browser implementation of element.addEventListener()
 
usage:
    listen('click', document, function(e) {console.log(e);});

*/
function listen(evnt, elem, func) {
    if (elem.addEventListener)  // W3C DOM
        elem.addEventListener(evnt,func,false);
    else if (elem.attachEvent) { // IE DOM
         var r = elem.attachEvent("on"+evnt, func);
	return r;
    }
    return null;
}


/* 
    query string encoder
via:
http://stackoverflow.com/questions/1714786/querystring-encoding-of-a-javascript-object
    usage:
    alert(serialize({foo: "hi there", bar: "100%" }));
*/
serialize = function(obj) {
  var str = [];
  for(var p in obj)
     str.push(p + "=" + encodeURIComponent(obj[p]));
  return str.join("&");
};
