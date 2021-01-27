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
  exhausted: {
      fr: "Épuisé",
      en: "Exhausted"
  },
  empty: {
      fr: "Vide",
      en: "Empty"
  }
}

$.ajaxSetup({headers: { "X-CSRFToken": $("meta[name='csrf-token']").attr("content") }})

$(document).ready(function() {
  setClickBtn()
})

function setClickBtn() {
  $(".dm-add2cart").on("click", function(event) {
    event.preventDefault()
    dm_add2cart(this)
  })

  $(".dm-add2cart-variant").on("click", function(event) {
    event.preventDefault()
    dm_add2cart_variant(this)
  })

  $(".dm-variants-select select").on("change", function(event) {
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
        } else {
            $(".btn-add2cart").addClass("disabled")
            $(".product_price").html("<span class=\"price\">&nbsp;</span>")
            $(".product_title .variant-tag").html("")
            $(".cart-product-quantity").hide()
            $(".cart_btn").hide()
            $(".product-detail-unavailable").show()
        }
    })
  })
      
  $(".down-arrow").on("click", function() {quantityMinus()})
  $(".up-arrow").on("click", function() {quantityPlus()})
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
  $.get(site + i18n.product[lang] + "/" + endpoint + "/add-to-cart", function(getResult) {
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
    $.get(site + i18n.product[lang] + "/" + endpoint + "/add-productvariable-to-cart?product_code="+variant, function(getResult) {
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

function getPanier() {
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
        let itemlist = "<ul>"
        getResult.items.forEach((item) => {
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
          itemlist += "<div>"+item.quantity+" x " + item.unit_price + "</div>"
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

/* ======================================================== //
// ===---    Produits Scripts                        ---=== //
// ======================================================== */

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

/* ===---   Toggle Menu Category   ---=== */

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

/* ======================================================== //
// ===---    Site Scripts                            ---=== //
// ======================================================== */

window.addEventListener('resize', () => {
    mobilevh()
});

function mobilevh () {
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}

$(document).ready(function() {
  mobilevh()
  if ($('.dm-drawer').length) {
    $('.drawer').drawer({
      class: {
        nav: 'drawer-nav',
        toggle: 'drawer-toggle',
        overlay: 'drawer-overlay',
        open: 'drawer-open',
        close: 'drawer-close',
        dropdown: 'drawer-dropdown'
      }
    })
    getPanier();
  }
  if ($('#cms-top').length && $('.topnav').length) {
    $('html').css({"margin-top":"0"});
    $('body').css({"padding-top":"46px"});
    $('.topnav').css({"top":"46px"});
    $('.drawer-overlay').css({"top":"92px"});
    $('.drawer-nav').css({
        "height":"calc(var(--vh, 1vh) * 100 - 92px)",
        "top":"92px"
    });
    $('.header_wrap.fixed-top').css({"top":"92px"});
  } else if ($('.topnav').length) {
    $('html').css({"margin-top":"0"});
    $('body').css({"padding-top":"46px"});
    $('.drawer-overlay').css({"top":"46px"});
    $('.drawer-nav').css({
        "height":"calc(var(--vh, 1vh) * 100 - 46px)",
        "top":"46px"
    });
    $('.header_wrap.fixed-top').css({"top":"46px"});
  } else if ($('#cms-top').length) {
    $('html').css({"margin-top":"0"});
    $('body').css({"padding-top":"46px"});
    $('.header_wrap.fixed-top').css({"top":"46px"});
  }
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
});

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
    }
  }).fail(function(failResult) {
    $('.dm-drawer-logs-login-error').show()
    $('.dm-drawer-logs-login-error').html(i18n.anerroroccurred[lang])
    if (failResult.responseJSON) {
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
    }
  })
  return false
}

/* ===--- Search ---=== */

function doSearch() {
    let query = $("#q").val()
    if (query) {
        window.location = "/search/?q="+query
    }
    return false
}

//* ===---   Load More   ---=== *//

function loadMoreProduits(what = null, search = null) {
    let offset = $('.dm-btn-more').data('offset')
    let limit = $('.dm-btn-more').data('limit')
    let query = ''
    if (search == 'category') {
      query = '&category='+what
    } else if (search == 'brand') {
      query = '&brand='+what
    }
    // ===---
    $.get("/api/fe/moreproduits/?offset="+offset+'&limit='+limit+query, function(getResult) {
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
          r += '<img src="https://via.placeholder.com/f7f8fb/f7f8fb" alt="" class="img-fluid">'
        }
        r += '</a>'
        r += '<div class="product_action_box">'
        r += '<ul class="list_none pr_action_btn">'
        r += '<li>'
        r += '<a href="'+product.url+'"><i class="ti-info-alt"></i></a>'
        r += '</li>'
        if (!product.variants && product.quantity > 0) {
          r += '<li>'
          r += '<a href="/" onclick="dm_add2cart($(this)); return false" class="dm-add2cart btn" data-product="'+product.slug+'"><i class="icon-basket-loaded"></i></a>'
          r += '</li>'
        }
        r += '</ul>'
        r += '</div>'
        r += '</div>'
        r += '<div class="product_info">'
        r += '<h6 class="product_title"><a href="'+product.url+'">'+product.name+'</a></h6>'
        r += '<div class="product_price">'
        if (product.variants) {
          r += '<span class="price">'+product.price+'</span>'
        } else {
          r += '<span class="price">'+product.price+'</span>'
          if (product.price != product.realprice) {
            r += '<del>'+product.realprice+'</del>'
          }
        }
        if (product.is_discounted) {
            r += '<span class="product_sale_discounted">'+i18n.discounted[lang]+'</span>'
        }
        r += '</div>'
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
      doProductsByFilters()
      $('.dm-btn-more').data('offset', offset + limit)
    })
    // ===---
    return false
  }

//* ===---   Load Products By Category   ---=== *//

function pbc_tab(cat, tab) {
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
                    r += '<a href="/" onclick="dm_add2cart($(this)); return false" class="dm-add2cart btn" data-product="'+product.slug+'"><i class="icon-basket-loaded"></i></a>'
                    r += '</li>'
                }
                r += '</ul>'
                r += '</div>'
                r += '</div>'
                r += '<div class="product_info text-left">'
                r += '<h6 class="product_title"><a href="'+product.url+'">'+product.name+'</a></h6>'
                r += '<div class="product_price">'
                if (product.variants) {
                    r += '<span class="price">'+product.price+'</span>'
                } else {
                    r += '<span class="price">'+product.price+'</span>'
                    if (product.price != product.realprice) {
                        r += '<del>'+product.realprice+'</del>'
                    }
                }
                if (product.is_discounted) {
                    r += '<span class="product_sale_discounted">'+i18n.discounted[lang]+'</span>'
                }
                r += '</div>'
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
