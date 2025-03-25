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

  document.addEventListener('DOMContentLoaded', function() {
    // Function to toggle study program dropdown visibility - generalized version
    function toggleStudyProgramContainer(roleSelectId, containerSelectId) {
      const roleSelect = document.getElementById(roleSelectId);
      const studyProgramContainer = document.getElementById(containerSelectId);
      
      if (roleSelect && studyProgramContainer) {
        if (roleSelect.value === 'student') {
          // Show the study program dropdown for students
          studyProgramContainer.style.display = 'block';
        } else {
          // Hide the study program dropdown for other roles
          studyProgramContainer.style.display = 'none';
        }
      }
    }
    
    // For edit form
    const editRoleSelect = document.getElementById('edit-role');
    if (editRoleSelect) {
      // Initial check
      toggleStudyProgramContainer('edit-role', 'edit-program-container');
      
      // Add event listener
      editRoleSelect.addEventListener('change', function() {
        toggleStudyProgramContainer('edit-role', 'edit-program-container');
      });
    }
    
    // For add form
    const addRoleSelect = document.getElementById('add-role');
    if (addRoleSelect) {
      // Initial check
      toggleStudyProgramContainer('add-role', 'add-program-container');
      
      // Add event listener
      addRoleSelect.addEventListener('change', function() {
        toggleStudyProgramContainer('add-role', 'add-program-container');
      });
    }
  });

  
  function validatePhoneInput(input) {
    if (!input.value.startsWith('+3706')) {
        input.value = '+3706';
    }
    
    let phoneValue = input.value.replace(/[^0-9+]/g, '');
    
    if (phoneValue.length > 13) {
        phoneValue = phoneValue.slice(0, 13);
    }
    
    input.value = phoneValue;
}

function savePhoneNumber(phone) {
    const phoneErrorElement = document.getElementById('phone-error');
    
    // Patikrinimas, ar telefono numeris pilnas
    if (phone.length !== 13) {
        phoneErrorElement.textContent = 'Prašome įvesti pilną telefono numerį';
        phoneErrorElement.style.display = 'block';
        return;
    }
    
    // Jei viskas gerai
    phoneErrorElement.style.display = 'none';
    localStorage.setItem('userPhone', phone);
}

function clearPhoneNumber() {
    localStorage.removeItem('userPhone');
    document.getElementById('phone').value = '+3706';
    document.getElementById('phone-error').style.display = 'none';
}

function saveBirthDate(date) {
    // Calculate age
    const birthDate = new Date(date);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDifference = today.getMonth() - birthDate.getMonth();
    
    // Adjust age if birthday hasn't occurred this year
    if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }

    const ageErrorElement = document.getElementById('age-error');

    // Patikrinimas, ar asmuo ne jaunesnis nei 18
    if (age < 18) {
        ageErrorElement.textContent = 'Turite būti ne jaunesnis nei 18 metų';
        ageErrorElement.style.display = 'block';
        document.getElementById('date-of-birth').value = '';
        localStorage.removeItem('userBirthDate');
        return;
    }

    // Patikrinimas, ar asmuo ne vyresnis nei 100
    if (age > 100) {
        ageErrorElement.textContent = 'Gimimo data atrodo per sena. Prašome patikrinti.';
        ageErrorElement.style.display = 'block';
        document.getElementById('date-of-birth').value = '';
        localStorage.removeItem('userBirthDate');
        return;
    }

    // Jei viskas gerai
    ageErrorElement.style.display = 'none';
    localStorage.setItem('userBirthDate', date);
}

// Užkrovus puslapį, užpildyti laukelį išsaugoта reikšme
window.onload = function() {
    const savedPhone = localStorage.getItem('userPhone');
    if (savedPhone) {
        document.getElementById('phone').value = savedPhone;
    }

    const savedBirthDate = localStorage.getItem('userBirthDate');
    
    if (savedBirthDate) {
        // Pakartotinai patikrinti amžių
        const birthDate = new Date(savedBirthDate);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDifference = today.getMonth() - birthDate.getMonth();
        
        if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }

        if (age >= 18 && age <= 100) {
            document.getElementById('date-of-birth').value = savedBirthDate;
        } else {
            localStorage.removeItem('userBirthDate');
        }
    }
}
