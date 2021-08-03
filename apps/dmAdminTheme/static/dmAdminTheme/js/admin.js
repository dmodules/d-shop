(function($) {
    'use strict';

    let el = document.getElementById("dm-admin")

    let cookie_asidebar = dmGetCookie("dm_asidebar")

    if (el && cookie_asidebar == 1 && !el.classList.contains("dm-show-sidebar")) {
        el.classList.add("dm-show-sidebar")
    } else if (el && cookie_asidebar == 0) {
        el.classList.remove("dm-show-sidebar")
    }

    $(document).ready(function() {
        let el = $("#dm-admin")

        $(window).on("click", function() {
            if (window.innerWidth < 960) {
                if (el.hasClass("dm-show-sidebar") && !el.hasClass("popup")) {
                    el.removeClass("dm-show-sidebar")
                    dmSetCookie("dm_asidebar", 0, 7)
                }
            }
        })

        /* ===--- Listeners ---=== */

        $(window).on("resize", function() {
            if (window.innerWidth >= 960 && !el.hasClass("dm-show-sidebar") && !el.hasClass("popup")) {
                el.addClass("dm-show-sidebar")
                dmSetCookie("dm_asidebar", 1, 7)
            }
        })

        $(".dm-admin-toggle-sidebar").click(function(event){
            event.stopPropagation()
            let el = $("#dm-admin")
            if (el.hasClass("dm-show-sidebar")) {
                el.removeClass("dm-show-sidebar")
                dmSetCookie("dm_asidebar", 0, 7)
            } else {
                el.addClass("dm-show-sidebar")
                dmSetCookie("dm_asidebar", 1, 7)
            }
        })

    })

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

})(django.jQuery);