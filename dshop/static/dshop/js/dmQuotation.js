/* ======================================================== //
// ===---    dmQuotation Scripts                     ---=== //
// ======================================================== */

$(document).ready(function() {
    setQuotationClickBtn()
})

function setQuotationClickBtn() {  
    $(".dm-add2quotation-variant").on("click", function(event) {
      event.preventDefault()
      dm_add2quotation_variant(this)
    })
}

function setCookie(name, value) {
    document.cookie = name + "=" + value;
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function openModal(items) {
    html = ""
    for(var i=0; i < items.length; i++){
        html += "<tr><td>" + items[i].product_name + "</td>"
        html += "<td>" + items[i].variant_attribute + "</td>"
        html += "<td><input type='number' id="+items[i].id+" value=" + items[i].quantity + "></td></tr>"
        html += "<td><button>Update</button></td>"
        html += "<td><button>Delete</button></td>"
    }
    $('.quotation-modal-body').append("<table>" + html + "</table>")
    $('#quotation-item-modal').modal('show');
}

/* ===--------------------------------------------------=== */

function dm_add2quotation_variant(k) {
    let variant = $(k).data("variant")
    let quantity = 1
    if ($(".input-num").length) {
        quantity = $(".input-num").val()
    }
    cookie_val = getCookie('quotation-cookie')
    if (!cookie_val){
        var cookie_val = 'id' + (new Date()).getTime();
        setCookie('quotation-cookie', cookie_val)
    }
    $.post("/quotation/cart/?variant=" + variant + "&quantity=" + quantity + "&cookie=" + cookie_val, function(getResult) {
        alert(getResult);
    })
}