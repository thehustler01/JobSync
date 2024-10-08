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

//Resume Uploading Functionality
const pdfFrame= document.getElementById('pdf-container'); 
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('resume-form'); 
    const uploadButton = document.getElementById('upload-button'); 

    uploadButton.addEventListener('click', function(event) {
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
            .then(async data => {
                if (data.success) {
                    const pdfResponse = await fetch(data.pdf_url); // Fetch the PDF URL
                    // console.log(pdfResponse);
                    const pdfText = await pdfResponse.text(); // Get the text content
                    pdfFrame.src = 'data:application/pdf;base64,' + btoa(pdfText); 
                } else {
                    alert(data.error);
                }
            })
            .catch(error => console.error('Error:', error));
        } else {
            alert('Please select a valid resume file.');
        }
    });
//     .then(response => {
//         if (response.ok) {
//             return response.blob();  // Get the PDF as a Blob
//         } else {
//             alert('Error uploading file.');
//             return null;
//         }
//     })
//     .then(blob => {
//         if (blob) {
//             // Create a URL for the Blob and set it as the iframe src
//             const fileUrl = URL.createObjectURL(blob);
//             displayPDF(fileUrl); 
//         }
//     })
//     .catch(error => console.error('Error:', error));
// } else {
//     alert('Please select a valid resume file.');
// }
// });

function displayPDF(fileUrl) {
    // Display the PDF in an iframe
    iframeContainer.innerHTML = '';  // Clear any previous content
    const iframe = document.createElement('iframe');
    iframe.src = fileUrl;
    iframe.width = '100%';
    iframe.height = '600px';
    iframeContainer.appendChild(iframe);
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
});
