// Pre-render tab initialization - runs immediately
(function () {
  // Get active tab from URL or session storage
  let activeTabType = "student"; // Default

  // Check URL first
  const urlSearch = window.location.search;
  const tabMatch = urlSearch.match(/[?&]tab=([^&]*)/);
  if (tabMatch && ["student", "lecturer", "admin"].includes(tabMatch[1])) {
    activeTabType = tabMatch[1];
  }
  // Then check session storage
  else if (sessionStorage && sessionStorage.getItem("activeTab")) {
    activeTabType = sessionStorage.getItem("activeTab");
  }

  // Store for later use
  if (sessionStorage) {
    sessionStorage.setItem("activeTab", activeTabType);
  }

  // Add style to immediately set correct tab state
  const style = document.createElement("style");
  style.textContent = `
    .form-content { display: none !important; }
    #${activeTabType} { display: block !important; }
  `;
  document.head.appendChild(style);
})();

// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Get the active tab from session storage
  const activeTabType = sessionStorage.getItem("activeTab") || "student";

  // Show courses list appropriately
  const coursesList = document.getElementById("coursesList");
  if (coursesList) {
    coursesList.classList.remove("displayNone");
    coursesList.style.display = activeTabType === "student" ? "block" : "none";
  }

  // Update tab states to match active tab
  document.querySelectorAll(".tab, .tab-register").forEach((tab) => {
    const tabType = tab.getAttribute("data-form");
    if (tabType === activeTabType) {
      tab.classList.add("active");
      tab.classList.remove("inactive");
    } else {
      tab.classList.remove("active");
      tab.classList.add("inactive");
    }
  });

  // Function to activate a specific tab
  function activateTab(tabType) {
    // Update tab-register tabs
    document.querySelectorAll(".tab-register").forEach((t) => {
      if (t.getAttribute("data-form") === tabType) {
        t.classList.add("active");
        t.classList.remove("inactive");
      } else {
        t.classList.remove("active");
        t.classList.add("inactive");
      }
    });

    // Update regular tabs
    document.querySelectorAll(".tab").forEach((t) => {
      if (t.getAttribute("data-form") === tabType) {
        t.classList.add("active");
        t.classList.remove("inactive");
      } else {
        t.classList.remove("active");
        t.classList.add("inactive");
      }
    });

    // Update form visibility
    document.querySelectorAll(".form-content").forEach((form) => {
      form.classList.remove("active");
    });
    document.getElementById(tabType).classList.add("active");

    // Show course list only for student
    if (coursesList) {
      coursesList.style.display = tabType === "student" ? "block" : "none";
    }

    // Store active tab in sessionStorage
    sessionStorage.setItem("activeTab", tabType);

    // Update URL without page reload
    const newUrl = new URL(window.location);
    newUrl.searchParams.set("tab", tabType);
    history.pushState({}, "", newUrl);
  }

  // Tab switching for student/lecturer register tabs
  document.querySelectorAll(".tab-register").forEach((tab) => {
    tab.addEventListener("click", function (e) {
      e.preventDefault();
      const tabType = this.getAttribute("data-form");
      activateTab(tabType);
    });
  });

  // Tab switching for login tabs
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", function (e) {
      e.preventDefault();
      const tabType = this.getAttribute("data-form");
      activateTab(tabType);
    });
  });

  // Course selection with highlighting
  document.querySelectorAll(".course-item").forEach((course) => {
    course.addEventListener("click", function () {
      document.querySelectorAll(".course-item").forEach((c) => {
        c.classList.remove("selected");
      });
      this.classList.add("selected");
      const selectedCourse = this.textContent;
      console.log("Selected course:", selectedCourse);
    });
  });

  // Handle form submissions to include the current tab
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", function () {
      const activeTab = sessionStorage.getItem("activeTab") || "student";
      const hiddenField = document.createElement("input");
      hiddenField.type = "hidden";
      hiddenField.name = "active_tab";
      hiddenField.value = activeTab;
      this.appendChild(hiddenField);
    });
  });
});
