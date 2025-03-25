document.addEventListener("DOMContentLoaded", function () {
    // Show course list immediately if student tab is active on load
    const activeTab = document.querySelector(".tab.active, .tab-register.active");
    if (activeTab && activeTab.getAttribute("data-form") === "student") {
      const coursesList = document.getElementById("coursesList");
      if (coursesList) {
        coursesList.style.display = "block";
        coursesList.classList.remove("displayNone");
      }
    }
  
    // Function to handle tab switching
    function switchTab(tabType) {
      // Update regular tabs
      document.querySelectorAll(".tab").forEach((tab) => {
        const currentTabType = tab.getAttribute("data-form");
        if (currentTabType === tabType) {
          tab.classList.add("active");
          tab.classList.remove("inactive");
        } else {
          tab.classList.remove("active");
          tab.classList.add("inactive");
        }
      });
  
      // Update register tabs
      document.querySelectorAll(".tab-register").forEach((tab) => {
        const currentTabType = tab.getAttribute("data-form");
        if (currentTabType === tabType) {
          tab.classList.add("active");
          tab.classList.remove("inactive");
        } else {
          tab.classList.remove("active");
          tab.classList.add("inactive");
        }
      });
  
      // Hide all forms
      document.querySelectorAll(".form-content").forEach((form) => {
        form.style.display = "none";
        form.classList.remove("active");
      });
  
      // Show selected form
      const selectedForm = document.getElementById(tabType);
      if (selectedForm) {
        selectedForm.style.display = "block";
        selectedForm.classList.add("active");
      }
  
      // Show course list only for student tab
      const coursesList = document.getElementById("coursesList");
      if (coursesList) {
        coursesList.style.display = tabType === "student" ? "block" : "none";
        if (tabType === "student") {
          coursesList.classList.remove("displayNone");
        }
      }
    }
  
    // Add click event listeners to regular tabs
    document.querySelectorAll(".tab").forEach((tab) => {
      tab.addEventListener("click", function (e) {
        e.preventDefault();
        const tabType = this.getAttribute("data-form");
        switchTab(tabType);
      });
    });
  
    // Add click event listeners to register tabs
    document.querySelectorAll(".tab-register").forEach((tab) => {
      tab.addEventListener("click", function (e) {
        e.preventDefault();
        const tabType = this.getAttribute("data-form");
        switchTab(tabType);
      });
    });
  });
  document.addEventListener("DOMContentLoaded", function () {
    // Ensure course list is visible for student form
    const studentTab = document.querySelector(
      '.tab-register[data-form="student"]'
    );
    if (studentTab && studentTab.classList.contains("active")) {
      const coursesList = document.getElementById("coursesList");
      if (coursesList) {
        coursesList.classList.remove("displayNone");
      }
    }
  
    // Course selection handling
    const courseItems = document.querySelectorAll(".course-item");
    courseItems.forEach(function (item) {
      item.addEventListener("click", function () {
        // Visually mark the selection
        courseItems.forEach((i) => i.classList.remove("selected"));
        this.classList.add("selected");
  
        // CRITICAL: Set the hidden input value
        // Look for the input with BOTH id and name attributes matching
        const hiddenInput = document.querySelector('input[name="study_program"]');
        if (hiddenInput) {
          hiddenInput.value = this.textContent.trim();
          console.log("Set course value to:", hiddenInput.value);
        } else {
          console.error(
            'Could not find hidden input field by name="study_program"'
          );
  
          // Fallback to ID-based lookup
          const hiddenInputById = document.getElementById(
            "selected-course-input"
          );
          if (hiddenInputById) {
            hiddenInputById.value = this.textContent.trim();
            console.log("Set course value by ID to:", hiddenInputById.value);
          } else {
            console.error("Could not find hidden input by ID either");
          }
        }
      });
    });
  });