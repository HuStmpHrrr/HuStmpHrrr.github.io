$(function() {
  function getFreq(e) {
    return parseInt($(e).find("sup").text());
  }

  var elem = $(".tags-list ul li").detach().sort(function (a, b) {
     var o = getFreq(b) - getFreq(a); 
     if (!o) {
       var ta = $(a).clone().children().remove().end().text(),
           tb = $(b).clone().children().remove().end().text();
       return ta < tb ? -1 : ta > tb;
     }
     return o;
  });
  
  $(".tags-list ul").append(elem);
})
