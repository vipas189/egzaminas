// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Show courses list for student form by default
  const coursesList = document.getElementById("coursesList");
  coursesList.classList.remove("displayNone");

  // Tab switching for student/lecturer
  document.querySelectorAll(".tab-register").forEach((tab) => {
    tab.addEventListener("click", function () {
      // Update tab states
      document.querySelectorAll(".tab-register").forEach((t) => {
        t.classList.remove("active");
        t.classList.add("inactive");
      });
      this.classList.remove("inactive");
      this.classList.add("active");

      // Update form visibility
      document.querySelectorAll(".form-content").forEach((form) => {
        form.classList.remove("active");
      });
      const formId = this.getAttribute("data-form");
      document.getElementById(formId).classList.add("active");

      // Show course list only for student
      coursesList.style.display = formId === "student" ? "block" : "none";
    });
  });
  // Tab switching for student/lecturer
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", function () {
      // Update tab states
      document.querySelectorAll(".tab").forEach((t) => {
        t.classList.remove("active");
        t.classList.add("inactive");
      });
      this.classList.remove("inactive");
      this.classList.add("active");

      // Update form visibility
      document.querySelectorAll(".form-content").forEach((form) => {
        form.classList.remove("active");
      });
      const formId = this.getAttribute("data-form");
      document.getElementById(formId).classList.add("active");

      // Show course list only for student
      coursesList.style.display = formId === "student" ? "block" : "none";
    });
  });

  // Course selection with highlighting
  document.querySelectorAll(".course-item").forEach((course) => {
    course.addEventListener("click", function () {
      // Remove selected class from all courses
      document.querySelectorAll(".course-item").forEach((c) => {
        c.classList.remove("selected");
      });

      // Add selected class to clicked course
      this.classList.add("selected");

      // Optional: Store the selected course value
      const selectedCourse = this.textContent;
      console.log("Selected course:", selectedCourse);

      // You could set a hidden input with the selected value
      // Example:
      // document.getElementById("selected-course-input").value = selectedCourse;
    });
  });
});
