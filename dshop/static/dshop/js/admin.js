$(document).ready(function() {
    $(document).on("click",function(event) {
        let el = $("#dm-admin")
        let $target = $(event.target)
        if (el.hasClass("dm-show-sidebar") && $target.closest("#dm-admin .dm-admin-sidebar").length == 0) {
            el.removeClass("dm-show-sidebar")
        }
    })
    $(".dm-admin-toggle-sidebar").click(function(event){
        event.stopPropagation()
        let el = $("#dm-admin")
        if (el.hasClass("dm-show-sidebar")) {
            el.removeClass("dm-show-sidebar")
        } else {
            el.addClass("dm-show-sidebar")
        }
    })
})

function dmAdminToggleSidebar() {
    let el = $("#dm-admin")
    if (el.hasClass("dm-show-sidebar")) {
        el.removeClass("dm-show-sidebar")
    } else {
        el.addClass("dm-show-sidebar")
    }
}