let currentQuestionIndex = 0; // Track the current question index
let questions = []; // Store questions
let userAnswer = ""; // Store user's answer

document.getElementById('interviewForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const jobRole = document.getElementById('job_role').value.trim();
    const skills = document.getElementById('skills').value.split(',').map(skill => skill.trim());

    // Here you would typically send the data to your backend to start the interview
    console.log('Job Role:', jobRole);
    console.log('Skills:', skills);

    // Simulate starting the interview by showing questions
    document.getElementById('questionsContainer').classList.remove('hidden');
    
    // Fetch questions from backend (simulated here)
    fetchQuestions(jobRole, skills);
});

function fetchQuestions(jobRole, skills) {
    // Simulated questions (replace this with an API call)
    questions = [
        "What are your strengths?",
        "Why do you want to work here?",
        "Describe a challenging situation and how you handled it."
        // Add more questions as needed
    ];

   displayQuestion();
}

function displayQuestion() {
   if (currentQuestionIndex < questions.length) {
       const currentQuestion = questions[currentQuestionIndex];
       document.getElementById('currentQuestion').innerHTML = `<strong>Question:</strong> ${currentQuestion}`;
       
       // Show answer container and buttons
       document.getElementById('answerContainer').classList.remove('hidden');
       document.getElementById('recordButton').classList.remove('hidden');
       document.getElementById('retryButton').classList.add('hidden'); // Hide retry button initially
       document.getElementById('submitResponseButton').classList.add('hidden'); // Hide submit button initially

       // Read aloud the question using SpeechSynthesis API
       const utterance = new SpeechSynthesisUtterance(currentQuestion);
       speechSynthesis.speak(utterance);

       // Reset previous answer
       userAnswer = "";
       document.getElementById('userAnswer').innerText = "";
       document.getElementById('suggestionsContainer').classList.add('hidden');
       document.getElementById('idealAnswerContainer').classList.add('hidden');
       
       // Start recording answer on button press
       handleRecording();
       
   } else {
       alert("No more questions.");
   }
}

function handleRecording() {
   const recordButton = document.getElementById('recordButton');
   let isRecording = false;

   recordButton.onmousedown = function() {
       isRecording = true;
       recordButton.innerText = "Recording... Release to Stop";
       listenToAnswer();
   };

   recordButton.onmouseup = function() {
       isRecording = false;
       recordButton.innerText = "Hold to Record";
   };

   recordButton.ontouchstart = function() { recordButton.onmousedown(); };
   recordButton.ontouchend = function() { recordButton.onmouseup(); };
}

function listenToAnswer() {
   const recognizer = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
   recognizer.lang = 'en-US';
   recognizer.interimResults = false;

   recognizer.start();

   recognizer.onresult = (event) => {
       userAnswer = event.results[0][0].transcript; // Get recognized text
       document.getElementById('userAnswer').innerText = userAnswer; // Display answer
       
       console.log(`You said: ${userAnswer}`);
       
       // Show submit response button after recording
       document.getElementById('submitResponseButton').classList.remove('hidden');
   };

   recognizer.onerror = (event) => {
       console.error(event.error);
   };
}

// Submit response functionality
document.getElementById('submitResponseButton').addEventListener('click', function() {
   submitResponse(userAnswer); // Submit answer to backend for analysis
});

// Submit response to backend and display suggestions/ideal answers
function submitResponse(answer) {
   console.log("Submitting response:", answer);
   
   // Simulate sending answer to backend and getting suggestions/ideal answer (replace with actual API call)
   const suggestions = "1. Be more specific about your strengths.\n2. Provide examples.";
   const idealAnswer = "An ideal answer would include specific strengths relevant to the job.";

   displaySuggestions(suggestions, idealAnswer);
}

// Display suggestions and ideal answers
function displaySuggestions(suggestions, idealAnswer) {
   document.getElementById('suggestionsContainer').innerHTML =
       `<strong>Suggestions:</strong><br>${suggestions}`;
   document.getElementById('suggestionsContainer').classList.remove('hidden');

   document.getElementById('idealAnswerContainer').innerHTML =
       `<strong>Ideal Answer:</strong><br>${idealAnswer}`;
   document.getElementById('idealAnswerContainer').classList.remove('hidden');

   document.getElementById('nextButton').classList.remove('hidden'); // Show next button after suggestions are displayed
}

// Next question button functionality
document.getElementById('nextButton').addEventListener('click', function() {
   currentQuestionIndex++;
   displayQuestion(); // Load next question
});

// Retry answer functionality
document.getElementById('retryButton').addEventListener('click', function() {
   userAnswer = ""; // Clear previous answer
   document.getElementById('userAnswer').innerText = ""; // Clear displayed answer

   // Show record button again for new recording
   document.getElementById('recordButton').classList.remove('hidden');
});

// Quit button functionality
document.getElementById('quitButton').addEventListener('click', function() {
   alert("Exiting the interview.");
});









// ================================================ navbar script =================================================================
function test(){
    var tabsNewAnim = $('#navbarSupportedContent');
    var selectorNewAnim = $('#navbarSupportedContent').find('li').length;
    var activeItemNewAnim = tabsNewAnim.find('.active');
    var activeWidthNewAnimHeight = activeItemNewAnim.innerHeight();
    var activeWidthNewAnimWidth = activeItemNewAnim.innerWidth();
    var itemPosNewAnimTop = activeItemNewAnim.position();
    var itemPosNewAnimLeft = activeItemNewAnim.position();
    $(".hori-selector").css({
      "top":itemPosNewAnimTop.top + "px", 
      "left":itemPosNewAnimLeft.left + "px",
      "height": activeWidthNewAnimHeight + "px",
      "width": activeWidthNewAnimWidth + "px"
    });
    $("#navbarSupportedContent").on("click","li",function(e){
      $('#navbarSupportedContent ul li').removeClass("active");
      $(this).addClass('active');
      var activeWidthNewAnimHeight = $(this).innerHeight();
      var activeWidthNewAnimWidth = $(this).innerWidth();
      var itemPosNewAnimTop = $(this).position();
      var itemPosNewAnimLeft = $(this).position();
      $(".hori-selector").css({
        "top":itemPosNewAnimTop.top + "px", 
        "left":itemPosNewAnimLeft.left + "px",
        "height": activeWidthNewAnimHeight + "px",
        "width": activeWidthNewAnimWidth + "px"
      });
    });
  }
  $(document).ready(function(){
    setTimeout(function(){ test(); });
  });
  $(window).on('resize', function(){
    setTimeout(function(){ test(); }, 500);
  });
  $(".navbar-toggler").click(function(){
    $(".navbar-collapse").slideToggle(300);
    setTimeout(function(){ test(); });
  });
  
  
  
  // --------------add active class-on another-page move----------
  jQuery(document).ready(function($){
    // Get current path and find target link
    var path = window.location.pathname.split("/").pop();
  
    // Account for home page with empty path
    if ( path == '' ) {
      path = 'index.html';
    }
  
    var target = $('#navbarSupportedContent ul li a[href="'+path+'"]');
    // Add active class to target link
    target.parent().addClass('active');
  });
  
  
  
  
  // Add active class on another page linked
  // ==========================================
  // $(window).on('load',function () {
  //     var current = location.pathname;
  //     console.log(current);
  //     $('#navbarSupportedContent ul li a').each(function(){
  //         var $this = $(this);
  //         // if the current path is like this link, make it active
  //         if($this.attr('href').indexOf(current) !== -1){
  //             $this.parent().addClass('active');
  //             $this.parents('.menu-submenu').addClass('show-dropdown');
  //             $this.parents('.menu-submenu').parent().addClass('active');
  //         }else{
  //             $this.parent().removeClass('active');
  //         }
  //     })
  // });
  