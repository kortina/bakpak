/* port of
https://github.com/steadicat/labels/blob/behind/labels.js
*/

/* labelfade.css
.input {
  margin: 5px 0;
  background: white;
  float: left;
  clear: both;
}
.input span {
  position: absolute;
  padding: 5px;
  margin-left: 3px;
  color: #999;
}
.input input, .input textarea, .input select {
  position: relative;
  margin: 0;
  border-width: 1px;
  padding: 6px;
  background: transparent;
  font: inherit;
}
// Hack to remove Safari's extra padding. Remove if you don't care about pixel-perfection.
@media screen and (-webkit-min-device-pixel-ratio:0) {
    .input input, .input textarea, .input select { padding: 4px; }
}
*/


function FL_applyToSpan(input, func) {
    if (input && input.parentNode) {
        var spans = input.parentNode.getElementsByTagName('span');
        for (var i = 0; i < spans.length; i++) {
            func(spans[i]);
        }
    }
}

function FL_toggle(input) {
    setTimeout(function() {
        var def = input.getAttribute('title');
        if (!input.value || (input.value == def)) {
            FL_applyToSpan(input, function(el) { el.style.visibility = ''; });   
            if (def) {
                var dummy = document.createElement('label');
                dummy.innerHTML = def;
                dummy.style.visibility = 'hidden';
                document.body.appendChild(dummy);
                FL_applyToSpan(input, function(el) { el.style['margin-left'] = dummy.offsetWidth + 3 + 'px';});
                document.body.removeChild(dummy);
            }
        } else {
            FL_applyToSpan(input, function(el) {el.style.visibility = 'hidden';});
        }
    }, 0);
}

function FL_reset(input) {
    var def = input.getAttribute('title');
    if (!input.value || (input.value == def)) {
        input.value = def;
        FL_applyToSpan(input, function(el) { el.style.visibility = ''; });
    }
}
function FL_addEvent(obj,type,fn) {
    if (obj.addEventListener) {
        obj.addEventListener(type,fn,false);
        return true;
    } else if (obj.attachEvent) {
        obj['e'+type+fn] = fn;
        obj[type+fn] = function() { obj['e'+type+fn]( window.event );};
        var r = obj.attachEvent('on'+type, obj[type+fn]);
        return r;
    } else {
        obj['on'+type] = fn;
        return true;
    }
}
function FL_setup() { // run this on body load
    var els;
    var i;
    els = document.getElementsByTagName('input');
    var color_ccc = function(el) { el.style.color = '#ccc'; };
    var color_999 = function(el) { el.style.color = '#999'; };
    for (i=0; i < els.length; i++) {
        FL_addEvent(els[i], 'keydown', function(e) {FL_toggle(e.target);});
        FL_addEvent(els[i], 'paste', function(e) {FL_toggle(e.target);});
        FL_addEvent(els[i], 'focus', function(e) { FL_applyToSpan(e.target, color_ccc);});
        FL_addEvent(els[i], 'blur', function(e) { FL_applyToSpan(e.target, color_999);});
        FL_toggle(els[i]);
    }
    els = document.getElementsByTagName('textarea');
    for (i=0; i < els.length; i++) {
        FL_addEvent(els[i], 'keydown', function(e) {FL_toggle(e.target);});
        FL_addEvent(els[i], 'paste', function(e) {FL_toggle(e.target);});
        FL_addEvent(els[i], 'focus', function(e) { FL_applyToSpan(e.target, color_ccc);});
        FL_addEvent(els[i], 'blur', function(e) { FL_applyToSpan(e.target, color_999);});
        FL_toggle(els[i]);
    }
    els = document.getElementsByTagName('select');
    for (i=0; i < els.length; i++) {
        FL_addEvent(els[i], 'change', function(e) {FL_toggle(e.target);});
    }
}
