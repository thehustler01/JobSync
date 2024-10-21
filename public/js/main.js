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
// Get the file input and file info elements
const fileInput = document.getElementById('file-input');
const fileInfo = document.getElementById('file-info');

// Trigger file input when the upload button is clicked
document.querySelector('.upload-btn').addEventListener('click', function() {
    fileInput.click(); // Open file dialog
});

// When a file is selected
fileInput.addEventListener('change', function() {
    if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        fileInfo.textContent = `Selected file: ${fileName}`;
        
        // Start the animation once a file is uploaded
        startAnimation();
    } else {
        fileInfo.textContent = 'No file selected';
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


