const deck = document.getElementById("deck");
const slides = Array.from(document.querySelectorAll(".slide"));
const total = slides.length;
const counterCurrent = document.querySelector(".current");
const counterTotal = document.querySelector(".total");
const toggleButton = document.querySelector(".lang-toggle");

let currentIndex = 0;
let currentLang = deck.dataset.lang || "en";

counterTotal.textContent = String(total);

function setLanguage(nextLang) {
  currentLang = nextLang;
  deck.dataset.lang = nextLang;
  toggleButton.dataset.activeLang = nextLang;
  slides.forEach((slide) => {
    slide.querySelectorAll("[data-lang]").forEach((node) => {
      node.classList.toggle("is-hidden", node.dataset.lang !== nextLang);
    });
  });
}

function activateSlide(index, updateHash = true) {
  currentIndex = (index + total) % total;
  slides.forEach((slide, slideIndex) => {
    slide.classList.toggle("is-active", slideIndex === currentIndex);
  });
  counterCurrent.textContent = String(currentIndex + 1);
  if (updateHash) {
    history.replaceState(null, "", `#${slides[currentIndex].id}`);
  }
}

function slideIndexFromHash() {
  const hash = window.location.hash.replace(/^#/, "");
  const match = slides.findIndex((slide) => slide.id === hash);
  return match >= 0 ? match : 0;
}

document.querySelector(".nav-prev").addEventListener("click", () => activateSlide(currentIndex - 1));
document.querySelector(".nav-next").addEventListener("click", () => activateSlide(currentIndex + 1));

document.querySelectorAll(".deck-index a").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    const id = link.getAttribute("href").slice(1);
    const nextIndex = slides.findIndex((slide) => slide.id === id);
    if (nextIndex >= 0) {
      activateSlide(nextIndex);
    }
  });
});

toggleButton.addEventListener("click", () => {
  setLanguage(currentLang === "en" ? "zh" : "en");
});

window.addEventListener("hashchange", () => {
  activateSlide(slideIndexFromHash(), false);
});

window.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight") {
    activateSlide(currentIndex + 1);
  } else if (event.key === "ArrowLeft") {
    activateSlide(currentIndex - 1);
  } else if (event.key === "Home") {
    activateSlide(0);
  } else if (event.key === "End") {
    activateSlide(total - 1);
  }
});

setLanguage(currentLang);
activateSlide(slideIndexFromHash(), false);
