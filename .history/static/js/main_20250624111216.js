document.addEventListener("DOMContentLoaded", function () {
    const loginSection = document.querySelector(".login");
    const registerSection = document.querySelector(".register");
    const registerButtons = document.querySelectorAll(".register-btn");
    const loginButtons = document.querySelectorAll(".login-btn");

    if (!loginSection || !registerSection || registerButtons.length === 0 || loginButtons.length === 0) {
        console.error("One or more required elements not found");
        return;
    }

    registerButtons.forEach(button => {
        button.addEventListener("click", function () {
            loginSection.style.visibility = "hidden";
            registerSection.style.visibility = "visible";
        });
    });

    loginButtons.forEach(button => {
        button.addEventListener("click", function () {
            registerSection.style.visibility = "hidden";
            loginSection.style.visibility = "visible";
        });
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const popup = document.querySelector('.homepopup');
    const closeBtn = document.querySelector('.homepopup-btn');

    closeBtn.addEventListener('click', function () {
      popup.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      popup.style.opacity = '0';
      popup.style.transform = 'translateY(-30px)';
      popup.style.transform = 'translateX(0px)';

      // Wait for animation to finish before hiding
      setTimeout(() => {
        popup.style.display = 'none';
      }, 600);
    });
  });
  
document.addEventListener('DOMContentLoaded', function() {
    const minusBtn = document.querySelector('.minus-btn');
    const plusBtn = document.querySelector('.plus-btn');
    const travellerCount = document.querySelector('.traveller-count');
    const travellersInput = document.getElementById('travellers');
    
    // Initialize with 1 traveller
    let count = 1;
    updateDisplay();
    
    // Minus button click handler
    minusBtn.addEventListener('click', function() {
        if (count > 1) {  // Prevent going below 1
            count--;
            updateDisplay();
        }
    });
    
    // Plus button click handler
    plusBtn.addEventListener('click', function() {
        count++;
        updateDisplay();
    });
    
    function updateDisplay() {
        travellerCount.textContent = count;
        
        // Disable minus button when at minimum
        minusBtn.disabled = count <= 1;
        minusBtn.style.opacity = count <= 1 ? "0.5" : "1";
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const switchButton = document.getElementById('switch-countries');
    const indiaFlag = document.querySelector('.india-flag img');
    const usaFlag = document.querySelector('.usa-flag img');
    const indiaInput = document.querySelector('.india-input');
    const usaInput = document.querySelector('.usa-input');
    
    switchButton.addEventListener('click', function() {
        // Swap flag images
        const tempSrc = indiaFlag.src;
        indiaFlag.src = usaFlag.src;
        usaFlag.src = tempSrc;
        
        // Swap alt texts
        const tempAlt = indiaFlag.alt;
        indiaFlag.alt = usaFlag.alt;
        usaFlag.alt = tempAlt;
        
        // Swap placeholder texts
        const tempPlaceholder = indiaInput.placeholder;
        indiaInput.placeholder = usaInput.placeholder;
        usaInput.placeholder = tempPlaceholder;
        
        // Swap input values
        const tempValue = indiaInput.value;
        indiaInput.value = usaInput.value;
        usaInput.value = tempValue;
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const visaSelect = document.getElementById("visa");
    const defaultOption = document.getElementById("defaultOption");

    visaSelect.addEventListener("change", function () {
      // Hide default option after user selects another
      if (visaSelect.value !== "") {
        defaultOption.style.display = "none";
      }
    });
  });

  document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const leftArrows = document.querySelectorAll('.left-arrow');
    const rightArrows = document.querySelectorAll('.right-arrow');
    const tabs = ['mission', 'vision', 'goal'];
    
    // Show first tab by default
    showTab('mission');
    
    // Tab button click event
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            showTab(tabId);
        });
    });
    
    // Left arrow click event (previous tab)
    leftArrows.forEach(arrow => {
        arrow.addEventListener('click', function() {
            const currentTab = document.querySelector('.tab-content.active').id;
            const currentIndex = tabs.indexOf(currentTab);
            const prevIndex = (currentIndex - 1 + tabs.length) % tabs.length;
            showTab(tabs[prevIndex]);
        });
    });
    
    // Right arrow click event (next tab)
    rightArrows.forEach(arrow => {
        arrow.addEventListener('click', function() {
            const currentTab = document.querySelector('.tab-content.active').id;
            const currentIndex = tabs.indexOf(currentTab);
            const nextIndex = (currentIndex + 1) % tabs.length;
            showTab(tabs[nextIndex]);
        });
    });
    
    function showTab(tabId) {
        // Remove active class from all buttons and contents
        tabButtons.forEach(btn => {
            btn.classList.remove('active', 'button2');
            btn.classList.add('button3');
            btn.style.color = 'dark';
        });
        
        tabContents.forEach(content => {
            content.classList.remove('active');
        });
        
        // Add active class to clicked button and corresponding content
        const activeButton = document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
        const activeContent = document.getElementById(tabId);
        
        if (activeButton && activeContent) {
            activeButton.classList.add('active', 'button2');
            activeButton.classList.remove('button3');
            activeButton.style.color = 'white';
            activeContent.classList.add('active');
        }
    }
});

function copyToClipboard() {
  const text = document.getElementById("upi-id").innerText;
  navigator.clipboard.writeText(text).then(() => {
    const toast = document.getElementById("copy-toast");
    toast.classList.add("show");
    setTimeout(() => {
      toast.classList.remove("show");
    }, 3000);
  });
}


document.addEventListener('DOMContentLoaded', function() {
    // Get all required elements
    const appointmentLocation = document.getElementById('appointmentLocation');
    const payNowAmount = document.getElementById('payNowAmount');
    const payLaterAmount = document.getElementById('payLaterAmount');
    const totalAmount = document.getElementById('totalAmount');
    const minusBtn = document.querySelector('.minus-btn');
    const plusBtn = document.querySelector('.plus-btn');
    const travellerCount = document.querySelector('.traveller-count');
    const travellersInput = document.getElementById('travellers');

    // Base prices
    const PRICES = {
        'pan-india': { payNow: 9999, payLater: 4999 },
        'mumbai': { payNow: 14999, payLater: 9999 }
    };

    // Initialize
    let count = parseInt(travellerCount.textContent) || 1;
    updateAll();

    // Event listeners
    minusBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (count > 1) {
            count--;
            updateAll();
        }
    });

    plusBtn.addEventListener('click', function(e) {
        e.preventDefault();
        count++;
        updateAll();
    });

    appointmentLocation.addEventListener('change', updateAll);

    // Main update function
    function updateAll() {
        // Update counter display
        travellerCount.textContent = count;
        travellersInput.value = count === 1 ? 'Traveller' : `Travellers (${count})`;
        minusBtn.disabled = count <= 1;
        minusBtn.style.opacity = count <= 1 ? "0.5" : "1";

        // Get current prices
        const location = appointmentLocation.value || 'pan-india';
        const payNowTotal = PRICES[location].payNow * count;
        const payLaterTotal = PRICES[location].payLater * count;

        // Update displayed amounts - NOW SHOWING TOTALS
        payNowAmount.textContent = `Rs. ${payNowTotal.toLocaleString('en-IN')} x ${count}`;
        payLaterAmount.textContent = `Rs. ${payLaterTotal.toLocaleString('en-IN')} x ${count}`;
        totalAmount.textContent = `Rs. ${payNowTotal.toLocaleString('en-IN')}/-`;
    }
});

function updateVisitorCount() {
    fetch('/visitor-count/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('visitor-count').textContent = data.count;
        });
}

// Update every 30 seconds
setInterval(updateVisitorCount, 30000);

// Initial update after page loads
document.addEventListener('DOMContentLoaded', updateVisitorCount);

document.addEventListener('DOMContentLoaded', function() {
    const appointmentForm = document.querySelector('.col-4.position-fixed');
    if (!appointmentForm) return;

    // Configuration
    const SCROLL_THRESHOLD = 500; // pixels
    const DESKTOP_RIGHT = '7%';
    const MOBILE_RIGHT = '1%'; 
    const TRANSITION = 'right 0.3s ease-out';
    
    // Check if mobile view
    function isMobile() {
        return window.innerWidth <= 768;
    }
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > SCROLL_THRESHOLD && !isMobile()) {
            appointmentForm.style.right = DESKTOP_RIGHT;
            appointmentForm.style.transition = TRANSITION;
        } else {
            appointmentForm.style.right = isMobile() ? MOBILE_RIGHT : '1%';
        }
    });
    
    // Handle resize events
    window.addEventListener('resize', function() {
        appointmentForm.style.right = (window.scrollY > SCROLL_THRESHOLD && !isMobile()) 
            ? DESKTOP_RIGHT 
            : MOBILE_RIGHT;
    });
});


document.getElementById('togglePassword').addEventListener('click', function() {
    const passwordField = document.getElementById('passwordField');
    const toggleIcon = document.getElementById('toggleIcon');
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.classList.remove('bi-eye-slash');
        toggleIcon.classList.add('bi-eye');
    } else {
        passwordField.type = 'password';
        toggleIcon.classList.remove('bi-eye');
        toggleIcon.classList.add('bi-eye-slash');
    }
});