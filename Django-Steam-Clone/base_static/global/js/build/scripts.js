const changeDisplayStyle = (element, display) => {
  if (element) element.style.display = display;
};

const changeOpacity = (element, opacity) => {
  if (element) element.style.opacity = opacity;
};

const changeBackground = (element, background) => {
  if (element) element.style.background = background;
};

const addClassList = (element, value) => {
  if (element) element.classList.add(value);
};

const removeClassList = (element, value) => {
  if (element) element.classList.remove(value);
};

function validateCardClasses() {
  const movies = document.querySelectorAll(".game-card-movie video");
  const pricesBGs = document.querySelectorAll(".game-card-flex-col");

  movies.forEach((movie) => {
    if (movie.classList.contains("toBottomAnimMovie")) {
      removeClassList(movie, "toBottomAnimMovie");
    }
  });

  pricesBGs.forEach((pricesBG) => {
    if (pricesBG.classList.contains("pricesBgAnimRemove")) {
      removeClassList(pricesBG, "pricesBgAnimRemove");
    }
  });
}

const root = document.documentElement;
let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(slideNumber) {
  showSlides((slideIndex += slideNumber));
  validateCardClasses();
}

function currentSlide(slideNumber) {
  showSlides((slideIndex = slideNumber));
  validateCardClasses();
}

function slidesOffSale(slides, dots, slideNumber) {
  if (slideNumber > slides.length) {
    slideIndex = 1;
  }

  if (slideNumber < 1) {
    slideIndex = slides.length;
  }

  for (let i = 0; i < slides.length; i++) {
    changeDisplayStyle(slides[i], "none");
  }

  for (let i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }

  changeDisplayStyle(slides[slideIndex - 1], "flex");
  dots[slideIndex - 1].className += " active";
}

function slidesOnSale(slides, dots, slideNumber) {
  let totalSlides = Math.ceil(slides.length / 3);

  if (slideNumber > totalSlides) {
    slideIndex = 1;
  }

  if (slideNumber < 1) {
    slideIndex = totalSlides;
  }

  for (let i = 0; i < slides.length; i++) {
    changeDisplayStyle(slides[i], "none");
  }

  for (let i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }

  let start = (slideIndex - 1) * 3;
  for (i = start; i < start + 3; i++) {
    if (slides[i]) {
      changeDisplayStyle(slides[i], "flex");
    }
  }
  dots[slideIndex - 1].className += " active";
}

function showSlides(slideNumber) {
  let slides = document.getElementsByClassName("store-games-slider-container");
  const dots = document.getElementsByClassName("slide-dot");

  if (slides.length !== 0) {
    slidesOffSale(slides, dots, slideNumber);
    return;
  }

  slides = document.getElementsByClassName("game-card-item");
  slidesOnSale(slides, dots, slideNumber);
}

(() => {
  const gameCardItems = document.querySelectorAll(".game-card-item");

  const pricesGradient = getComputedStyle(root).getPropertyValue(
    "--prices-bg-gradient"
  );

  gameCardItems.forEach((card) => {
    const movie = card.querySelector(".game-card-movie video");
    const pricesBG = card.querySelector(".game-card-flex-col");

    if (movie) changeOpacity(movie, 0);

    card.addEventListener("mouseover", () => {
      if (movie) {
        removeClassList(movie, "toBottomAnimMovie");
        addClassList(movie, "toTopAnimMovie");
        changeOpacity(movie, 1);
      }
      if (pricesBG) {
        removeClassList(pricesBG, "pricesBgAnimRemove");
        addClassList(pricesBG, "pricesBgAnim");
        changeBackground(pricesBG, pricesGradient);
      }
    });

    card.addEventListener("mouseout", () => {
      if (movie) {
        removeClassList(movie, "toTopAnimMovie");
        addClassList(movie, "toBottomAnimMovie");
        changeOpacity(movie, 0);
      }
      if (pricesBG) {
        removeClassList(pricesBG, "pricesBgAnim");
        addClassList(pricesBG, "pricesBgAnimRemove");
        changeBackground(pricesBG, "none");
      }
    });
  });
})();
