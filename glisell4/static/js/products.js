/**
 * Created by Norberto on 4/24/2016.
 */
$( document ).ready(function() {
    //var defaultForm = $unchangedForm.serialize();
    //
    //function checkIfFormChanged($form) {
    //    return defaultForm !== $form.serialize();
    //    // You can also use a one-liner: return !(defaultForm !== $form.serialize())
    //}
    function getPercentVal(cost, percent, type){
        var $result;
        if(type == 1){
            $result = parseFloat(cost) + ((parseFloat(percent) * parseFloat(cost))/100.00);
        }else{
            $result = parseFloat(cost) + parseFloat(percent);
        }
        return $result
    }

    if ($('body').hasClass('model-product')) {
        var $add = $('a#id_supplier_product_rel-ADD');
        var $prosa = $("#inline_child_supplier_product_rel-0");
        var $cost = 0;
        var $percent = 0;
        var $type = 0;

        $($prosa).find("li.cost-price-info input").change(function () {
            $cost = $($prosa).find("li.cost-price-info input").val();
            $percent = $($prosa).find("li.profit-margin-info input").val();
            $type = $($prosa).find("li.marging-rate-info select").val();
            $($prosa).find("li.sale-price-info input").prop('readonly', true).val(getPercentVal($cost, $percent, $type));
        }).trigger("change");

        $($prosa).find("li.profit-margin-info input").change(function () {
            $cost = $($prosa).find("li.cost-price-info input").val();
            $percent = $($prosa).find("li.profit-margin-info input").val();
            $type = $($prosa).find("li.marging-rate-info select").val();
            $($prosa).find("li.sale-price-info input").prop('readonly', true).val(getPercentVal($cost, $percent, $type));
        }).trigger("change");

        $($prosa).find("li.marging-rate-info select").change(function () {
            $cost = $($prosa).find("li.cost-price-info input").val();
            $percent = $($prosa).find("li.profit-margin-info input").val();
            $type = $($prosa).find("li.marging-rate-info select").val();
            $($prosa).find("li.sale-price-info input").prop('readonly', true).val(getPercentVal($cost, $percent, $type));
        }).trigger("change");

        $add.on('click', function () {
            $('#id_supplier_product_rel-FORMS').find('> li:not(deleted)').each(function (i) {
                var $verso = $("#inline_child_supplier_product_rel-" + i);
                /*
                $('#id_supplier_product_rel-FORMS').find('> li:not(.deleted)').each(function (i) {
                    var $rem = $(this).find(".supplier-lodging-info select").find(":selected").val();
                    if($($verso).find(".supplier-lodging-info select").find(":selected").val() != $rem){
                        $($verso).find(".supplier-lodging-info select option[value='"+$rem+"']").hide();
                    }
                });
                */

                if(i>0){
                    $($verso).find("li.cost-price-info input").change(function () {
                        $cost = $($verso).find("li.cost-price-info input").val();
                        $percent = $($verso).find("li.profit-margin-info input").val();
                        $type = $($verso).find("li.marging-rate-info select").val();
                        $($verso).find("li.sale-price-info input").prop('readonly', true).val(getPercentVal($cost, $percent, $type));
                    }).trigger("change");

                    $($verso).find("li.profit-margin-info input").change(function () {
                        $cost = $($verso).find("li.cost-price-info input").val();
                        $percent = $($verso).find("li.profit-margin-info input").val();
                        $type = $($verso).find("li.marging-rate-info select").val();
                        $($verso).find("li.sale-price-info input").prop('readonly', true).val(getPercentVal($cost, $percent, $type));
                    }).trigger("change");

                    $($verso).find("li.marging-rate-info select").change(function () {
                        $cost = $($verso).find("li.cost-price-info input").val();
                        $percent = $($verso).find("li.profit-margin-info input").val();
                        $type = $($verso).find("li.marging-rate-info select").val();
                        $($verso).find("li.sale-price-info input").prop('readonly', true).val(getPercentVal($cost, $percent, $type));
                    }).trigger("change");
                }
            });
        });

    }
});