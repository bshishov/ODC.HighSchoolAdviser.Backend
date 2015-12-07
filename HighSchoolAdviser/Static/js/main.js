Array.prototype.contains = function(obj) {
  var i = this.length;
  while(i--)if(this[i] === obj)return true;return false;
}

$( document ).ready(function() {
    $(".fav").click(function(){   
        that = this; 
        var method = "add";
        if($( this ).hasClass("fa-star"))
            method = "remove"

        $.get("/my/" + $( this ).data("fav-type") + "/" + method + "/", { id: $( this ).data("fav-id") })
            .done(function() {                 
                $( that ).toggleClass("fa-star-o").toggleClass("fa-star");
            })
            .fail(function() { console.log( "error" ); })
            .always(function() {console.log( "finished" ); });        
    });

     $(".ege-toggle").click(function(){
        $("input[name='" + $(this).data('ege') + "']").parent().toggle('slow');        
     });
});