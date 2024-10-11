console.log("888888888888888888");
document.addEventListener('DOMContentLoaded', function () {
    let currentQuestionIndex = 0; // Track the current question index
    let questions = []; // Store questions
    let userAnswer = ""; // Store user's answer

    const interviewForm = document.getElementById('interviewForm');
    if (interviewForm) {
        let currentQuestionIndex = 0; // Track the current question index
        let questions = []; // Store questions
        let userAnswer = ""; // Store user's answer

        document.getElementById('interviewForm').addEventListener('submit', function(event) {
            event.preventDefault();
            
            const jobRole = document.getElementById('job_role').value.trim();
            const skills = document.getElementById('skills').value.split(',').map(skill => skill.trim());

            fetch('/interview/', { // Adjust URL as necessary
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Include CSRF token if needed
                },
                body: JSON.stringify({ job_role: jobRole, skills })
            })
            .then(response => response.json())
            .then(data => {
                questions = data.questions; // Get questions from response
                document.getElementById('questionsContainer').classList.remove('hidden');
                displayQuestion();
            });
        });

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
               
               handleRecording();
           } else {
               alert("No more questions.");
               location.reload();
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
           recordButton.onmouseleave = function() {
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
        submitResponse(userAnswer, currentQuestionIndex); // Submit answer and current index to backend for analysis
        });

        // Submit response to backend and display suggestions/ideal answers
        function submitResponse(answer, currentIndex) {
            fetch('analyze-answer/', { // Adjust URL as necessary
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Include CSRF token if needed
                },
                body: JSON.stringify({ answer, current_index: currentIndex }) // Send both answer and index
            })
            .then(response => response.json())
            .then(data => {
                displaySuggestions(data.suggestions, data.ideal_answer);
            });
        }    

       // Display suggestions and ideal answers
       function displaySuggestions(suggestions, idealAnswer) {
           const suggestionsList = suggestions.split('\n').filter(Boolean).map(item => `<li>${item}</li>`).join('');
           
           document.getElementById('suggestionsContainer').innerHTML =
               `<strong>Suggestions:</strong><ul>${suggestionsList}</ul>`;
           document.getElementById('suggestionsContainer').classList.remove('hidden');

           document.getElementById('idealAnswerContainer').innerHTML =
               `<strong>Ideal Answer:</strong><p>${idealAnswer}</p>`;
           document.getElementById('idealAnswerContainer').classList.remove('hidden');

           document.getElementById('nextButton').classList.remove('hidden'); // Show next button after suggestions are displayed
           document.getElementById('recordButton').classList.add('hidden');
           document.getElementById('submitResponseButton').classList.add('hidden');
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
          if (confirm("Exiting the interview.")) {
            location.reload();
          } 
       });

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
    }

    //Resume-uploading-functionality


    const form = document.getElementById('resume-form');
    if (form) {
        const pdfFrame = document.getElementById('pdf-container');
        const uploadButton = document.getElementById('upload-button');

        uploadButton.addEventListener('click', function (event) {
            console.log("hellloooooooo");
            event.preventDefault();

            if (form.checkValidity()) {
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

                            pdfFrame.src = data.pdf_url;
                            // displayParsedData(parsedData);

                        } else {
                            alert(data.error);
                        }
                    })
                    .catch(error => console.error('Error:', error));
            } else {
                alert('Please select a valid resume file.');
            }
        });
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

        function displayParsedData(parsedData) {
            const dataContainer = document.getElementById('parsed-data');
            dataContainer.innerHTML = '';

            const ul = document.createElement('ul');
            for (const [key, value] of Object.entries(parsedData)) {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${key}:</strong> ${value}`;
                ul.appendChild(li);
            }
            dataContainer.appendChild(ul);
        }
    }
});


