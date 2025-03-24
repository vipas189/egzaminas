document.addEventListener("DOMContentLoaded", function () {
  const header = document.querySelector("header");
  let lastScrollTop = 0;

  window.addEventListener(
    "scroll",
    function () {
      let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

      if (scrollTop > lastScrollTop) {
        // Scrolling down
        header.classList.add("header-hidden");
      } else {
        // Scrolling up
        header.classList.remove("header-hidden");
      }

      lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For Mobile or negative scrolling
    },
    false
  );
});
