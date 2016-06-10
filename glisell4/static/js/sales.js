$( document ).ready(function($) {
	$('#page-edit-form ul.tab-nav li a[href="#content"]').text('Contenido');	
	$('#page-edit-form ul.tab-nav li a[href="#promote"]').text('Configuración');	
	$('#page-edit-form ul.tab-nav li a[href="#settings"]').text('Publicación');

    var msa = $('body.model-sale');
    msa.find("#page-edit-form footer button.action-save > em").text("Guardar En Borrador");
    msa.find("#page-edit-form footer button[value='action-publish'] > em").text("Confirmar venta");
    msa.find("#page-edit-form footer input[name='action-submit']").val("Envíar a revisión");
    msa.find("#page-edit-form footer li.actions ul>li>a.shortcut").text("Eliminar");

    if (msa.hasClass('create') || msa.not('page-is-live')) {
        var $type_desc = $('li.type-disc-rel');
        var $has_desc;
        var $lines;
        var add = $('li.sale-product-info p.add > a.button');

        var $pr = "http://127.0.0.1:8000/products/";

        $('.sale-passengers-group li.child-age').hide();

        $('li.created-date-info #id_created_date').prop('readonly', true);
        $('li.sale-taxes-field').hide().find('#id_sale_taxes').prop('readonly', true);

        $('li.total-amount-inline input').prop('readonly', true);
        $('li.sub-total-inline input').prop('readonly', true);
        $('li.amounts-sale-info li.sub-total-info input').prop('readonly', true);
        $('li.amounts-sale-info li.total-amount-info input').prop('readonly', true);
        $('li.sale-price-info input').prop('readonly', true);
        $('li.product-sale-rel').hide();

        $type_desc.hide(500);
        $('li.sale-inline-group .discount-sale-rel').hide(500);

        $('#inline_child_sale_inline_rels-0').find('li.apply-disc-rel').find('input').on('click', function () {
            if ($(this).is(':checked')) {
                $('#inline_child_sale_inline_rels-0').find('li.apply-disc-rel.focused + li.type-disc-rel').show(500);
                $('#inline_child_sale_inline_rels-0').find('li.sale-inline-group .discount-sale-rel').show(500);
            } else {
                $('#inline_child_sale_inline_rels-0').find('li.apply-disc-rel.focused + li.type-disc-rel select').val(null);
                $('#inline_child_sale_inline_rels-0').find('li.sale-inline-group .discount-sale-rel input').val(null);
                $('#inline_child_sale_inline_rels-0').find('li.apply-disc-rel.focused + li.type-disc-rel').hide(500);
                $('#inline_child_sale_inline_rels-0').find('li.sale-inline-group .discount-sale-rel').hide(500);
            }
        });

        $("#inline_child_sale_inline_rels-0").find("li.sale-passengers-group li.num-child-rel select").change(function () {
            $("#inline_child_sale_inline_rels-0").find("li.sale-passengers-group li.child-age").hide();
            if ($(this).val() == 0) {
                $("#inline_child_sale_inline_rels-0").find("li.sale-passengers-group li.child-age select").val(0);
            }
            if ($(this).val() > 0) {
                var $child = $(this).val();
                for (var n = 1; n <= $child; n++) {
                    $("#inline_child_sale_inline_rels-0").find('li.sale-passengers-group .child-' + n + '-age').show();
                }
            }
        }).trigger("change");

        // -------------------------------------------------
        function getObjects(obj, key, val) {
            var objects = [];
            for (var i in obj) {
                if (!obj.hasOwnProperty(i)) continue;
                if (typeof obj[i] == 'object') {
                    objects = objects.concat(getObjects(obj[i], key, val));
                } else if (i == key && obj[key] == val) {
                    objects.push(obj);
                }
            }
            return objects;
        }

        // -------------------------------------------------
        function getPercentVal(cost, percent) {
            return (parseFloat(cost) * parseFloat(percent)) / 100;
        }

        // -------------------------------------------------
        function getSubTotal(price, qty, days){
            return (parseFloat(price) * parseFloat(qty) * parseFloat(days));
        }
        $hotels = [];
        // $item  = new Array();
        $precio = {};
        $firstOp = 0;
        function getProdRest($url, $dataList, $parent, $child, $id) {
            // var $result = {};
            var $rs;
            var $lk;
            // $hotels = new Array();
            $item  = [];
            $precio = {};
            $.ajax({
                url: $url,
                type: "GET",
                contentType: 'application/json'
            }).then(function (data) {
                $rs = JSON.stringify(data, $dataList);
                $lk = JSON.parse($rs);
                $($lk).each(function (z) {
                    console.log("ID Proveedor! ===> "+ $id);
                    $($lk[z].supplier_product_rel).each(function (n) {
                        $($lk[z].supplier_product_rel[n].supplier_lodging_rel).each(function (j) {
                            if ($(this)[j].id == $id) { // Esto filtra a los suplidores  <<<---
//                                console.log("Aqui ESTOY--->:");
                                var $esel = $($parent).find($child + " select option[value='" + $lk[z].id + "']");
                                var intel = $lk[z].supplier_product_rel[n].inline_title;
                                var sprc = $lk[z].supplier_product_rel[n].id;
                                var rcr = $($parent).find($child + ' select');
                                var $title = $lk[z].title;
                                if (intel.length > 0){
                                    $title = $lk[z].title +" - "+intel;
                                }
                                var idcl = 'sprc-'+sprc+'-'+$($parent).attr("id");
                                if($("#"+idcl).length){// Control de las duplicaciones aqui <<<---
                                    $(this).remove();
                                }else{
                                    rcr.append('<option id="'+idcl+'" value=' + $lk[z].id + '>' + $title + '</option>');
                                } // Control de las duplicaciones aqui <<<---
                                if($("input."+idcl).length){
                                    $(this).remove();
                                }else{
                                    $($parent).find(
                                        $child + " .field-content .input"
                                    ).append('<input type="hidden" class="'+idcl+'" value='
                                              +$lk[z].supplier_product_rel[n].sale_price+
                                             ' />');
                                }
                                $precio[$lk[z].id] = {
                                    hotel: $(this)[j].id, name: $(this)[j].title, hab: $lk[z].title,
                                    price: $lk[z].supplier_product_rel[n].sale_price
                                };
                                $item[$lk[z].id] = {
                                    room: $lk[z].title,
                                    price: $lk[z].supplier_product_rel[n].sale_price
                                };
                                $hotels[$(this)[j].id] = {
                                    rooms:$item
                                };
                            }
                        });
                    });
                });
            });
        }

        var $dl = ["id", "title", "supplier_product_rel", "inline_title", "cost_price", "margin_rate",
            "profit_margin", "sale_price", "supplier_lodging_rel", "id", "title"];
        var $chisa = $("#inline_child_sale_inline_rels-0");
        var $price = 0;
        $prisa = 0;
        $sarel = 0;
        std = 0;
        $($chisa).find("li.supplier-sale-rel select").change(function () {
            var $chisa = $("#inline_child_sale_inline_rels-0");
            var $gd = 0;
            $prisa = $($chisa).find("li.product-sale-rel select").val();
            $sarel = $(this).val();
            var psr = $($chisa).find('li.product-sale-rel');
            std = psr.find('select option:selected').val();
            if ($sarel > 0) {
                psr.show(1000);
                psr.find('select option').remove();
            } else {
                $($chisa).find('li.product-sale-rel').hide(500);
                $($chisa).find('li.product-sale-rel select option').remove();
            }
            getProdRest($pr, $dl, $chisa, 'li.product-sale-rel', $sarel);
//            $($chisa).find("li.sale-price-info input").val($hotels[$sarel].rooms[$prisa].price);
            var ips = $($chisa).find("li.product-sale-rel select option:selected").attr("id");
            var tpri = $($chisa).find("li.product-sale-rel input."+ips).val();
            $($chisa).find("li.sale-price-info input").val(tpri);

        }).trigger("change");

        $($chisa).find("li.duration-sale-rel select").change(function () {
            var $dura = $(this).val();
            var $susa = $($chisa).find("li.supplier-sale-rel select").val();

        }).trigger("change");
        $($chisa).find("li.product-sale-rel select").change(function () {
            $sarel = $($chisa).find("li.supplier-sale-rel select").val();
            getProdRest($pr, $dl, $chisa, 'li.product-sale-rel', $sarel);

        }).trigger("change");

        disc = 0;
        $subTotal = 0;
        price = 0;
        qty = 0;
        dur = 0;
        $($chisa).find("li.product-sale-rel select").change(function () {
            var ips = $(this).find("option:selected").attr("id");
            var fpri = $($chisa).find("li.product-sale-rel input."+ips).val();

            $($chisa).find("li.sale-price-info input").val(fpri);
        });
        $("li.sale-product-info #inline_child_sale_inline_rels-0").hover(function() {
            $prisa = $(this).find("li.product-sale-rel select").val();
            $sarel = $(this).find("li.supplier-sale-rel select").val();
            getProdRest($pr, $dl, "#inline_child_sale_inline_rels-0", 'li.product-sale-rel', $sarel);

            // ********
            var ipclass = $(this).find("li.product-sale-rel select option:selected").attr("id");
            var fprice = $(this).find("li.product-sale-rel input."+ipclass).val();
            $($chisa).find("li.sale-price-info input").val(fprice);
            // ********

            price = $(this).find("li.sale-price-info input").val();
            qty = $(this).find("li.qty-sale-info select").val();
            dur = $(this).find("li.duration-sale-rel select").val();
            $subTotal = getSubTotal(price, qty, dur);
            $(this).find("li.sub-total-inline input").val($subTotal);
            if ($(this).find('li.apply-disc-rel input').is(':checked')) {
                disc = getPercentVal($subTotal, $($chisa).find("li.discount-sale-rel input").val());
            }else{
                disc = 0;
            }
            var get_total = ((disc > 0) ? (parseFloat($subTotal) - parseFloat(disc)) : parseFloat($subTotal));
            $(this).find("li.total-amount-inline input").val(get_total);
        });

        $tax = 0;
        $itax = {};
        $("li.taxes-sale-info p.add a#id_tax_sale_rel-ADD").mouseenter(function(){
            if($(this).find('li').hasClass('empty')){
                $('li.sale-taxes-field').hide(500).find("input").val(0);
                $("#id_sale_taxes").val(0);
            }
            $('li.sale-taxes-field').show(1500);

            $("#id_tax_sale_rel-FORMS").find("> li").not(".deleted").each(function(i){
                $tax = $(this).find(".field-content input[type='hidden']").val();
                var $dali = ["id", "name", "tax_field", "tax_calculation", "amount_of"];
                var $pcost = $("#id_sub_total").val();
                var count = 0;
                // console.log($tax);
                $.ajax({
                    url: "http://127.0.0.1:8000/taxes/",
                    type: "GET",
                    contentType: 'application/json'
                }).then(function (data){
                    $rs = JSON.stringify(data, $dali);
                    $lk = JSON.parse($rs);
                    $($lk).each(function (y) {
                        if($lk[y].id == $tax){
                            if($lk[y].tax_calculation == 'percent'){
                                $itax[$lk[y].id] = {
                                    tax: getPercentVal($pcost, $lk[y].amount_of)
                                };
                            }
                            if ($lk[y].tax_calculation == 'fixed'){
                                $itax[$lk[y].id] = {
                                    tax: $lk[y].amount_of
                                }
                            }
                        }
                    });
                });
                var sta = 0;
                var del = $(this).find(".field-content input[type='hidden']").val();
                $(this).find("button[title='Delete']").click(function(){
                    //console.log("delete");
                    //console.log(del);
                    sta = 1;
                    $itax[del] = null;
                    if ($itax.hasOwnProperty(del)) {
                        delete $itax[del];
                    }
                });
            });
            // $("#id_sale_taxes").val($itax);
        }).mouseleave(function(){
            var seltax = 0;
            if($("li.taxes-sale-info").find('li').hasClass('empty')){
                $('li.sale-taxes-field').hide(500).find("input").val(0);
                $("#id_sale_taxes").val(0);
            }
            var i;
            for (i in $itax){
                seltax += $itax[i].tax;
                console.log($itax[i].tax);
            }
            $("#id_sale_taxes").val(seltax);
            var $taxes = $("#id_sale_taxes").val();
            var $subtt = $("#id_sub_total").val();
            $("#id_total_amount").val(parseFloat($taxes) + parseFloat($subtt));
        });
        $("li.taxes-sale-info").mouseleave(function(){
            if($(".taxes-sale-info").find('li').hasClass('empty')){
                $('li.sale-taxes-field').hide(500).find("input").val(0);
                $("#id_sale_taxes").val(0);
            }
        });
        $("#page-edit-form footer").mouseenter(function(){
            if($(".taxes-sale-info").find('li').hasClass('empty')){
                $('li.sale-taxes-field').hide(500).find("input").val(0);
                $("#id_sale_taxes").val(0);
            }
             $("#id_tax_sale_rel-FORMS").find("> li").not(".deleted").each(function(i){
                $tax = $(this).find(".field-content input[type='hidden']").val();
                var $dali = ["id", "name", "tax_field", "tax_calculation", "amount_of"];
                var $pcost = $("#id_sub_total").val();
                var count = 0;
                // console.log($tax);
                $.ajax({
                    url: "http://127.0.0.1:8000/taxes/",
                    type: "GET",
                    contentType: 'application/json'
                }).then(function (data){
                    $rs = JSON.stringify(data, $dali);
                    $lk = JSON.parse($rs);
                    $($lk).each(function (y) {
                        if($lk[y].id == $tax){
                            if($lk[y].tax_calculation == 'percent'){
                                $itax[$lk[y].id] = {
                                    tax: getPercentVal($pcost, $lk[y].amount_of)
                                };
                            }
                            if ($lk[y].tax_calculation == 'fixed'){
                                $itax[$lk[y].id] = {
                                    tax: $lk[y].amount_of
                                }
                            }
                        }
                    });
                });
            });

            var seltax = 0;
            var i;
            for (i in $itax){
                seltax += $itax[i].tax;
            }
            $("#id_sale_taxes").val(seltax);
            var $taxes = $("#id_sale_taxes").val();
            var $subtt = $("#id_sub_total").val();
            $("#id_total_amount").val(parseFloat($taxes) + parseFloat($subtt));
        });
        $("li.sale-product-info").hover(function(){
            if($(".taxes-sale-info").find('li').hasClass('empty')){
                $('li.sale-taxes-field').hide(500).find("input").val(0);
                $("#id_sale_taxes").val(0);
            }
             $("#id_tax_sale_rel-FORMS").find("> li").not(".deleted").each(function(i){
                $tax = $(this).find(".field-content input[type='hidden']").val();
                var $dali = ["id", "name", "tax_field", "tax_calculation", "amount_of"];
                var $pcost = $("#id_sub_total").val();
                var count = 0;
                // console.log($tax);
                $.ajax({
                    url: "http://127.0.0.1:8000/taxes/",
                    type: "GET",
                    contentType: 'application/json'
                }).then(function (data){
                    $rs = JSON.stringify(data, $dali);
                    $lk = JSON.parse($rs);
                    $($lk).each(function (y) {
                        if($lk[y].id == $tax){
                            if($lk[y].tax_calculation == 'percent'){
                                $itax[$lk[y].id] = {
                                    tax: getPercentVal($pcost, $lk[y].amount_of)
                                };
                            }
                            if ($lk[y].tax_calculation == 'fixed'){
                                $itax[$lk[y].id] = {
                                    tax: $lk[y].amount_of
                                }
                            }
                        }
                    });
                });
            });

            var seltax = 0;
            var i;
            for (i in $itax){
                seltax += $itax[i].tax;
            }
            $("#id_sale_taxes").val(seltax);
            var $taxes = $("#id_sale_taxes").val();
            var $subtt = $("#id_sub_total").val();
            $("#id_total_amount").val(parseFloat($taxes) + parseFloat($subtt));
        });

        $("#page-edit-form").find("#id_customer").change(function () {
            var ad = $("#id_accounting_date").val();
            var ic = $(this).find("option:selected").text();
            $("#page-edit-form").find("#id_title").val(ic+" "+ad);
            $("#promote").find("#id_slug").val(ic.replace(" ","-")+"-"+$.now());
            //console.log(cd);
        });

        //var $curren;
        add.on('click', function () {
            $('#id_sale_inline_rels-FORMS').find('> li').not(".deleted").each(function (i) {

                $(this).find('li.total-amount-inline input').prop('readonly', true);
                $(this).find('li.sub-total-inline input').prop('readonly', true);
                $(this).find('li.amounts-sale-info li.sub-total-info input').prop('readonly', true);
                $(this).find('li.amounts-sale-info li.total-amount-info input').prop('readonly', true);
                var $sel_val = $(this).find("li.sale-passengers-group li.num-child-rel select");
                if (!$(this).find('li.apply-disc-rel input').is(':checked')) {
                    $(this).find('li.type-disc-rel').hide();
                    $('li#inline_child_sale_inline_rels-' + i + ' li.sale-inline-group .discount-sale-rel').hide();
                }
                if ($sel_val == 0) {
                    $(this).find('li.child-age').hide();
                }
                $(this).find('li.apply-disc-rel input').on('click', function () {
                    if ($(this).is(':checked')) {
                        $('li#inline_child_sale_inline_rels-' + i + ' li.apply-disc-rel.focused + li.type-disc-rel').show(500);
                        $('li#inline_child_sale_inline_rels-' + i + ' li.sale-inline-group .discount-sale-rel').show(500);
                    } else {
                        $('li#inline_child_sale_inline_rels-' + i + ' li.sale-inline-group .discount-sale-rel').hide(500);
                        $('li#inline_child_sale_inline_rels-' + i + ' li.sale-inline-group .discount-sale-rel input').val(null);
                        $('li#inline_child_sale_inline_rels-' + i + ' li.apply-disc-rel.focused + li.type-disc-rel select').val(null);
                        $('li#inline_child_sale_inline_rels-' + i + ' li.apply-disc-rel.focused + li.type-disc-rel').hide(500);
                    }
                });
                //$curren = $(this);
                if (i > 0) {
                    var $chisa = $("#inline_child_sale_inline_rels-" + i);
                    if (!$($chisa).find("li.supplier-sale-rel select").val()) {
                        $($chisa).find('li.product-sale-rel').hide();
                    }

                    $(this).find("li.sale-passengers-group li.num-child-rel select").change(function () {
                        $("#inline_child_sale_inline_rels-" + i).find("li.sale-passengers-group li.child-age").hide();
                        if ($(this).val() == 0) {
                            $("#inline_child_sale_inline_rels-" + i).find('li.sale-passengers-group li.child-age select').val(0);
                        }
                        if ($(this).val() > 0) {
                            var $child = $(this).val();
                            for (var n = 1; n <= $child; n++) {
                                $("#inline_child_sale_inline_rels-" + i).find('li.sale-passengers-group .child-' + n + '-age').addClass('show-me-baby').show();
                            }
                        }
                    }).trigger("change");

                    $($chisa).find("li.supplier-sale-rel select").change(function () {
                        var $result;
                        var $lookIn;
                        var $sarel = $(this).val();
                        var $chisa = $("#inline_child_sale_inline_rels-" + i);
                        if ($sarel > 0) {
                            $($chisa).find('li.product-sale-rel').show(1000);
                            $($chisa).find('li.product-sale-rel select option').remove();
                        } else {
                            $($chisa).find('li.product-sale-rel').hide(500);
                            $($chisa).find('li.product-sale-rel select option').remove();
                        }
                        getProdRest($pr, $dl, $chisa, 'li.product-sale-rel', $sarel);
                    });

                    $(this).find("li.product-sale-rel select").change(function () {
                        var ips = $(this).find("option:selected").attr("id");
                        var fpri = $($chisa).find("li.product-sale-rel input."+ips).val();
                        $(this).find("li.sale-price-info input").val(fpri);
                    });
                    $(this).mouseleave(function() {
                        var $chisa = $("#inline_child_sale_inline_rels-" + i);
                        $prisa = $(this).find("li.product-sale-rel select").val();
                        var $sarel = $(this).find("li.supplier-sale-rel select").val();
                        getProdRest($pr, $dl, $chisa, 'li.product-sale-rel', $sarel);

//                        $($chisa).find("li.sale-price-info input").val($hotels[$sarel].rooms[$prisa].price);
//                        console.log($hotels[$sarel].rooms[$prisa]);

                        var ips = $($chisa).find("li.product-sale-rel select option:selected").attr("id");
                        var fpri = $($chisa).find("li.product-sale-rel input."+ips).val();
                        $($chisa).find("li.sale-price-info input").val(fpri);

                        price = $($chisa).find("li.sale-price-info input").val();
                        qty = $(this).find("li.qty-sale-info select").val();
                        dur = $(this).find("li.duration-sale-rel select").val();
                        $subTotal = getSubTotal(price, qty, dur);
                        $(this).find("li.sub-total-inline input").val($subTotal);
                        if ($(this).find('li.apply-disc-rel input').is(':checked')) {
                            disc = getPercentVal($subTotal, $(this).find("li.discount-sale-rel input").val());
                        }else{
                            disc = 0;
                        }
                        $(this).find("li.total-amount-inline input").val(parseFloat($subTotal) - parseFloat(disc));
                    });
                }
            });
        });

        var $sapro = $("li.sale-product-info");
        $($sapro).hover(function(){
            var total = 0;
            $('#id_sale_inline_rels-FORMS').find('> li').not(".deleted").each(function (i) {
                total += parseFloat($(this).find("li.total-amount-inline input").val());
            });
            $("li.amounts-sale-info li.sub-total-info input").val(total);
        });

        // Customer get journal
        $("#id_customer").change(function () {
            var $cus = $(this).val();
            var $cufi = ["id", "title", "customer_business_rel", "id", "fis_position"];
            $.ajax({
                url: 'http://127.0.0.1:8000/customers/',
                type: "GET",
                contentType: 'application/json'
            }).then(function (data) {
                $rcus = JSON.stringify(data, $cufi);
                $posf = JSON.parse($rcus);
                $($posf).each(function (i) {
                    if($posf[i].id == $cus){
                        var fiscal = JSON.parse(JSON.stringify($posf[i], ["customer_business_rel", "id", "fis_position"]));
                        var fid = fiscal.customer_business_rel[0].fis_position
                        $.ajax({
                            url: 'http://127.0.0.1:8000/fiscal/',
                            type: "GET",
                            contentType: 'application/json'
                        }).then(function (dt) {
                            $seq = JSON.stringify(dt, ["id", "sequence"]);
                            $seqf = JSON.parse($seq);
                            $($seqf).each(function(j){
                                if($seqf[j].id == fid){
                                    $("#id_sequence").val($seqf[j].sequence);
                                }
                            });
                        });
                    }
                });
            });
        });

    }
    pef =$("body.model-sale #page-edit-form");
    $("li.sale-status.Cancelado").hide();
    $("li.sale-status.Crédito").hide();
    if($('#sale-state-bar').find("li.Abierto").hasClass('state-active')){
        pef.find("#id_sale_inline_rels-FORMS ul.controls").hide();
        pef.find("p.add").hide();
        readonly('input, select', true);
        // console.log("Hola mundo!");
        // pef.find("select").find('option').not('selected').prop('disabled', true);
        // console.log("Holass")
        //$("li.sale-status.Presupuesto").hide();
        $(pef).find("footer li.actions > div.dropdown").hide();
        $(pef).find("footer li.actions:first-child").append(
            "<button type='submit' id='sale-canceled' name='canceled' class='action-append icon icon-cancel' " +
            "data-clicked-text='Cancelando...' value='action-cancel'>" +
            "Cancelar" +
            "</button>"
        );

    }
    iss = $("#id_sale_state");
    $(pef).find("footer button[name='action-publish']").click(function(){
        $('li.sale-status').removeClass('state-active');
        $("li.sale-status.Abierto").addClass('state-active');
        //document.getElementById('#id_sale_state').selectedIndex = -1;
        $(iss).find("option").removeAttr('selected');
        $(iss).find("option[value='2']").attr("selected", "selected");
    });
    $(pef).find("footer li.actions ul li > a[href*='unpublish']").click(function(){
        $('li.sale-status').removeClass('state-active');
        $("li.sale-status.Presupuesto").addClass('state-active');
        //document.getElementById('#id_sale_state').selectedIndex = -1;
        $(iss).find("option").removeAttr('selected');
        $(iss).find("option[value='1']").attr("selected", "selected");
    });
    $("#sale-canceled").click(function(){
        $("li.sale-status").hide();
        $("li.sale-status").removeClass("state-active");
        $("li.sale-status.Cancelado").addClass("state-active").show();
        $(iss).find("option").removeAttr('selected');
        $(iss).find("option[value='4']").attr("selected", "selected");
    });
});