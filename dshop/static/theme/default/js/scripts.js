/* ======================================================== //
// ===---    D-SHOP Scripts                          ---=== //
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
  $.get("/api/fe/moreproduits/?offset="+offset+'&limit='+limit+cat, function(getResult) {
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
        r += '<img src="https://via.placeholder.com/540x600" alt="" class="img-fluid">'
      }
      r += '</a>'
      r += '<div class="product_action_box">'
      r += '<ul class="list_none pr_action_btn">'
      r += '<li>'
      r += '<a href="'+product.url+'"><i class="ti-info-alt"></i></a>'
      r += '</li>'
      if (product.variants) {}
      else {
        r += '<li>'
        r += '<a href="/" class="dm-add2cart btn" data-product="'+product.slug+'"><i class="icon-basket-loaded"></i></a>'
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
