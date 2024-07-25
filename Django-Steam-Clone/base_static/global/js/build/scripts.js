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

(() => {
  const gameCardItems = document.querySelectorAll(".game-card-item");

  gameCardItems.forEach((card) => {
    const movie = card.querySelector(".game-card-movie video");

    if (movie) changeOpacity(movie, 0);

    card.addEventListener("mouseover", () => {
      if (movie) {
        removeClassList(movie, "toBottomAnimMovie");
        addClassList(movie, "toTopAnimMovie");
        changeOpacity(movie, 1);
      }
    });
    card.addEventListener("mouseout", () => {
      if (movie) {
        removeClassList(movie, "toTopAnimMovie");
        addClassList(movie, "toBottomAnimMovie");
        changeOpacity(movie, 0);
      }
    });
  });
})();

function removeMoviesAnimation() {
  const movies = document.querySelectorAll(".game-card-movie video");

  movies.forEach((movie) => {
    if (movie.classList.contains("toBottomAnimMovie")) {
      removeClassList(movie, "toBottomAnimMovie");
    }
  });
}

const handleSlides = (slides, dots, slideIndex, cardsPerSlide) => {
  for (let i = 0; i < slides.length; i++) {
    changeDisplayStyle(slides[i], "none");
  }

  for (let i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }

  let start = (slideIndex - 1) * cardsPerSlide;
  for (let i = start; i < start + cardsPerSlide; i++) {
    if (slides[i]) {
      changeDisplayStyle(slides[i], "flex");
    }
  }
  dots[slideIndex - 1].className += " active";
};

const setupCarousel = (slides, dots, nextSlide, prevSlide, cardsPerSlide) => {
  if (!slides) return;
  const totalSlides = Math.ceil(slides.length / cardsPerSlide);
  let slideIndex = 1;

  nextSlide.addEventListener("click", () => {
    slideIndex++;
    if (slideIndex > totalSlides) slideIndex = 1;
    handleSlides(slides, dots, slideIndex, cardsPerSlide);
    removeMoviesAnimation();
  });

  prevSlide.addEventListener("click", () => {
    slideIndex--;
    if (slideIndex < 1) slideIndex = totalSlides;
    handleSlides(slides, dots, slideIndex, cardsPerSlide);
    removeMoviesAnimation();
  });

  dots.forEach((dot) => {
    dot.addEventListener("click", () => {
      const dotNumber = parseInt(dot.getAttribute("slide-number"));
      slideIndex = dotNumber;
      handleSlides(slides, dots, slideIndex, cardsPerSlide);
    });
  });
  handleSlides(slides, dots, slideIndex, cardsPerSlide);
};

(() => {
  const salesContainer = document.querySelector(".sales-grid-cards-content");
  if (salesContainer) {
    setupCarousel(
      (slides = salesContainer.querySelectorAll(".game-card-item")),
      (dots = salesContainer.querySelectorAll(".store-slides .slide-dot")),
      (nextSlide = salesContainer.querySelector(".arrow-right")),
      (prevSlide = salesContainer.querySelector(".arrow-left")),
      (cardsPerSlide = 3)
    );
  }

  const deepDiscContainer = document.querySelector(".deep-discounts-container");
  if (deepDiscContainer) {
    setupCarousel(
      (slides = deepDiscContainer.querySelectorAll(".deep-disc-card-item")),
      (dots = deepDiscContainer.querySelectorAll(".slide-dot")),
      (nextSlide = deepDiscContainer.querySelector(".arrow-right")),
      (prevSlide = deepDiscContainer.querySelector(".arrow-left")),
      (cardsPerSlide = 3)
    );
  }

  const categoriesContainer = document.querySelector(
    ".browse-by-category-container"
  );
  if (categoriesContainer) {
    setupCarousel(
      (slides = categoriesContainer.querySelectorAll(".category-item")),
      (dots = categoriesContainer.querySelectorAll(".slide-dot")),
      (nextSlide = categoriesContainer.querySelector(".arrow-right")),
      (prevSlide = categoriesContainer.querySelector(".arrow-left")),
      (cardsPerSlide = 4)
    );
  }
})();

(() => {
  const gameCarouselItems = document.querySelectorAll(".game-carousel-item");

  if (!gameCarouselItems) return;

  if (gameCarouselItems.length > 5) {
    const gameCarouselArray = Array.from(gameCarouselItems);
    const lastElements = gameCarouselArray.slice(5);
    for (const elm of lastElements) changeDisplayStyle(elm, "none");
  }

  addClassList(gameCarouselItems[0], "active");
})();
