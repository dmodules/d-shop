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

  $(".dm-add2soumission").on("click", function(event) {
    event.preventDefault()
    dm_add2soumission(this)
  })
      
  $(".down-arrow").on("click", function() {quantityMinus()})
  $(".up-arrow").on("click", function() {quantityPlus()})
}

function quantityMinus() {
  if ($(".input-num").val() > parseInt($(".input-num").attr('min'))) {
    $(".input-num").val(+$(".input-num").val() - 1)
    $(".dm-add2cart").data("quantity", $(".input-num").val())
  }
}

function quantityPlus() {
  if ($(".input-num").val() < parseInt($(".input-num").attr('max').replace(',','').replace('.',''))) {
    $(".input-num").val(+$(".input-num").val() + 1)
    $(".dm-add2cart").data("quantity", $(".input-num").val())
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

function getPanier() {
  $.get(shop + "cart/fetch-dropdown/", function(getResult) {
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
      $("#dm-drawer-price").text(getResult.total)
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

/**/

function showAdd2soumissionSnack() {
  $('#snackbar').text('Produit ajouté à la soumission')
  $('#snackbar').addClass('show')
  setTimeout(function () {
    $('#snackbar').removeClass('show')
  }, 3000)
}

function dm_add2soumission(k) {
  let endpoint = $(k).data("product")
  let quantity = 0
  $.get(site + i18n.product[lang] + "/" + endpoint + "/add-to-cart", function(getResult) {
    getResult.quantity = quantity
    $.post(shop + "cart/", getResult, function() {
      showAdd2soumissionSnack()
      getSoumission()
    })
  })
}

function dm_delete2soumission(endpoint) {
  $.ajax({
    url: shop + "watch/" + endpoint,
    type: "DELETE",
    success: function() {
      getSoumission()
    }
  })
  return false
}

function getSoumission() {
  $.get(shop + "watch/", function(getResult) {
    if (getResult.items.length >= 1) {
      $("#dm-soumission-items").show()
      $("#dm-soumission-items").text(getResult.items.length)
      if (getResult.num_items > 1) {
        $("#drawer-soumission-count").text(getResult.num_items + " " + i18n.products[lang])
      } else {
        $("#drawer-soumission-count").text(getResult.num_items + " " + i18n.product[lang])
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
          itemlist += "<a href='#' class='dm-item-delete' onclick='return dm_delete2soumission("+JSON.stringify(item.url.split("/cart/")[1])+")'>X</a>"
          itemlist += "</div>"
          itemlist += "</div></div>"
          itemlist += "</li>"
          $("#drawer-soumission-list").html(itemlist)
        })
        itemlist += "</ul>"
        $(".btn-soumission").removeClass("disabled")
      } else {
        $("#dm-soumission-items").hide()
        $("#dm-soumission-items").text("0")
        $("#drawer-soumission-count").text("0 " + i18n.product[lang])
        $("#drawer-soumission-list").html('')
        $(".btn-soumission").addClass("disabled")
      }
    } else {
      $("#dm-soumission-items").hide()
      $("#dm-soumission-items").text("0")
      $("#drawer-soumission-count").text("0 " + i18n.product[lang])
      $("#drawer-soumission-list").html('')
      $(".btn-soumission").addClass("disabled")
    }
  })
}

/* ======================================================== //
// ===---    Produits Scripts                        ---=== //
// ======================================================== */

//* ===---   Load More   ---=== *//

function loadMoreProduits(category = null) {
  let offset = $('.dm-btn-more').data('offset')
  let limit = $('.dm-btn-more').data('limit')
  let cat = ''
  if (category) {
    cat = '&category='+category
  }
  // ===---
  $.get("/api/v1/moreproduits/?offset="+offset+'&limit='+limit+cat, function(getResult) {
    let r = ''
    getResult.products.forEach((product) => {
      r = ''
      r += '<div class="item-container col-md-6" data-filters="tous'
      if (product.filters) {
        r += ' ' + product.filters
      }
      r += '">'
      r += '<div class="shop-item">'
      r += '<a href="'+product.url+'" class="item-img">'
      if (product.image) {
        r += '<img src="'+product.image+'" alt="" class="img-fluid">'
      } else {
        r += '<img src="https://via.placeholder.com/510" alt="" class="img-fluid">'
      }
      r += '</a>'
      r += '<div class="item-bottom-container">'
      r += '<div class="item-meta table">'
      r += '<div class="d-table-row">'
      r += '<div class="item-price text-right">'
      r += '<span>'+product.price+'</span>'
      r += '</div>'
      r += '</div>'
      r += '</div>'
      r += '<div class="item-bottom-box equal-height">'
      r += '<a href="'+product.url+'" class="item-title">'
      r += product.name
      r += '</a>'
      r += '<div class="item-desc">'
      r += product.caption
      r += '</div>'
      r += '</div>'
      r += '<div class="add-to-cart">'
      r += '<a href="#" class="dm-add2cart btn" data-product="'+product.slug+'">Ajouter au panier</a>'
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

//* ===---   Filtres   ---=== *//

$('.size-box').on('change', function( ){
  if ($(this).children('input').attr('name') !== 'tous') {
    $('.size-box.dm-tous').removeClass('checked')
    $('.size-box.dm-tous').children('input').prop("checked", false)
  } else {
    $('.size-box:not(.dm-tous)').removeClass('checked')
    $('.size-box:not(.dm-tous)').children('input').prop("checked", false)
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
  $('.produits .item-container').hide()
  $('.size-box').each(function() {
    if ($(this).children('input').prop('checked')) {
      showProduit($(this).children('input').attr('name'))
    }
  })
}

function showProduit(filter) {
  $('.produits .item-container').each(function() {
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
    getSoumission();
  }
  if ($('#cms-top').length && $('.topnav').length) {
    $('html').css({"margin-top":"0"});
    $('body').css({"padding-top":"92px"});
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
  if ($('#app').length) {
    $('.drawer-toggle.dm-soumission').hide()
    $('.drawer-toggle.dm-cart').hide()
  } else {
    $('.drawer-toggle.dm-soumission').show()
    $('.drawer-toggle.dm-cart').show()
  }
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
    $('.dm-drawer-logs-login-error').html('Une erreur est survenue, veuillez réessayez plus tard.')
    if (failResult.responseJSON) {
      if (failResult.responseJSON.login_form) {
        if (failResult.responseJSON.login_form.email) {
          $('.dm-drawer-logs-login-error').html('Courriel : ' + failResult.responseJSON.login_form.email[0])
        } else if (failResult.responseJSON.login_form.password) {
          $('.dm-drawer-logs-login-error').html('Mot de passe : ' + failResult.responseJSON.login_form.password[0])
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

/* ======================================================== //
// ===---    @ 2020 D-Modules                        ---=== //
// ======================================================== */
