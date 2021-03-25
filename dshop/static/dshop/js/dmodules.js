/* ======================================================== //
// ===---    D-Boutique Scripts                      ---=== //
// ======================================================== */

const site = "/"+document.documentElement.lang+"/"
const shop = "/shop/api/"
const auth = "/shop/auth/"

const lang = $('html')[0].lang

const i18n = {
  product: {
    fr: "produit",
    en: "product"
  },
  products: {
    fr: "produits",
    en: "products"
  },
  productaddedtocart: {
      fr: "Produit ajouté au panier",
      en: "Product added to cart"
  },
  quantitymaxreach: {
      fr: "Produits ajoutés partiellement au panier; maximum atteint",
      en: "Products partially added to cart; maximum reach"
  },
  productoutofstock: {
      fr: "Produit en rupture de stock",
      en: "Product out of stock"
  },
  voirplus: {
    fr: "Voir plus",
    en: "See more"
  },
  anerroroccurred: {
      fr: "Une erreur est survenue, veuillez réessayez plus tard.",
      en: "An error occurred, please try again later."
  },
  discounted: {
      fr: "Promotion",
      en: "Discounted"
  },
  outofstock: {
      fr: "Rupture de stock",
      en: "Out of Stock"
  },
  exhausted: {
      fr: "Épuisé",
      en: "Exhausted"
  },
  empty: {
      fr: "Vide",
      en: "Empty"
  },
  infolettresuccess: {
      fr: "Vous avez été ajouté avec succès à notre infolettre.",
      en: "You've been successfully added to our newsletter."
  },
  infolettrealready: {
      fr: "Vous êtes déjà inscrit à cette infolettre.",
      en: "You're already subscribed to this newsletter."
  },
  infolettrewrong: {
      fr: "Votre réponse est erronée.",
      en: "Your answer is wrong."
  },
  infolettreerror: {
      fr: "Une erreur est survenue, désolé.",
      en: "Something went wrong, sorry."
  },
  cantloginwithinfos: {
      fr: "Impossible de se connecter avec les informations d'identification fournies.",
      en: "Unable to log in with provided credentials."
  },
  productaddedtoquotation: {
      fr: "Produit ajouté au devis",
      en: "Product added to quotation"
  },
  xofx: {
      fr: "de",
      en: "of"
  }
}

$.ajaxSetup({headers: { "X-CSRFToken": $("meta[name='csrf-token']").attr("content") }})

//* ===--- Cookies ---=== *//

function dmGetCookie(cname) {
    var name = cname + "="
    var decodedCookie = decodeURIComponent(document.cookie)
    var ca = decodedCookie.split(';')
    for(var i = 0; i <ca.length; i++) {
      var c = ca[i]
      while (c.charAt(0) == ' ') {
        c = c.substring(1)
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length)
      }
    }
    return ""
}


function dmSetCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

//* ===--- Main ---=== *//

$(document).ready(function() {
  setClickBtn()
})

function setClickBtn() {
    $("#dm-productlist-sortby").on("change", function(event) {
        event.preventDefault()
        dmDoProductsSortBy(this)
    })

    $(".dm-add2cart").on("click", function(event) {
        event.preventDefault()
        dm_add2cart(this)
    })

    $(".dm-add2cart-variant").on("click", function(event) {
        event.preventDefault()
        dm_add2cart_variant(this)
    })

  $(".dm-variants-select select").on("change", function(event) {
      dm_selectvariant();
  })
      
  $(".down-arrow").on("click", function() {quantityMinus()})
  $(".up-arrow").on("click", function() {quantityPlus()})
}

function quantityExact() {
    $(".btn-add2cart").data("quantity", $(".input-num").val())
}

function quantityMinus() {
  if ($(".input-num").val() > parseInt($(".input-num").attr('min'))) {
    $(".input-num").val(+$(".input-num").val() - 1)
    $(".btn-add2cart").data("quantity", $(".input-num").val())
  }
}

function quantityPlus() {
  if ($(".input-num").val() < parseInt($(".input-num").attr('max').replace(',','').replace('.',''))) {
    $(".input-num").val(+$(".input-num").val() + 1)
    $(".btn-add2cart").data("quantity", $(".input-num").val())
  }
}

function dm_selectvariant () {
    let pk = $(".dm-variants-select").data("product")
    let attrs = []
    // ===---
    $(".dm-variants-select select").each(function (item) {
        attrs.push($(this)[0].value.replace(",", "//comma//"))
    })
    // ===---
    let price = "-"
    let dprice = "-"
    // ===---
    $.get("/api/fe/load-variant/?product="+pk+"&attributes="+encodeURIComponent(attrs), function(getResult) {
        if (getResult.variants.length > 0) {
            if (getResult.variants[0].quotation == 1){
                $(".btn-add2quotation").removeClass("disabled")
                $(".btn-add2quotation").data("variant", getResult.variants[0].product_code)
            } else {
                $(".btn-add2cart").removeClass("disabled")
                $(".btn-add2cart").data("variant", getResult.variants[0].product_code)
                price = getResult.variants[0].unit_price
                dprice = getResult.variants[0].real_price
                if (price != dprice) {
                    $(".product_price").html("<span class=\"price\">"+dprice+"</span><del>"+price+"</del>")
                } else {
                    $(".product_price").html("<span class=\"price\">"+price+"</span>")
                }
                if (getResult.variants[0].is_discounted) {
                    $(".product_title .variant-tag").html("<span class='product-detail-discounted'>"+i18n.discounted[lang]+"</span>")
                } else {
                    $(".product_title .variant-tag").html("")
                }
                if (getResult.variants[0].quantity > 0) {
                    $(".cart-product-quantity").show()
                    $(".cart_btn").show()
                    $(".product-detail-unavailable").hide()
                } else {
                    $(".cart-product-quantity").hide()
                    $(".cart_btn").hide()
                    $(".product-detail-unavailable").show()
                }
            }
            // ===---
            if ($(".slick-slide > .product_gallery_item").length) {
                $(".slick-slide > .product_gallery_item").removeClass("active")
                let varitem = $(".slick-slide > .product_gallery_item[data-variant='"+getResult.variants[0].product_code+"']")
                if (varitem.length) {
                    varitem.addClass("active")
                    $("#product_img").attr("src", varitem.data("image"))
                    $("#product_img").data("zoomImage", varitem.data("zoomImage"))
                    $(".zoomContainer .zoomWindowContainer > div").css("background-image", "url("+varitem.data("zoomImage")+")")
                } else {
                    $(".slick-slide > .product_gallery_item").first().addClass("active")
                    $("#product_img").attr("src", $(".slick-slide > .product_gallery_item").first().data("image"))
                    $("#product_img").data("zoomImage", $(".slick-slide > .product_gallery_item").first().data("zoomImage"))
                    $(".zoomContainer .zoomWindowContainer > div").css("background-image", "url("+$(".slick-slide > .product_gallery_item").first().data("zoomImage")+")")
                }
            }
            // ===---
        } else {
            $(".btn-add2cart").addClass("disabled")
            $(".product_price").html("<span class=\"price\">&nbsp;</span>")
            $(".product_title .variant-tag").html("")
            $(".cart-product-quantity").hide()
            $(".cart_btn").hide()
            $(".product-detail-unavailable").show()
        }
    })
}

function showAdd2cartSnack(text = i18n.productaddedtocart[lang]) {
  $('#snackbar').text(text)
  $('#snackbar').addClass('show')
  setTimeout(function () {
    $('#snackbar').removeClass('show')
  }, 3000)
}

function dm_add2cart(k) {
  let endpoint = $(k).data("product")
  let quantity = 1
  if ($(k).data("quantity")) {
    quantity = $(k).data("quantity")
  }
  $.get(site + "produits/" + endpoint + "/add-to-cart", function(getResult) {
    if (getResult.availability.quantity > 0) {
        if (getResult.availability.quantity >= quantity) {
            getResult.product_code = getResult.product_code.toString()
            getResult.quantity = quantity
            $.post(shop + "cart/", getResult, function() {
                showAdd2cartSnack()
                getPanier()
            })
        } else {
            getResult.product_code = getResult.product_code.toString()
            getResult.quantity = quantity
            $.post(shop + "cart/", getResult, function() {
                showAdd2cartSnack(i18n.quantitymaxreach[lang])
                getPanier()
            })
        }
    } else {
        showAdd2cartSnack(i18n.productoutofstock[lang])
    }
  })
}

function dm_add2cart_variant(k) {
  let endpoint = $(k).data("product")
  let variant = $(k).data("variant")
  let quantity = 1
  if ($(k).data("quantity")) {
    quantity = $(k).data("quantity")
  }
  if (variant) {
    $.get(site + "produits/" + endpoint + "/add-productvariable-to-cart?product_code="+variant, function(getResult) {
        if (getResult.availability.quantity > 0) {
            if (getResult.availability.quantity >= quantity) {
                getResult.quantity = quantity
                getResult.product_code = variant
                $.post(shop + "cart/", getResult, function() {
                    showAdd2cartSnack()
                    getPanier()
                })
            } else {
                getResult.quantity = quantity
                getResult.product_code = variant
                $.post(shop + "cart/", getResult, function() {
                    showAdd2cartSnack(i18n.quantitymaxreach[lang])
                    getPanier()
                })
            }
        } else {
            showAdd2cartSnack(i18n.productoutofstock[lang])
        }
    })
  }
}

function dm_delete2cart(endpoint) {
  $.ajax({
    url: shop + "cart/" + endpoint,
    type: "DELETE",
    success: function() {
      getPanier()
    }
  })
  return false
}

function dm_minus2cart(button, endpoint, pk, qty) {
    if ($(button).hasClass("disabled")) {
        return false
    } else {
        $(button).addClass("disabled")
        let datas = {
            product: pk,
            quantity: qty
        }
        $.ajax({
            url: shop + "cart/" + endpoint,
            type: "PUT",
            data: datas,
            success: function(getResult) {
                getPanier()
            }
        })
    return false
    }
}

function dm_plus2cart(button, endpoint, pk, qty) {
    if ($(button).hasClass("disabled")) {
        return false
    } else {
        $(button).addClass("disabled")
        let datas = {
            product: pk,
            quantity: qty
        }
        $.ajax({
            url: shop + "cart/" + endpoint,
            type: "PUT",
            data: datas,
            success: function(getResult) {
                if (getResult.cart_item.quantity < datas.quantity) {
                    showAdd2cartSnack(i18n.quantitymaxreach[lang])
                }
                getPanier()
            }
        })
    return false
    }
}

function getPanier() {
    if ($("#drawer-items-list").length) {
        $.get(shop + "cart/", function(getResult) {
            if (getResult.num_items) {
                $("#dm-cart-items").show()
                $("#dm-cart-items").text(getResult.total_quantity)
                if (getResult.num_items > 1) {
                    $("#drawer-items-count").text(getResult.num_items + " " + i18n.products[lang])
                } else {
                    $("#drawer-items-count").text(getResult.num_items + " " + i18n.product[lang])
                }
                if (getResult.items.length >= 1) {
                    let items = getResult.items.sort(
                        (a,b) => (
                            a.summary.product_name > b.summary.product_name
                        ) ? 1 : (
                            (
                                b.summary.product_name > a.summary.product_name
                            ) ? -1 : 0
                        )
                    )
                    let itemlist = "<ul>"
                    items.forEach((item) => {
                        itemlist += "<li>"
                        itemlist += "<div class='container-fluid'><div class='row'>"
                        itemlist += "<div class='col-3'>"
                        itemlist += item.summary.media
                        itemlist += "</div>"
                        itemlist += "<div class='col-8 text-left'>"
                        itemlist += "<div><a href='"+item.summary.product_url+"'>" + item.summary.product_name + "</a></div>"
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
                            itemlist += "' onclick='return dm_minus2cart($(this), "+JSON.stringify(item.url.split("/cart/")[1])+", "+item.product+", "+(item.quantity-1)+")'"
                        }
                        itemlist += ">-</span>"+item.quantity+"<span class='plus' onclick='return dm_plus2cart($(this), "+JSON.stringify(item.url.split("/cart/")[1])+", "+item.product+", "+(item.quantity+1)+")'>+</span></div>"
                        itemlist += " x " + item.unit_price + "</div>"
                        itemlist += "<a href='#' class='dm-item-delete' onclick='return dm_delete2cart("+JSON.stringify(item.url.split("/cart/")[1])+")'>X</a>"
                        itemlist += "</div>"
                        itemlist += "</div></div>"
                        itemlist += "</li>"
                        $("#drawer-items-list").html(itemlist)
                    })
                    itemlist += "</ul>"
                    $(".btn-order").removeClass("disabled")
                } else {
                    $("#dm-cart-items").hide()
                    $("#dm-cart-items").text("0")
                    $("#drawer-items-count").text("0 " + i18n.product[lang])
                    $("#drawer-items-list").html('')
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
}

/* ======================================================== //
// ===---    Produits Scripts                        ---=== //
// ======================================================== */

//* ===--- Sort By ---=== *//
function dmDoProductsSortBy () {
    let current = $("#dm-productlist-sortby option:selected").val()
    dmSetCookie("dm_psortby", current)
    location.reload()
    $(document).scrollTop(0)
}

//* ===---   Filtres   ---=== *//

$('.filters-box').on('change', function( ){
  if ($(this).children('input').attr('name') !== 'tous') {
    $('.filters-box.dm-tous').removeClass('checked')
    $('.filters-box.dm-tous').children('input').prop("checked", false)
  } else {
    $('.filters-box:not(.dm-tous)').removeClass('checked')
    $('.filters-box:not(.dm-tous)').children('input').prop("checked", false)
  }
  //
  if ($(this).hasClass('checked')) {
    $(this).removeClass('checked')
  } else {
    $(this).addClass('checked')
  }
  //
  doProductsByFilters()
})

function doProductsByFilters() {
  $('.shop_container .produit').hide()
  $('.filters-box').each(function() {
    if ($(this).children('input').prop('checked')) {
      showProduit($(this).children('input').attr('name'))
    }
  })
}

function showProduit(filter) {
  $('.shop_container .produit').each(function() {
    if ($(this).data('filters').indexOf(filter) >= 0) {
      $(this).show()
    }
  })
}

/* ===---   Toggle Menu Category (deprecated)   ---=== */

function toggleMenuCategory (btn) {
  $('.dm-produits-category-submenu').hide()
  if ($(btn).text() === '+') {
    $('.dm-produits-category-haschildren .toggle').text('+')
    $(btn).next().show()
    $(btn).text('-')
  } else {
    $('.dm-produits-category-haschildren .toggle').text('+')
    $(btn).next().hide()
    $(btn).text('+')
  }
}

/* ===---   Toggle Menu Filtering   ---=== */

function toggleMenuFiltering (btn) {
    if ($(btn).text() === '+') {
        $(btn).next().show()
        $(btn).text('-')
    } else if ($(btn).text() === '-') {
        $(btn).next().hide()
        $(btn).text('+')
    }
}

function toggleMenuFilteringChecked () {
    if ($(".dmfilters-list").length) {
        let content = $(".dmfilters-list .dmfilters-list-submenu")
        content.each(function() {
            $(this).children().children().children().each(function() {
                if ($(this).prop('checked')) {
                    let p = $(this).parent().parent().parent(".dmfilters-list-submenu")
                    toggleMenuFiltering(p.siblings(".toggle"))
                }
            })
        })
    }

}

function toggleMenuFilteringMobile(resize = false) {
    if ($(".dmfilters-list").length) {
        if ($(window).width() > 767) {
            $(".dmfilters-list").show()
        } else if (resize) {
            $(".dmfilters-list").hide()
        } else {
            $(".dmfilters-list").toggle()
        }
    }
}

function dmFilterURL(){
    url = window.location.href;
    url = url.split("?")[0];
    /**/
    brands = ""
    $('[id^="brand_"]').each(function(i, obj) {
        if (obj.name && obj.checked){
            if (brands) {
                brands +=  "," + obj.name
            } else {
                brands += obj.name
            }
        }
    });
    if (brands) {
        brands = "brand=" + brands
    }
    /**/
    categories = ""
    $('[id^="category_"]').each(function(i, obj) {
        if (obj.name && obj.checked){
            if (categories) {
                categories +=  "," + obj.name
            } else {
                categories += obj.name
            }
        }
    });
    if (categories) {
        categories = "category=" + categories
    }
    /**/
    filters = ""
    $('[id^="filter_"]').each(function(i, obj) {
        if (obj.name && obj.checked){
            if (filters) {
                filters +=  "," + obj.name
            } else {
                filters += obj.name
            }
        }
    });
    if (filters) {
        filters = "filter=" + filters
    }
    /**/
    attributes = ""
    $('[id^="attribute_"]').each(function(i, obj) {
        if (obj.name && obj.checked){
            if (attributes) {
                attributes +=  "," + obj.name
            } else {
                attributes += obj.name
            }
        }
    });
    if (attributes) {
        attributes = "attribute=" + attributes
    }
    /**/
    return [url, filters, attributes, categories, brands]
}

function dmApplyFilter(){
    data = dmFilterURL()
    new_url = data[0]
    if (data[1] || data[2] || data[3] || data[4]) {
        new_url += "?"
    }
    let filterings = ""
    if (data[1]) {
        filterings += data[1]
    }
    if (data[2]) {
        if (filterings && !filterings.endsWith("&")) {
            filterings += "&"
        }
        filterings += data[2]
    }
    if (data[3]) {
        if (filterings && !filterings.endsWith("&")) {
            filterings += "&"
        }
        filterings += data[3]
    }
    if (data[4]) {
        if (filterings && !filterings.endsWith("&")) {
            filterings += "&"
        }
        filterings += data[4]
    }
    new_url += filterings
    window.location = new_url
}

/* ======================================================== //
// ===---    Site Scripts                            ---=== //
// ======================================================== */

window.addEventListener('resize', () => {
    mobilevh()
    toggleMenuFilteringMobile(true)
    $(".dm-main-submenu.show").removeClass("show")
    $(".dm-menu-toggle.active").removeClass("ion-ios-arrow-down")
    $(".dm-menu-toggle.active").addClass("ion-ios-arrow-right")
    $(".dm-menu-toggle.active").removeClass("active")
});

window.addEventListener('scroll', () => {
    stickyMenu()
});

$(document).ready(function() {
  mobilevh()
  checkInfolettre()
  /* ===--- ---=== */
  if ($('.dm-drawer').length) {
    $('.drawer').drawer({
      class: {
        nav: 'drawer-nav',
        toggle: 'drawer-toggle',
        overlay: 'drawer-overlay',
        open: 'drawer-open',
        close: 'drawer-close',
        dropdown: 'drawer-dropdown'
      },
      iscroll: {
          preventDefault: true,
          click: false,
      }
    })
    $(window).off('resize.drawer');
    getPanier();
  }
  /* ===--- ---=== */
  if ($('#cms-top').length && $('#tophead').length) {
    $('html').css({"margin-top":"0"});
    $('body').css({"padding-top":"0"});
    $('.drawer-nav').css({
        "height":"calc(var(--vh, 1vh) * 100 - 46px)",
        "top":"46px"
    });
  } else if ($('#tophead').length) {
    $('html').css({"margin-top":"0"});
    $('body').css({"padding-top":"0"});
    $('.drawer-nav').css({
        "height":"calc(var(--vh, 1vh) * 100)",
        "top":"0"
    });
  }
  /* ===--- ---=== */
  if ($('#app-checkout').length) {
    $('.drawer-toggle.dm-cart').hide()
  } else {
    $('.drawer-toggle.dm-cart').show()
  }
    /* ===--- ---=== */
    if ($(".contact-same-height").length) {
        let maxh = null
        $(".contact-same-height").each(function () {
            h = $(this)[0].clientHeight
            if (h > maxh || maxh == null) {
                maxh = h
            }
            $(this).css("height", maxh)
        })
    }
    /* ===--- ---=== */
    $(document).mouseup(function(e) {
        if ($("#topsearch").hasClass("show")) {
            if ($("#topsearch").is(e.target)) {
                toggleSearch()
            }
        } else if ($("body").hasClass("drawer-open")) {
            if ($(".drawer-overlay").is(e.target)) {
                $(".drawer").drawer("close")
                $(".dm-panel-user").removeClass("dm-panel-user")
                $(".dm-panel-cart").removeClass("dm-panel-cart")
            }
        }
   })
    $(document).keyup(function(e) {
        if ($("#topsearch").hasClass("show")) {
            if (e.key === "Escape") {
                toggleSearch()
            } else if (e.key === "Enter") {
                doSearch("#q")
            }
        } else if ($("body").hasClass("drawer-open")) {
            if (e.key === "Escape") {
                $(".drawer").drawer("close")
                $(".dm-panel-user").removeClass("dm-panel-user")
                $(".dm-panel-cart").removeClass("dm-panel-cart")
            }
        }
   })
   /* ===--- ---=== */
   if ($("#dm-productlist-sortby").length) {
    let cookie_sortby = dmGetCookie("dm_psortby")
    if (cookie_sortby) {
        $("#dm-productlist-sortby").children(".sb-"+cookie_sortby).prop("selected", true)
    }
   }
   /* ===--- ---=== */
   /* ===--- Apply filter---=== */
    var urlParams;
    (window.onpopstate = function () {
        var match,
            pl     = /\+/g,  // Regex for replacing addition symbol with a space
            search = /([^&=]+)=?([^&]*)/g,
            decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
            query  = window.location.search.substring(1);

        urlParams = {};
        while (match = search.exec(query))
            urlParams[decode(match[1])] = decode(match[2]);
    })();
    if (urlParams['filter']) {
        filters = urlParams['filter'].split(",")
        filters.forEach(function (item, index) {
            if (item){
                $("[id=filter_" + item+"]")[0].checked=true
            }
        });
    }
    if (urlParams['attribute']) {
        attributes = urlParams['attribute'].split(",")
        attributes.forEach(function (item, index) {
            if (item){
                $("[id=attribute_" + item+"]")[0].checked=true
            }
        });
    }
    if (urlParams['brand']) {
        attributes = urlParams['brand'].split(",")
        attributes.forEach(function (item, index) {
            if (item){
                $("[id=brand_" + item+"]")[0].checked=true
            }
        });
    }
    if (urlParams['category']) {
        attributes = urlParams['category'].split(",")
        attributes.forEach(function (item, index) {
            if (item){
                $("[id=category_" + item+"]")[0].checked=true
            }
        });
    }
    toggleMenuFilteringChecked()
});

function mobilevh () {
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}

function checkInfolettre () {
    var urlParams = window.location.search
    if (urlParams == '?infolettre=success') {
        showAdd2cartSnack(i18n.infolettresuccess[lang])
    } else if (urlParams == '?infolettre=already') {
        showAdd2cartSnack(i18n.infolettrealready[lang])
    } else if (urlParams == '?infolettre=wrong') {
        showAdd2cartSnack(i18n.infolettrewrong[lang])
    } else if (urlParams == '?infolettre=error') {
        showAdd2cartSnack(i18n.infolettreerror[lang])
    }

}

function dmDrawerTabUserLogin() {
  $('.dm-drawer-tabs-login .btn').addClass('disabled')
  $('.dm-drawer-tabs-register .btn').removeClass('disabled')
  $('.dm-drawer-logs-login').show()
  $('.dm-drawer-logs-register').hide()
  return false
}

function dmDrawerTabUserRegister() {
  $('.dm-drawer-tabs-login .btn').removeClass('disabled')
  $('.dm-drawer-tabs-register .btn').addClass('disabled')
  $('.dm-drawer-logs-login').hide()
  $('.dm-drawer-logs-register').show()
  return false
}

function dmDrawerDoLogin() {
  $('.dm-drawer-logs-login-error').hide()
  let datas = {
    form_data: {
      email: $('#dm-drawer-form-login-email').val(),
      password: $('#dm-drawer-form-login-password').val()
    }
  }
  $.ajax({
    url: auth + "login/",
    type: "POST",
    data: JSON.stringify(datas),
    contentType: "application/json;charset=UTF-8",
    success: function() {
      window.location = '/'
      if(typeof(quotationMerge) === typeof(Function)) {
          quotationMerge()
      }
    }
  }).fail(function(failResult) {
    $('.dm-drawer-logs-login-error').show()
    $('.dm-drawer-logs-login-error').html(i18n.anerroroccurred[lang])
    if (failResult.status == 500) {
        $('.dm-drawer-logs-login-error').html(i18n.cantloginwithinfos[lang])
        $.ajax({
            url: "/api/fe/send-unclone/",
            type: "POST",
            data: JSON.stringify(datas),
            contentType: "application/json;charset=UTF-8"
        })
    } else if (failResult.responseJSON) {
      if (failResult.responseJSON.login_form) {
        if (failResult.responseJSON.login_form.email) {
          $('.dm-drawer-logs-login-error').html('Courriel : ' + failResult.responseJSON.login_form.email[0])
        } else if (failResult.responseJSON.login_form.password) {
          $('.dm-drawer-logs-login-error').html('Mot de passe : ' + failResult.responseJSON.login_form.password[0])
        } else if (failResult.responseJSON.login_form.non_field_errors) {
          $('.dm-drawer-logs-login-error').html(failResult.responseJSON.login_form.non_field_errors[0])
        }
      }
    }
  })
  return false
}

function dmDrawerDoRegister() {
  $('.dm-drawer-logs-register-error').hide()
  let datas = {
    form_data: {
      email: $('#dm-drawer-form-register-email').val(),
      password1: $('#dm-drawer-form-register-password1').val(),
      password2: $('#dm-drawer-form-register-password2').val()
    }
  }
  $.ajax({
    url: auth + "register/",
    type: "POST",
    data: JSON.stringify(datas),
    contentType: "application/json;charset=UTF-8",
    success: function() {
      window.location = '/'
      if(typeof(quotationMerge) === typeof(Function)) {
          quotationMerge()
      }
    }
  }).fail(function(failResult) {
    $('.dm-drawer-logs-register-error').show()
    $('.dm-drawer-logs-register-error').html('Une erreur est survenue, veuillez réessayez plus tard.')
    if (datas.form_data.email === "") {
      $('.dm-drawer-logs-register-error').html('Courriel : Ce champs est requis.')
    }
    if (datas.form_data.password1 === "" || datas.form_data.password2 === "") {
      $('.dm-drawer-logs-register-error').html('Mot de passe : Ce champs est requis.')
    }
    if (failResult.responseJSON) {
      if (failResult.responseJSON.register_user_form) {
        if (failResult.responseJSON.register_user_form.__all__) {
          $('.dm-drawer-logs-register-error').html(failResult.responseJSON.register_user_form.__all__[0].replace('\n','<br />'))
        } else if (failResult.responseJSON.login_form.password) {
          $('.dm-drawer-logs-register-error').html('Mot de passe : ' + failResult.responseJSON.login_form.password[0])
        }
      }
    }
  })
  return false
}

function dmDrawerDoLogout() {
  $.ajax({
    url: auth + "logout/",
    type: "POST",
    data: {},
    contentType: "application/json;charset=UTF-8",
    success: function() {
      window.location = '/'
      if(typeof(setCookie) === typeof(Function)) {
        setCookie('quotation-cookie', '')
      }

    }
  })
  return false
}

/* ===--- Main Menu ---=== */

function toggleMainMenu() {
    $(".tophead-botnav").toggle()
}

function toggleSubmenu(e) {
    if (e.siblings(".dm-main-submenu").hasClass("show")) {
        e.removeClass("active")
        if (!e.siblings(".dm-main-submenu").hasClass("sub")) {
            e.removeClass("ion-ios-arrow-down")
            e.addClass("ion-ios-arrow-right")
        }
        e.siblings(".dm-main-submenu").removeClass("show")
    } else {
        e.addClass("active")
        if (!e.siblings(".dm-main-submenu").hasClass("sub")) {
            e.removeClass("ion-ios-arrow-right")
            e.addClass("ion-ios-arrow-down")
        }
        e.siblings(".dm-main-submenu").addClass("show")
    }
}

function stickyMenu() {
    if ($(window).scrollTop() >= 500) {
        $(".tophead-botnav").addClass("sticky")
    } else {
        $(".tophead-botnav").removeClass("sticky")
    }
}

/* ===--- Search ---=== */

function doSearch(id = "#qs") {
    let query = ""
    if ($(id).length) {
        query = $(id).val()
    }
    if (query !== "") {
        window.location = "/search/?q="+query
    }
    return false
}

function toggleSearch() {
    if ($("#topsearch").hasClass("show")) {
        $("#topsearch").removeClass("visible")
        setTimeout(function () {
            $("#topsearch").removeClass("show")
        }, 100)
    } else {
        $("#topsearch").addClass("show")
        setTimeout(function () {
            $("#topsearch").addClass("visible")
        }, 100)
    }
}

/* ===--- Advertising: Popup ---=== */
function dmClosePopup(popup, cookie = 0) {
    $("#dmadvertising-popup").hide()
    if (cookie === 1) {
        dmSetCookie("dm_popad_"+popup, 1, 30)
    }
}

//* ===---   Load More   ---=== *//

function loadMoreProduits(what = null, search = null) {
    let offset = $('.dm-btn-more').data('offset')
    let limit = $('.dm-btn-more').data('limit')
    let cookie_sortby = dmGetCookie("dm_psortby")
    let query = ''
    data = dmFilterURL()
    if (search == 'category') {
      query = '&category='+what
    } else if (search == 'brand') {
      query = '&brand='+what
    }
    // ===---
    //$.get("/api/fe/moreproduits/?offset="+offset+'&limit='+limit+'&sortby='+cookie_sortby+query, function(getResult) {
    $.get("/fr/produits/?type=1&"+data[1]+"&"+data[2]+"&"+data[3]+"&"+data[4]+"&offset="+offset+'&limit='+limit+'&sortby='+cookie_sortby+query, function(getResult) {
      let r = ''
      getResult.products.forEach((product) => {
        r = ''
        r += '<div class="produit col-md-4 col-6" data-filters="tous'
        if (product.filters) {
          r += ' ' + product.filters
        }
        r += '">'
        r += '<div class="product">'
        r += '<div class="product_img">'
        r += '<a href="'+product.url+'">'
        if (product.image) {
          r += '<img src="'+product.image+'" alt="" class="img-fluid">'
        } else {
          r += '<img src="https://via.placeholder.com/540x600/f7f8fb/f7f8fb" alt="" class="img-fluid">'
        }
        r += '</a>'
        r += '<div class="product_action_box">'
        r += '<ul class="list_none pr_action_btn">'
        r += '<li>'
        r += '<a href="'+product.url+'"><i class="ti-info-alt"></i></a>'
        r += '</li>'
        if (!product.variants && product.quantity > 0) {
            r += '<li>'
            if (product.is_quotation) {
                r += '<a href="/" onclick="dm_add2quotation($(this)); return false" class="dm-add2cart btn" data-product="'+product.product_code+'"><i class="icon-basket-loaded"></i></a>'
            } else {
                r += '<a href="/" onclick="dm_add2cart($(this)); return false" class="dm-add2cart btn" data-product="'+product.slug+'"><i class="icon-basket-loaded"></i></a>'
            }
            r += '</li>'
        } else if (product.variants_count === 1) {
            r += '<li>'
            if (product.is_quotation) {
                r += '<a href="/" onclick="dm_add2quotation_variant($(this)); return false" data-product="'+product.variants_product_code+'" data-variant="'+product.variants_product_code+'"><i class="icon-basket-loaded"></i></a>'
            } else {
                r += '<a href="/" onclick="dm_add2cart_variant($(this)); return false" data-product="'+product.slug+'" data-variant="'+product.variants_product_code+'"><i class="icon-basket-loaded"></i></a>'
            }
            r += '</li>'
        }
        r += '</ul>'
        r += '</div>'
        if (product.label) {
            r += '<span class="product_sale_customlabel" style="background-color:'+product.label.bg_colour+';border-color:'+product.label.colour+';color:'+product.label.colour+';">'+product.label.name+'</span>'
        }
        r += '</div>'
        r += '<div class="product_info">'
        r += '<h6 class="product_title"><a href="'+product.url+'">'+product.name+'</a></h6>'
        if (!product.is_quotation) {
            r += '<div class="product_price">'
            r += '<span class="price">'+product.price+'</span>'
            if (product.price != product.realprice) {
                r += '<del>'+product.realprice+'</del>'
            }
            if (product.quantity <= 0) {
                r += '<span class="product_sale_outofstock">'+i18n.outofstock[lang]+'</span>'
            } else if (product.is_discounted) {
                r += '<span class="product_sale_discounted">'+i18n.discounted[lang]+'</span>'
            }
            r += '</div>'
        }
        r += '<div class="pr_desc">'
        r += '<p>'+product.caption+'</p>'
        r += '</div>'
        r += '<div class="list_product_action_box">'
        r += '<ul class="list_none">'
        r += '<button class="btn btn-fill-out" type="button" onclick="location.href=\''+product.url+'\';">'+i18n.voirplus[lang]+'</button>'
        r += '</ul>'
        r += '</div>'
        r += '</div>'
        r += '</div>'
        r += '</div>'
        $(".produits").append(r)
      })
      if (getResult.next === 0) {
        $('.dm-btn-more').hide()
      }
    }).then(function() {
      setClickBtn()
      //doProductsByFilters()
      $('.dm-btn-more').data('offset', offset + limit)
    })
    // ===---
    return false
}

//* ===---   Load Products By Category   ---=== *//

function loadMoreByCategory(cat, tab) {
    $.get("/api/fe/products-by-category/?category="+cat, function(getResult) {
        $('#tab'+tab+' .shop_container').html('')
        let r = ''
        if (getResult.products.length > 0) {
            getResult.products.forEach((product) => {
                r = ''
                r += '<div class="col-lg-3 col-md-4 col-6" id="produitno'+tab+'">'
                r += '<div class="product animated fadeInUp">'
                r += '<div class="product_img">'
                r += '<a href="'+product.url+'">'
                if (product.image) {
                    r += '<img src="'+product.image+'" alt="" class="img-fluid">'
                } else {
                    r += '<img src="https://via.placeholder.com/540x600/f7f8fb/f7f8fb" alt="" class="img-fluid">'
                }
                r += '</a>'
                r += '<div class="product_action_box">'
                r += '<ul class="list_none pr_action_btn">'
                r += '<li>'
                r += '<a href="'+product.url+'"><i class="ti-info-alt"></i></a>'
                r += '</li>'
                if (!product.variants && product.quantity > 0) {
                    r += '<li>'
                    if (product.is_quotation) {
                        r += '<a href="/" onclick="dm_add2quotation($(this)); return false" class="dm-add2cart btn" data-product="'+product.product_code+'"><i class="icon-basket-loaded"></i></a>'
                    } else {
                        r += '<a href="/" onclick="dm_add2cart($(this)); return false" class="dm-add2cart btn" data-product="'+product.slug+'"><i class="icon-basket-loaded"></i></a>'
                    }
                    r += '</li>'
                } else if (product.variants_count === 1) {
                    r += '<li>'
                    if (product.is_quotation) {
                        r += '<a href="/" onclick="dm_add2quotation_variant($(this)); return false" data-product="'+product.variants_product_code+'" data-variant="'+product.variants_product_code+'"><i class="icon-basket-loaded"></i></a>'
                    } else {
                        r += '<a href="/" onclick="dm_add2cart_variant($(this)); return false" data-product="'+product.slug+'" data-variant="'+product.variants_product_code+'"><i class="icon-basket-loaded"></i></a>'
                    }
                    r += '</li>'
                }
                r += '</ul>'
                r += '</div>'
                if (product.label) {
                    r += '<span class="product_sale_customlabel" style="background-color:'+product.label.bg_colour+';border-color:'+product.label.colour+';color:'+product.label.colour+';">'+product.label.name+'</span>'
                }
                r += '</div>'
                r += '<div class="product_info text-left">'
                r += '<h6 class="product_title"><a href="'+product.url+'">'+product.name+'</a></h6>'
                if (!product.is_quotation) {
                    r += '<div class="product_price">'
                    r += '<span class="price">'+product.price+'</span>'
                    if (product.price != product.realprice) {
                        r += '<del>'+product.realprice+'</del>'
                    }
                    if (product.quantity <= 0) {
                        r += '<span class="product_sale_outofstock">'+i18n.outofstock[lang]+'</span>'
                    } else if (product.is_discounted) {
                        r += '<span class="product_sale_discounted">'+i18n.discounted[lang]+'</span>'
                    }
                    r += '</div>'
                }
                r += '<div class="pr_desc">'
                r += '<p>'+product.caption+'</p>'
                r += '</div>'
                r += '<div class="list_product_action_box">'
                r += '<ul class="list_none">'
                r += '<button class="btn btn-fill-out" type="button" onclick="location.href=\''+product.url+'\';">'+i18n.voirplus[lang]+'</button>'
                r += '</ul>'
                r += '</div>'
                r += '</div>'
                r += '</div>'
                r += '</div>'
                $('#tab'+tab+' .shop_container').append(r)
            })
        } else {
            $('#tab'+tab+' .shop_container').append(i18n.empty[lang])
        }
    })
    .then()
}

/* ======================================================== //
// ===---    @ 2020 D-Modules                        ---=== //
// ======================================================== */
