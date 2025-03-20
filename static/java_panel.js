document.addEventListener("DOMContentLoaded", function () {
  // Toggle sidebar on mobile
  const menuToggle = document.getElementById("menu-toggle");
  const sidebarClose = document.getElementById("sidebar-close");
  const sidebar = document.getElementById("sidebar");

  if (menuToggle) {
    menuToggle.addEventListener("click", function () {
      sidebar.classList.add("active");
    });
  }

  if (sidebarClose) {
    sidebarClose.addEventListener("click", function () {
      sidebar.classList.remove("active");
    });
  }

  // Navigation section switching
  const navLinks = document.querySelectorAll(".nav-link");
  const dashboardSection = document.getElementById("dashboard-section");
  const profileSection = document.getElementById("profile-section");
  const topBarTitle = document.querySelector(".top-bar-title");

  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      const targetSection = this.getAttribute("data-section");

      // Remove active class from all links
      navLinks.forEach((navLink) => {
        navLink.classList.remove("active");
      });

      // Add active class to current link
      this.classList.add("active");

      if (targetSection === "dashboard-section") {
        dashboardSection.style.display = "block";
        profileSection.style.display = "none";
        topBarTitle.textContent = "Student Dashboard";
      } else if (targetSection === "profile-section") {
        dashboardSection.style.display = "none";
        profileSection.style.display = "block";
        topBarTitle.textContent = "My Profile";
      } else if (this.getAttribute("href") === "#") {
        e.preventDefault();
        alert("This feature is coming soon!");
      }
    });
  });

  // Schedule tabs
  const scheduleTabs = document.querySelectorAll(".schedule-tab");

  scheduleTabs.forEach((tab) => {
    tab.addEventListener("click", function () {
      // Remove active class from all tabs
      scheduleTabs.forEach((scheduleTab) => {
        scheduleTab.classList.remove("active");
      });

      // Add active class to current tab
      this.classList.add("active");
    });
  });

  // Settings tabs
  const settingsTabs = document.querySelectorAll(".settings-tab");

  settingsTabs.forEach((tab) => {
    tab.addEventListener("click", function () {
      // Remove active class from all tabs
      settingsTabs.forEach((settingsTab) => {
        settingsTab.classList.remove("active");
      });

      // Add active class to current tab
      this.classList.add("active");
    });
  });

  // Profile image upload
  const avatarTrigger = document.getElementById("avatar-trigger");
  const profilePicture = document.getElementById("profile-picture");
  const previewProfileImg = document.getElementById("preview-profile-img");
  const sidebarAvatar = document.querySelector(".user-avatar img");

  if (avatarTrigger) {
    avatarTrigger.addEventListener("click", function () {
      profilePicture.click();
    });
  }

  if (profilePicture) {
    profilePicture.addEventListener("change", function () {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.addEventListener("load", function () {
          // Update all instances of the profile image
          if (previewProfileImg) previewProfileImg.src = this.result;
          if (sidebarAvatar) sidebarAvatar.src = this.result;
        });
        reader.readAsDataURL(file);
      }
    });
  }

  // Form submission
  const profileForm = document.getElementById("profile-form");

  if (profileForm) {
    profileForm.addEventListener("submit", function (e) {
      e.preventDefault();
      alert("Profile updated successfully!");
    });
  }
});
