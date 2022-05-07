function delete_flash(flash) {
  $(flash).parent().remove();
}

document.addEventListener("DOMContentLoaded", function (event) {
  var scrollpos = localStorage.getItem("scrollpos");
  var pathname = localStorage.getItem("pathname");
  if (scrollpos && pathname && window.location.pathname === pathname)
    window.scrollTo(0, scrollpos);
});

window.onbeforeunload = function (e) {
  localStorage.setItem("scrollpos", window.scrollY);
  localStorage.setItem("pathname", window.location.pathname);
};

function on_remove_clicked() {
  searchInput = document.getElementById("search");
  searchInput.value = "";
  searchInput.focus();
}
