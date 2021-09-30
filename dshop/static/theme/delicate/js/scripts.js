/* ======================================================== //
// ===---    Delicate Scripts                         ---=== //
// ======================================================== */

$(document).ready(function() {

    setMainMenuMobile();
    setDelicateClickBtn();

    window.addEventListener('resize', () => {
        setMainMenuMobile();
    });

    window.addEventListener('scroll', () => {
        setStickyNavbar();
        setMainMenuMobileTop();
    });
})


function setDelicateClickBtn() {
    $(".dmtop-main-menu-mtoggle").on("click", function(event) {
        event.preventDefault();
        setMainMenuMobileTop();
        $(".dmtop-main-menu").slideToggle();
    });
}

function setMainMenuMobileTop () {
    let h = $(".dmtop-navbar").height()
    if ($("#cms-top").length) {
        h += 46
    }
    $(".dmtop-main-menu").css("top", h+"px");
}

function setMainMenuMobile () {
    if ($(".dmtop-main-menu").length) {
        $(".dmtop-main-menu").removeClass("mobile");
        $(".dmtop-main-menu-mtoggle").css("display", "none");
        if (window.innerWidth < 767 || ($(".dmtop-main-menu")[0].scrollWidth) > ($(".dmtophead-menu").width())) {
            $(".dmtop-main-menu").addClass("mobile");
            $(".dmtop-main-menu").css("display", "none");
            $(".dmtop-main-menu-mtoggle").css("display", "inline-block");
        } else {
            $(".dmtop-main-menu").removeClass("mobile");
            $(".dmtop-main-menu").css("display", "inline-block");
            $(".dmtop-main-menu-mtoggle").css("display", "none");
        }
    }
}

function setStickyNavbar() {
    if (window.scrollY > 600) {
        $(".dmtop-sticky-holder").css("height", $(".dmtop-navbar").height());
        $(".dmtop-navbar").addClass("dmtop-sticky");
    } else if (window.scrollY < 500) {
        $(".dmtop-sticky-holder").css("height", "0");
        $(".dmtop-navbar").removeClass("dmtop-sticky");
    }
}

function dmTopToggleSubmenu(e) {
    if (e.siblings(".dmtop-main-menu-submenu").hasClass("show")) {
        e.removeClass("active")
        if (!e.siblings(".dmtop-main-menu-submenu").hasClass("sub")) {
            e.removeClass("ion-ios-arrow-down")
            e.addClass("ion-ios-arrow-right")
        }
        e.siblings(".dmtop-main-menu-submenu").removeClass("show")
    } else {
        e.addClass("active")
        if (!e.siblings(".dmtop-main-menu-submenu").hasClass("sub")) {
            e.removeClass("ion-ios-arrow-right")
            e.addClass("ion-ios-arrow-down")
        }
        e.siblings(".dmtop-main-menu-submenu").addClass("show")
    }
}
