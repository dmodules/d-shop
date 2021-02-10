/* ======================================================== //
// ===---    dmQuotation Scripts                     ---=== //
// ======================================================== */

$(document).ready(function() {
    setQuotationClickBtn();
    getQuotationCart();
})

function setQuotationClickBtn() {  
    $(".dm-add2quotation-variant").on("click", function(event) {
      event.preventDefault();
      dm_add2quotation_variant(this);
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

/* ===--------------------------------------------------=== */

function getQuotationCart() {
    $.get("/quotation/current/", function(getResult) {
        if (getResult.quotation && getResult.quotation.items) {
            $("#dm-cart-items").show()
            $("#dm-cart-items").text(getResult.quotation.items.length)
            if (getResult.quotation.items.length > 1) {
                $("#drawer-quotation-items-count").text(getResult.quotation.items.length + " " + i18n.products[lang])
            } else {
                $("#drawer-quotation-items-count").text(getResult.quotation.items.length + " " + i18n.product[lang])
            }
            if (getResult.quotation.items.length >= 1) {
                let items = getResult.quotation.items.sort(
                    (a,b) => (
                        a.product_name > b.product_name
                    ) ? 1 : (
                        (
                            b.product_name > a.product_name
                        ) ? -1 : 0
                    )
                )
                let itemlist = "<ul>"
                items.forEach((item) => {
                    itemlist += "<li>"
                    itemlist += "<div class='container-fluid'><div class='row'>"
                    itemlist += "<div class='col-3'>"
                    itemlist += ""
                    itemlist += "</div>"
                    itemlist += "<div class='col-8 text-left'>"
                    itemlist += "<div><a href='"+"(url)"+"'>" + item.product_name + "</a></div>"
                    if (item.extra && item.extra.variables && item.extra.variables.attributes) {
                        itemlist += "<div class='drawer-cart-attributes'>"
                        for (let i = 0; i < item.extra.variables.attributes.length; i++) {
                            itemlist += "<div>"+item.extra.variables.attributes[i]+"</div>"
                        }
                        itemlist += "</div>"
                    }
                    itemlist += "<div class='mt-2'>"
                    itemlist += "<div class='cart-change-quantity'><span class='minus"
                    if (item.quantity <= 1) {
                        itemlist += " disabled'"
                    } else {
                        itemlist += "' onclick='return dm_minus2cart($(this), "+item.id+", "+item.product+", "+(item.quantity-1)+")'"
                    }
                    itemlist += ">-</span>"+item.quantity+"<span class='plus' onclick='return dm_plus2cart($(this), "+item.id+", "+item.product+", "+(item.quantity+1)+")'>+</span></div></div>"
                    itemlist += "<a href='#' class='dm-item-delete' onclick='return dm_delete2cart("+item.id+")'>X</a>"
                    itemlist += "</div>"
                    itemlist += "</div></div>"
                    itemlist += "</li>"
                    $("#drawer-quotation-items-list").html(itemlist)
                })
                itemlist += "</ul>"
                $(".btn-order").removeClass("disabled")
            } else {
                $("#dm-cart-items").hide()
                $("#dm-cart-items").text("0")
                $("#drawer-quotation-items-count").text("0 " + i18n.product[lang])
                $("#drawer-quotation-items-list").html('')
                $(".btn-order").addClass("disabled")
            }
            $("#dm-drawer-price").text(getResult.subtotal)
        } else {
            $("#dm-cart-items").hide()
            $("#dm-cart-items").text("0")
            $("#drawer-items-count").text("0 " + i18n.product[lang])
            $("#drawer-items-list").html('')
            $("#dm-drawer-price").text("-")
            $(".btn-order").addClass("disabled")
        }
    })
}
