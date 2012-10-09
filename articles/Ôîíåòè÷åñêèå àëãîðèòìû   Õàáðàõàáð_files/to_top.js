/**
 * В этом файле описан функционал, который добавляет панель в правую часть сайта, которая позволяет промотать экран вверх.
 */


$(function() {

	var show = false
	var close_button = g_is_guest ? '<div class="close_panel" title="Убрать панель прокрутки"><span class="close dotted">убрать</span></div>' : ''
	
	//console.log( g_is_guest , close_button)
	
	var to_top_button = $('<div class="to_top" ><div class="to_top_panel" ><div class="to_top_button" title="Наверх"><span class="arrow">&uarr;</span> <span class="label">наверх</span></div>  '+ close_button +'</div></div>')	
		
	$('body').append(to_top_button);
	
	$('.to_top_panel', to_top_button).click(function(){
		$.scrollTo( $('body') , 500,  { axis: 'y' } );
	})
	
	$('.close_panel', to_top_button).click(function(){
		$.post('/json/settings/disable_scrollup/', { 'action': 'disable' }, function(json){
			if(json.messages == 'ok'){
				$('.to_top').remove()
				$.jGrowl('Панель отключена. Вы можете настроить показ панели в <a href="/settings/others/">настройках</a>.', { sticky: true })
			}else{
				show_system_error(json)
			}
		})
		return false;
	})
	

	      
	$(window).scroll(function () {   
		show_or_hide()
	})
	
	function show_or_hide(){
		if( window.pageYOffset > 400){
			if(!show){
				to_top_button.show()
				show = true
			}
		}else{
			if(show){
				to_top_button.hide()
				show = false
			}
		}
	}


	show_or_hide()
	
});