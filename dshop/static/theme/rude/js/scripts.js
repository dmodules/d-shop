/* ======================================================== //
// ===---    Rude Scripts                         ---=== //
// ======================================================== */

$(document).ready(function() {

    setMainMenuMobile();
    setRudeClickBtn();

    window.addEventListener('resize', () => {
        setMainMenuMobile();
    });

    window.addEventListener('scroll', () => {
        setStickyNavbar();
        // setMainMenuMobileTop();
    });
})


function setRudeClickBtn() {
    $(".dmtop-main-menu-mtoggle").on("click", function(event) {
        event.preventDefault();
        setMainMenuMobileTop();
        // $(".dmtop-main-menu").slideToggle();
    });
}

function setMainMenuMobileTop () {
    if ($(".dmtop-main-menu").hasClass("dm-isopen")) {
        $(".dmtop-main-menu").removeClass("dm-isopen");
        $(".dmtop-main-menu").css("transform", "translateX(100%)");
    } else {
        $(".dmtop-main-menu").addClass("dm-isopen");
        $(".dmtop-main-menu").css("transform", "translateX(0)");
    }
}

function setMainMenuMobile () {
    if ($(".dmtop-main-menu").length) {
        $(".dmtop-navbar").removeClass("mobile");
        $(".dmtop-main-menu").removeClass("mobile");
        $(".dmtop-main-menu-mtoggle").css("display", "none");
        $(".dmtop-main-menu-logo").css("display", "none");
        if (window.innerWidth < 767 || ($(".dmtop-main-menu")[0].scrollWidth) > ($(".dmtophead-menu").width())) {
            $(".dmtop-navbar").addClass("mobile");
            $(".dmtop-main-menu").addClass("mobile");
            // $(".dmtop-main-menu").css("display", "none");
            $(".dmtop-main-menu").removeClass("dm-isopen");
            $(".dmtop-main-menu").css("transform", "translateX(100%)");
            $(".dmtop-main-menu-mtoggle").css("display", "inline-block");
            $(".dmtop-main-menu-logo").css("display", "inline-block");
            $("#dshop-toggle-cart").prependTo($(".dmtophead-right"));
            $("#dshop-toggle-user").prependTo($(".dmtophead-right"));
        } else {
            $(".dmtop-navbar").removeClass("mobile");
            $(".dmtop-main-menu").removeClass("mobile");
            // $(".dmtop-main-menu").css("display", "inline-block");
            $(".dmtop-main-menu").addClass("dm-isopen");
            $(".dmtop-main-menu").css("transform", "translateX(0)");
            $(".dmtop-main-menu-mtoggle").css("display", "none");
            $(".dmtop-main-menu-logo").css("display", "none");
            $("#dshop-toggle-cart").prependTo($(".dmtop-menu-icon-cart"));
            $("#dshop-toggle-user").prependTo($(".dmtop-menu-icon-user"));
        }
    }
}

function setStickyNavbar() {
    if (window.scrollY > 600) {
        let h = $("#rude-topbar").height() + 92
        $(".dmtop-sticky-holder").css("height", h);
        $(".dmtop-navbar").addClass("dmtop-sticky");
    } else if (window.scrollY < 500) {
        $(".dmtop-sticky-holder").css("height", "0");
        $(".dmtop-navbar").removeClass("dmtop-sticky");
    }
}

function dmTopToggleSubmenu(e) {
    if ($(".dmtop-main-menu").hasClass("mobile")) {
        if (e.siblings(".dmtop-main-menu-submenu").hasClass("show")) {
            e.removeClass("active")
            if (!e.siblings(".dmtop-main-menu-submenu").hasClass("sub")) {
                e.removeClass("fa-caret-down")
                e.addClass("fa-caret-right")
            }
            e.siblings(".dmtop-main-menu-submenu").removeClass("show")
        } else {
            e.addClass("active")
            if (!e.siblings(".dmtop-main-menu-submenu").hasClass("sub")) {
                e.removeClass("fa-caret-right")
                e.addClass("fa-caret-down")
            }
            e.siblings(".dmtop-main-menu-submenu").addClass("show")
        }
    }
}
