var flash = $(".flash-container").offset();
var flashTop = flash ? flash.top : undefined;
$(window).scroll(function () {
  var currentScroll = $(window).scrollTop();
  if (currentScroll >= flashTop - 8) {
    $(".flash-container").css({
      position: "fixed",
      marginTop: "0.5rem",
    });
  } else {
    $(".flash-container").css({
      position: "absolute",
      marginTop: "5.5rem",
    });
  }
});
