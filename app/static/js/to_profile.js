const profileLink = document.getElementById("to_profile");

if (profileLink) {
  profileLink.addEventListener("click", function () {
    window.location.href = "/profile";
  });
}
