document.addEventListener("DOMContentLoaded", function () {
  // Get sidebar and main content elements
  const sidebar = document.getElementById("sidebar");
  const mainContent = document.getElementById("main-content");

  // Create toggle button for mobile
  const toggleBtn = document.createElement("button");
  toggleBtn.className = "sidebar-toggle";
  toggleBtn.innerHTML =
    '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>';
  document.body.appendChild(toggleBtn);

  // Get close button
  const sidebarClose = document.getElementById("sidebar-close");

  // Toggle sidebar expansion
  function toggleSidebar() {
    sidebar.classList.toggle("expanded");
    sidebar.classList.toggle("active");
    mainContent.classList.toggle("shifted");
  }

  // Add expanded toggle
  toggleBtn.addEventListener("click", toggleSidebar);

  // Close button functionality
  if (sidebarClose) {
    sidebarClose.addEventListener("click", function () {
      sidebar.classList.remove("active");
      sidebar.classList.remove("expanded");
      mainContent.classList.remove("shifted");
    });
  }

  // Hover functionality for desktop with debounce
  let expandTimeout;
  let collapseTimeout;

  sidebar.addEventListener("mouseenter", function () {
    if (window.innerWidth > 768) {
      clearTimeout(collapseTimeout);

      // Small delay before expanding to prevent accidental triggers
      expandTimeout = setTimeout(function () {
        sidebar.classList.add("expanded");
        mainContent.classList.add("shifted");
      }, 100);
    }
  });

  sidebar.addEventListener("mouseleave", function () {
    if (window.innerWidth > 768) {
      clearTimeout(expandTimeout);

      // Delay before collapsing
      collapseTimeout = setTimeout(function () {
        sidebar.classList.remove("expanded");
        mainContent.classList.remove("shifted");
      }, 300);
    }
  });

  // Navigation Links
  const navLinks = document.querySelectorAll(".nav-link[data-section]");
  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      // Remove active class from all links
      navLinks.forEach((link) => link.classList.remove("active"));
      // Add active class to clicked link
      this.classList.add("active");
      // Hide all sections
      const sections = document.querySelectorAll('[id$="-section"]');
      sections.forEach((section) => (section.style.display = "none"));
      // Show target section
      const targetSectionId = this.getAttribute("data-section");
      document.getElementById(targetSectionId).style.display = "block";

      // On mobile, close the sidebar after selection
      if (window.innerWidth <= 768) {
        sidebar.classList.remove("expanded");
        sidebar.classList.remove("active");
        mainContent.classList.remove("shifted");
      }
    });
  });

  // Avatar and profile picture handling
  const profilePicture = document.getElementById("profile-picture");
  const previewProfileImg = document.getElementById("preview-profile-img");
  const sidebarAvatar = document.querySelector(".user-avatar img");

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
});
