(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.navbar').addClass('sticky-top shadow-sm');
        } else {
            $('.navbar').removeClass('sticky-top shadow-sm');
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Skills
    $('.skill').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%');
        });
    }, {offset: '80%'});


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 25,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            992:{
                items:2
            }
        }
    });


    // Portfolio isotope and filter
    var portfolioIsotope = $('.portfolio-container').isotope({
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'
    });
    $('#portfolio-flters li').on('click', function () {
        $("#portfolio-flters li").removeClass('active');
        $(this).addClass('active');

        portfolioIsotope.isotope({filter: $(this).data('filter')});
    });
    
})(jQuery);




// ##############################################   resume-section   #####################################################



const form = document.getElementById('resume-form');
const pdfFrame = document.getElementById('pdf-container');
const uploadButton = document.getElementById('upload-button');
const selectFileButton = document.getElementById('select-file-button');
const fileInput = document.getElementById('file-input');
const fileInfo = document.getElementById('file-info');

// Trigger file input when 'Select Resume' button is clicked
selectFileButton.addEventListener('click', () => {
    fileInput.click();
});

// Update file info on selection and trigger animation
fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        fileInfo.textContent = `Selected: ${fileInput.files[0].name}`;
        startAnimation();
    } else {
        fileInfo.textContent = 'No file selected';
    }
});

form.addEventListener('submit', function (event) {
    event.preventDefault();

    if (fileInput.files.length > 0) {
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Display the uploaded PDF
                pdfFrame.src = data.pdf_url;

                // Display parsed data if available
                if (data.skillset) {
                    displayParsedData(data.skillset);
                    console.log(data.suggested_job_role);
                    console.log(data.missing_skills);
                    displayMissingSkills(data.missing_skills);
                    // displayJobRole(data.suggested_job_role);
                    

                }
            } else {
                alert(data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please select a resume file.');
    }
});

// Function to animate the progress bar and activate circle 2
function startAnimation() {
    const step1 = document.querySelectorAll('.step')[0];
    const step2 = document.querySelectorAll('.step')[1];
    const lineBetween = document.querySelectorAll('.line')[0];

    // Keep circle 1 active
    step1.classList.add('active');

    // Animate the line between circle 1 and circle 2
    lineBetween.classList.add('animated-line');

    // Wait for the line animation to complete (1s), then activate circle 2
    setTimeout(function() {
        step2.classList.add('active');
    }, 1000); // Time same as the CSS animation duration
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// function displayParsedData(parsedData) {
//     const dataContainer = document.getElementById('parsed-data');
//     dataContainer.innerHTML = '';  // Clear previous data

//     const ul = document.createElement('ul');
//     for (const [key, value] of Object.entries(parsedData)) {
//         const li = document.createElement('li');
//         li.innerHTML = `<strong>${key}:</strong> ${value}`;
//         ul.appendChild(li);
//     }
//     dataContainer.appendChild(ul);
// }
function displayParsedData(parsedData) {
    const dataContainer = document.getElementById('user-skills');
    const header = document.getElementById('Extracted-head1');
    header.style.display = "block";
    dataContainer.innerHTML = '';  // Clear previous data

    const ul = document.createElement('ul');
    
    let index = 0; // To calculate animation delay
    for (const [key, value] of Object.entries(parsedData)) {
        const li = document.createElement('li');
        li.style.setProperty('--i', index); // Custom property for delay
        li.innerHTML = `
            <i class="fas fa-rocket"></i>
            ${value}
        `;
        
        ul.appendChild(li);
        index++;
    }
    dataContainer.appendChild(ul);
    
    // Trigger animation after adding elements
    setTimeout(() => {
        document.querySelectorAll('.parsed-data li').forEach(li => {
            li.style.opacity = 1;
        });
    }, 100); // Small delay before animation starts
}
function displayMissingSkills(parsedData) {
    const dataContainer = document.getElementById('missing-skills');
    const header = document.getElementById('Extracted-head2');
    header.style.display = "block";
    dataContainer.innerHTML = '';  // Clear previous data

    const ul = document.createElement('ul');
    
    let index = 0; // To calculate animation delay
    for (const [key, value] of Object.entries(parsedData)) {
        const li = document.createElement('li');
        li.style.setProperty('--i', index); // Custom property for delay
        li.innerHTML = `
            <i class="fas fa-rocket"></i>
            ${value}
        `;
        
        ul.appendChild(li);
        index++;
    }
    dataContainer.appendChild(ul);
    
    // Trigger animation after adding elements
    setTimeout(() => {
        document.querySelectorAll('.parsed-data li').forEach(li => {
            li.style.opacity = 1;
        });
    }, 100); // Small delay before animation starts
}



// function displayMissingSkills(parsedData) {
//     const dataContainer = document.getElementById('missing-skills');
//     const header = document.getElementById('Extracted-head2');
//     header.style.display = "block";

//     dataContainer.innerHTML = '';  // Clear previous data

//     const ul = document.createElement('ul');
    
//     let index = 0; // To calculate animation delay
//     for (const [key, value] of Object.entries(parsedData)) {
//         const li = document.createElement('li');
//         li.style.setProperty('--i', index); // Custom property for delay
//         li.innerHTML = `
//             <i class="fas fa-rocket"></i>
//             ${value}
//         `;
        
//         ul.appendChild(li);
//         index++;
//     }
//     dataContainer.appendChild(ul);
    
//     // Trigger animation after adding elements
//     setTimeout(() => {
//         document.querySelectorAll('.parsed-data li').forEach(li => {
//             li.style.opacity = 1;
//         });
//     }, 100); // Small delay before animation starts
// }
// function displayJobRole(parsedData) {
//     const dataContainer = document.getElementById('job-role');
//     const header = document.getElementById('Extracted-head3');
//     header.style.display = "block";

//     dataContainer.innerHTML = '';  // Clear previous data

//     const ul = document.createElement('ul');
    
//     let index = 0; // To calculate animation delay
//     for (const [key, value] of Object.entries(parsedData)) {
//         const li = document.createElement('li');
//         li.style.setProperty('--i', index); // Custom property for delay
//         li.innerHTML = `
//             <i class="fas fa-rocket"></i>
//             ${value}
//         `;
        
//         ul.appendChild(li);
//         index++;
//     }
//     dataContainer.appendChild(ul);
    
//     // Trigger animation after adding elements
//     setTimeout(() => {
//         document.querySelectorAll('.parsed-data li').forEach(li => {
//             li.style.opacity = 1;
//         });
//     }, 100); // Small delay before animation starts
// }
