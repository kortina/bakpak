/* via
http://stackoverflow.com/questions/1714786/querystring-encoding-of-a-javascript-object
*/
serialize = function(obj) {
  var str = [];
  for(var p in obj)
     str.push(p + "=" + encodeURIComponent(obj[p]));
  return str.join("&");
}

alert(serialize({foo: "hi there", bar: "100%" }));
