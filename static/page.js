

$(document).ready(function(){
	$("div.new-comment").hide();
	$(window).load(
		commentSlide=function(){
			$("a.comment").click(function(){
	    	$("div.new-comment").slideToggle("slow");
	    	
	  	});

	});

});