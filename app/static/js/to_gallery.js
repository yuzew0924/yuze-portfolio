const galleryLink = document.getElementById("to_gallery");

if (galleryLink) {
  galleryLink.addEventListener("click", function () {
    window.location.href = "/";
  });
}
