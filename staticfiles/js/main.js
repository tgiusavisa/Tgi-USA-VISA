document.addEventListener('DOMContentLoaded', function() {
    const visaSelect = document.getElementById('visa');
    const servicesSelect = document.getElementById('services');
    const locationSelect = document.getElementById('appointmentLocation');
    
    // Store all original options
    const allServiceOptions = Array.from(servicesSelect.options);
    const allLocationOptions = Array.from(locationSelect.options);
    
    // Function to filter services based on visa
    function filterServicesByVisa(visa) {
        servicesSelect.innerHTML = '';
        allServiceOptions.forEach(option => servicesSelect.add(option.cloneNode(true)));
        
        Array.from(servicesSelect.options).forEach(option => {
            if (option.value) option.style.display = 'none';
        });

        switch(visa) {
            case 'B1B2-Visa':
                showServiceOptions(['Only-Slot-Booking', 'Only-Normal-Process', 'Full-Process-Express-Dates']);
                break;
            case 'B1B2-Visa Dropbox':
                showServiceOptions(['Full-Process-Dates']);
                break;
            case 'C1d-Visa':
                showServiceOptions(['Full-Process-Express-Dates',]);
                break;
            case 'Immigration-Visa':
                showServiceOptions(['Full-Process-Dates']);
                break;
            case 'H1b/H4-Visa':
            case 'F1/F2-Visa':
            case 'L1/L2-Visa':
            case 'Blanket-L1-Visa':
            case 'Blanket-L2-Visa-Drop-visa':
                showServiceOptions(['Express-Dates']);
                break;
            default:
                showServiceOptions(['Only-Slot-Booking', 'Only-Normal-Process', 'Express-Dates', 
                                 'Full-Process-Dates', 'Full-Process-Express-Dates']);
        }
        servicesSelect.value = '';
        locationSelect.value = '';
    }
    
    // Function to filter locations based on visa and service
    function filterLocations(visa, service) {
        locationSelect.innerHTML = '';
        allLocationOptions.forEach(option => locationSelect.add(option.cloneNode(true)));
        
        Array.from(locationSelect.options).forEach(option => {
            if (option.value) option.style.display = 'none';
        });

        // B1B2 Visa rules
        if (visa === 'B1B2-Visa') {
            if (service === 'Only-Slot-Booking' || service === 'Full-Process-Express-Dates') {
                showLocationOptions(['Pan-India', 'Mumbai-Both-Dates']);
            } 
            else if (service === 'Only-Normal-Process') {
                showLocationOptions(['Mumbai-Delhi-Hydrabad-Chennai-Kolkata']);
            }
        } 
        // B1B2 Visa Dropbox rules
        else if (visa === 'B1B2-Visa Dropbox' && service === 'Full-Process-Dates') {
            showLocationOptions(['Mumbai-Delhi-Hydrabad-Chennai-Kolkata']);
        }
        else if (visa === 'C1d-Visa' && service === 'Full-Process-Express-Dates') {
            showLocationOptions(['Mumbai/Location-of-Your-Choice']);
        }
        // H1b/H4 Visa rules
        else if (visa === 'H1b/H4-Visa' && service === 'Express-Dates') {
            showLocationOptions(['Location-of-your-choice/Hydrabad-Chennai']);
        }
        // F1/F2 Visa rules
        else if (visa === 'F1/F2-Visa' && service === 'Express-Dates') {
            showLocationOptions(['Mumbai/Location-of-Your-Choice']);
        }
        // L1/L2 Visa rules
        else if (visa === 'L1/L2-Visa' && service === 'Express-Dates') {
            showLocationOptions(['Location-of-your-choice/Hydrabad-Chennai']);
        }
        // Blanket L1 Visa rules
        else if (visa === 'Blanket-L1-Visa' && service === 'Express-Dates') {
            showLocationOptions(['Chennai-Only']);
        }
        // Blanket L2 Visa rules
        else if (visa === 'Blanket-L2-Visa-Drop-visa' && service === 'Express-Dates') {
            showLocationOptions(['Location-of-your-choice/Hydrabad-Chennai']);
        }
        // Immigration Visa rules
        else if (visa === 'Immigration-Visa' && service === 'Full-Process-Dates') {
            showLocationOptions(['Mumbai-Both-Dates']);
        }
        
        locationSelect.value = '';
    }
    
    // Helper functions
    function showServiceOptions(options) {
        Array.from(servicesSelect.options).forEach(option => {
            if (option.value && options.includes(option.value)) {
                option.style.display = '';
            }
        });
    }
    
    function showLocationOptions(options) {
        Array.from(locationSelect.options).forEach(option => {
            if (option.value && options.includes(option.value)) {
                option.style.display = '';
            }
        });
    }
    
    // Event listeners
    visaSelect.addEventListener('change', function() {
        filterServicesByVisa(this.value);
    });
    
    servicesSelect.addEventListener('change', function() {
        filterLocations(visaSelect.value, this.value);
    });
    
    // Initialize
    filterServicesByVisa(visaSelect.value);
});


document.addEventListener('DOMContentLoaded', function() {
    // Get all required elements
    const visaSelect = document.getElementById('visa');
    const servicesSelect = document.getElementById('services');
    const locationSelect = document.getElementById('appointmentLocation');
    const payNowAmount = document.getElementById('payNowAmount');
    const payLaterAmount = document.getElementById('payLaterAmount');
    const processingFees = document.getElementById('ProcessingFees');
    const ExpressDate = document.getElementById('ExpressDate');
    const totalAmount = document.getElementById('totalAmount');
    const travellerCount = document.querySelector('.traveller-count');

    // Comprehensive price matrix
    const PRICE_MATRIX = {
        'B1B2-Visa': {
            'Only-Slot-Booking': {
                'Pan-India': { payNow: 7500, payLater: 7500, processing: 0 },
                'Mumbai-Both-Dates': { payNow: 12500, payLater: 12500, processing: 0 }
            },
            'Only-Normal-Process': {
                'Mumbai-Delhi-Hydrabad-Chennai-Kolkata': { payNow: 4500, payLater: 0, processing: 4500 }
            },
            'Full-Process-Express-Dates': {
                'Pan-India': { payNow: 10000, payLater: 9500, processing: 4500, express: 15000},
                'Mumbai-Both-Dates': { payNow: 17000, payLater: 12500, processing: 4500, express: 25000},
            }
        },
        'B1B2-Visa Dropbox': {
            'Full-Process-Dates': {
                'Mumbai-Delhi-Hydrabad-Chennai-Kolkata': { payNow: 10000, payLater: 0, processing: 10000, express: 0},
            },
        },
        'C1d-Visa': {
            'Full-Process-Express-Dates': {
                'Mumbai/Location-of-Your-Choice': { payNow: 10000, payLater: 5000, processing: 15000, express: 0},
            },
        },
        'H1b/H4-Visa': {
            'Express-Dates': {
                'Location-of-your-choice/Hydrabad-Chennai': { payNow: 10000, payLater: 5000, processing: 0, express: 15000},
            },
        },
        'F1/F2-Visa': {
            'Express-Dates': {
                'Mumbai/Location-of-Your-Choice': { payNow: 10000, payLater: 5000, processing: 0, express: 15000},
            },
        },
        'L1/L2-Visa': {
            'Express-Dates': {
                'Location-of-your-choice/Hydrabad-Chennai': { payNow: 10000, payLater: 5000, processing: 0, express: 15000},
            },
        },
        'Blanket-L1-Visa': {
            'Express-Dates': {
                'Chennai-Only': { payNow: 10000, payLater: 5000, processing: 0, express: 15000},
            },
        },
        'Blanket-L2-Visa-Drop-visa': {
            'Express-Dates': {
                'Location-of-your-choice/Hydrabad-Chennai': { payNow: 10000, payLater: 5000, processing: 0, express: 15000},
            },
        },
        'Immigration-Visa': {
            'Full-Process-Dates': {
                'Mumbai-Both-Dates': {payNow: 10000, payLater: 0, processing: 15000, express: 0},
            },
        },
        'default': {
            'pan-india': { payNow: 7500, payLater: 7500, processing: 0 },
            'mumbai': { payNow: 14999, payLater: 9999, processing: 0 }
        }
    };

    // Function to update prices based on selections
    function updatePrices() {
        const visa = visaSelect.value;
        const service = servicesSelect.value;
        const location = locationSelect.value;
        const count = parseInt(travellerCount.textContent) || 1;

        let payNowPrice = 0;
        let payLaterPrice = 0;
        let processingPrice = 0;
        let expressPrice = 0;

        // Check for specific price rules first
        if (visa && service && location && 
            PRICE_MATRIX[visa] && 
            PRICE_MATRIX[visa][service] && 
            PRICE_MATRIX[visa][service][location]) {
            const prices = PRICE_MATRIX[visa][service][location];
            payNowPrice = prices.payNow;
            payLaterPrice = prices.payLater;
            processingPrice = prices.processing;
            expressPrice = prices.express || 0;
        } else {
            // Use default pricing based on location
            const loc = location ? location.toLowerCase() : 'pan-india';
            const defaultPrices = PRICE_MATRIX.default[loc] || PRICE_MATRIX.default['pan-india'];
            payNowPrice = defaultPrices.payNow;
            payLaterPrice = defaultPrices.payLater;
            processingPrice = defaultPrices.processing;
            expressPrice = defaultPrices.express || 0;
        }

        // Calculate totals
        const payNowTotal = payNowPrice * count;
        const payLaterTotal = payLaterPrice * count;
        const processingTotal = processingPrice * count;
        const expressTotal = expressPrice * count;
        const total = payNowTotal + processingTotal + expressTotal;

        // Update displayed amounts
        payNowAmount.textContent = `Rs. ${payNowTotal.toLocaleString('en-IN')} x ${count}`;
        payLaterAmount.textContent = `Rs. ${payLaterTotal.toLocaleString('en-IN')} x ${count}`;
        processingFees.textContent = processingTotal > 0 ? `Rs. ${processingTotal.toLocaleString('en-IN')}` : 'Rs. 0';
        ExpressDate.textContent = expressTotal > 0 ? `Rs. ${expressTotal.toLocaleString('en-IN')}/-` : 'Rs. 0/-';
        totalAmount.textContent = `Rs. ${total.toLocaleString('en-IN')}/-`;
    }

    // Add event listeners
    visaSelect.addEventListener('change', updatePrices);
    servicesSelect.addEventListener('change', updatePrices);
    locationSelect.addEventListener('change', updatePrices);
    document.querySelector('.plus-btn').addEventListener('click', updatePrices);
    document.querySelector('.minus-btn').addEventListener('click', updatePrices);

    // Initialize prices
    updatePrices();
});


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
    const ExpressDate = document.getElementById('ExpressDate');
    const totalAmount = document.getElementById('totalAmount');
    const minusBtn = document.querySelector('.minus-btn');
    const plusBtn = document.querySelector('.plus-btn');
    const travellerCount = document.querySelector('.traveller-count');
    const travellersInput = document.getElementById('travellers');

    // Base prices
    const PRICES = {
        'pan-india': { payNow: 7500, payLater: 7500 },
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
        ExpressDate.textContent = 'Rs. 0';
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


