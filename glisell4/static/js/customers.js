$( document ).ready(function() {
	var title = $("li.fiscal-position .chosen span.title");
	var contact = $("ul.objects li.contact-info");
	var section = $("#content .general-info");
	var nic = $(".nic-field div.field > label");
	var position = $("#content .fiscal-position");
	// $("ul.objects > li.general-info ul.fields > li > p.add").hide();
	var type = $("#content .type-info");
	var media = $("#content .media-info");
	var location = $("#content .location-info");
	// Hiding fieldgroups
	var titles = $("#content .title.required h2 label");

	var $typeDisc;
	var $discRel;

	// $discRel.hide();
	// $typeDisc.hide();

	titles.text('Título');
	if($("body").hasClass('create')){
		section.hide();
		media.hide();
		location.hide();
		contact.hide();
		$(type).hover(function(){
			section.show(2000);
		}); 

	    $(section).hover(function(){  
		    if(title.text() == 'Persona Física'){
		    	contact.hide(2000);
		    	nic.text('Cédula:');
//		    	$(".fiscal-position div.chosen span.title").text('Consumidor Final');
//		    	$("#id_customer_business_rel-0-fis_position").val(2);
		    } else if(title.text() == 'Persona Jurídica') {
		    	contact.show(2000);
		    	nic.text('RNC:');
//		    	$(".fiscal-position div.chosen span.title").text('Para Crédito Fiscal');
//		    	$("#id_customer_business_rel-0-fis_position").val(1);
		    } else if(title.text() == 'Regímen Especial') {
		    	contact.show(2000);
		    	nic.text('RNC:');
//		    	$(".fiscal-position div.chosen span.title").text('Gubernamental');
//		    	$("#id_customer_business_rel-0-fis_position").val(3);
		    }
	    });
	    var isVisible = contact.is(':visible');
		if (isVisible === true) {
			$(this).hover(function(){
				media.show(2000);
			});
		} else { 
			$(section).hover(function(){  
				media.show(2000);
			});
		}
		$(media).hover(function(){
			$(location).show(2000);
		});  
	}
	var sku = $("li.sku-info");
	var lodging;
	if($("body").hasClass('model-product')){
		$("#id_product_type").change(function() {
			$( "select#id_product_type option:selected" ).each(function() {
				if($(this).text() != 'Almacenable'){
					sku.hide(2000)
				} else {
					sku.show(2000)
				}
			});
		}).trigger("change");
	}

	var saleState = $("#id_sale_state");
	$( "li.sale-state-info" ).append($( "<ul id='sale-state-bar'></ul>" ));
	$("#id_sale_state option").each(function(){
	 	if($(this).is(':selected')){
	 		$("#sale-state-bar").append($("<li class='sale-status "+$(this).text().replace(/\s/g, '')+" state-active'><span>"+$(this).text()+"</span></li>"));
	 	} else{
	 		$("#sale-state-bar").append($("<li class='sale-status "+$(this).text().replace(/\s/g, '')+"'><span>"+$(this).text()+"</span></li>"));
	 	}
	});
	$("#id_sale_state").change(function() {
		$("#id_sale_state option:selected").each(function(){
			 $('li.sale-status').removeClass('state-active');
			 $("li.sale-status."+$(this).text().replace(/\s/g, '')).addClass('state-active');
		});
	}).trigger("change");

	// var x = 0;
	// $("ul#id_sale_inline_rels-FORMS").change(function() {
	// 	$("ul#id_sale_inline_rels-FORMS > li").each(function(){
	// 		$(this).addClass('stdr-'+ x);
	// 		$typeDisc = $('stdr-'+ x + " .sale-head-group li.type-disc-rel");
	// 		$typeDisc.hide(); 
	// 		$('stdr-'+ x + " li.apply-disc-rel input").on('click', function(){
	// 			alert('Hola Mundosss');
	// 			if ( $(this).is(':checked') ) {
	// 				$typeDisc.show(1500);
	// 			} 
	// 			else {
	// 				$typeDisc.hide(1500);
	// 			}
	// 		});
	// 	});
	// }).trigger("change");
 

});

//$(function() {
//
//    var observer = new MutationObserver(function(mutations) {
//      mutations.forEach(function(mutation) {
//          //console.log($(mutation.removedNodes)); // <<-- includes text nodes
//          $(mutation.removedNodes).each(function(value, index) {
//              if(this.nodeType === 1) {
//                  console.log(this)
//              }
//          });
//      });
//    });
//    var config = { attributes: true, childList: true, characterData: true };
//    observer.observe($('#id_sale_inline_rels-FORMS')[0], config);
//
//});