$(function(){
	$('.auth-form').hide();
	
	$('.auth').click(function() {
		$('.auth-form').toggle();
		$('.other-projects').hide();
		$('.hide').addClass('other');
		$('.hide').removeClass('hide');
		return false;
	});
	
	$(document).click(function(event){ 		
			var target = $(event.target);
			if (target.parents(".enter").length == 0) {				
				$(".auth-form").hide();
			}
	});	
});
		
	
$(function(){
	$('.other-projects').hide();
	
	$('.other').click(function(){
		$('.other-projects').toggle();
		$('.other').toggleClass('hide');
		$('.auth-form').hide();
		return false;
	});
	
	$(document).click(function(event){ 		
			var target = $(event.target);
			if (target.parents(".projects").length == 0) {				
				$(".other-projects").hide();
				$('.hide').addClass('other');
				$('.hide').removeClass('hide');
			}
	});	
});
		
		

$(function(){
	$('.section-toggle').each(function(){
		$(this).click(function(){
			$(this).next('.archive-article-info').toggle();
			return false;
		});
	});
});


$(function(){
	$('.toggle').each(function(){
		$(this).click(function(){
			$(this).next('.sub-menu').slideToggle('fast');
			return false;
		});
	});
});
		