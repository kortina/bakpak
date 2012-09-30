function addLoadEvent(func) {                                                                                                                                                                       
    var oldonload = window.onload; 
    if (typeof window.onload != 'function') { 
        window.onload = func; 
    } else { 
        window.onload = function() { 
            oldonload(); 
            func(); 
        } 
    } 
} 


function loadScript(_src) {
  var e = document.createElement('script'); 
  e.setAttribute('language','javascript'); 
  e.setAttribute('type', 'text/javascript');
  e.setAttribute('src',_src); document.body.appendChild(e); 
};
