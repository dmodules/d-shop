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
    let price = $(".dm-variants-select option:selected").data("price")
    let dprice = $(".dm-variants-select option:selected").data("dprice")
    if (price != dprice) {
      $(".product_price").html("<span class=\"price\">"+dprice+"</span><del>"+price+"</del>")
    } else {
      $(".product_price").html("<span class=\"price\">"+price+"</span>")
    }
    $(".btn-add2cart").removeClass("disabled")
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

function showAdd2cartSnack() {
  $('#snackbar').text('Produit ajouté au panier')
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
    getResult.product_code = getResult.product_code.toString()
    getResult.quantity = quantity
    $.post(shop + "cart/", getResult, function() {
      showAdd2cartSnack()
      getPanier()
    })
  })
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

function dm_add2cart_variant(k) {
  let endpoint = $(k).data("product")
  let quantity = 1
  let variant = $('.dm-variants-select option.choix:selected').val()
  if ($(k).data("quantity")) {
    quantity = $(k).data("quantity")
  }
  if (variant) {
    $.get(site + i18n.product[lang] + "/" + endpoint + "/add-productvariable-to-cart?product_code="+variant, function(getResult) {
      getResult.quantity = quantity
      getResult.product_code = variant
      $.post(shop + "cart/", getResult, function() {
        showAdd2cartSnack()
        getPanier()
      })
    })
  }
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

$(document).ready(function() {
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
    $('.drawer-nav').css({"height":"calc(100vh - 92px)","top":"92px"});
    $('.header_wrap.fixed-top').css({"top":"92px"});
  } else if ($('.topnav').length) {
    $('html').css({"margin-top":"0"});
    $('body').css({"padding-top":"46px"});
    $('.drawer-overlay').css({"top":"46px"});
    $('.drawer-nav').css({"height":"calc(100vh - 46px)","top":"46px"});
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

/* ======================================================== //
// ===---    @ 2020 D-Modules                        ---=== //
// ======================================================== */
