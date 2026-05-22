const categoryMenu = document.querySelector(".category-menu");
const categoryToggle = document.querySelector(".category-toggle");
const categoryOptions = document.querySelectorAll(".category-option");
const waterfall = document.querySelector(".waterfall");
const galleryItems = document.querySelectorAll(".waterfall .item");
const emptyGallery = document.querySelector(".empty-gallery");
const hasGallery = galleryItems.length > 0;

function setActiveCategory(selectedCategory) {
  let visibleCount = 0;

  if (waterfall) {
    waterfall.classList.toggle("category-filtered", selectedCategory !== "all");
  }

  galleryItems.forEach((item) => {
    const shouldShow =
      selectedCategory === "all" || item.dataset.category === selectedCategory;

    item.classList.toggle("hidden", !shouldShow);

    if (shouldShow) {
      visibleCount += 1;
    }
  });

  categoryOptions.forEach((option) => {
    option.classList.toggle("active", option.dataset.category === selectedCategory);
  });

  if (emptyGallery) {
    emptyGallery.classList.toggle("visible", visibleCount === 0);
  }
}

function goToGalleryCategory(selectedCategory) {
  const target =
    selectedCategory === "all"
      ? "/"
      : `/?category=${encodeURIComponent(selectedCategory)}`;

  window.location.href = target;
}

function updateCategoryUrl(selectedCategory) {
  const nextUrl =
    selectedCategory === "all"
      ? window.location.pathname
      : `${window.location.pathname}?category=${encodeURIComponent(selectedCategory)}`;

  window.history.replaceState({}, "", nextUrl);
}

const initialCategory = new URLSearchParams(window.location.search).get("category");

if (hasGallery && initialCategory) {
  setActiveCategory(initialCategory);
} else if (hasGallery) {
  setActiveCategory("all");
}

categoryOptions.forEach((option) => {
  option.addEventListener("click", () => {
    if (hasGallery) {
      setActiveCategory(option.dataset.category);
      updateCategoryUrl(option.dataset.category);
    } else {
      goToGalleryCategory(option.dataset.category);
    }

    categoryMenu.classList.remove("open");
  });
});

categoryToggle.addEventListener("click", () => {
  if (hasGallery) {
    setActiveCategory("all");
    updateCategoryUrl("all");
  } else {
    window.location.href = "/";
    return;
  }

  categoryMenu.classList.toggle("open");
});

document.addEventListener("click", (event) => {
  if (!categoryMenu.contains(event.target)) {
    categoryMenu.classList.remove("open");
  }
});

categoryMenu.addEventListener("mouseleave", () => {
  categoryMenu.classList.remove("open");
});
