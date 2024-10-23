document.addEventListener('DOMContentLoaded', function () {
    let currentQuestionIndex = 0;
    let questions = [];
    let userAnswer = "";

    const interviewForm = document.getElementById('interviewForm');

    if (interviewForm) {
        document.getElementById('interviewForm').addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Get the input values
            const jobRole = document.getElementById('job_role').value.trim();
            const skills = document.getElementById('skills').value.split(',').map(skill => skill.trim());
        
            // Get the input fields and button
            const jobRoleField = document.getElementById('job_role');
            const skillsField = document.getElementById('skills');
            const startButton = event.target.querySelector('button[type="submit"]');
            const interviewForm = document.getElementById('interviewForm');
        
            // Fetch questions from server
            fetch('/interview/', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ job_role: jobRole, skills })
            })
            .then(response => response.json())
            .then(data => {
                // Hide input fields and button
                jobRoleField.style.display = 'none';
                skillsField.style.display = 'none';
                startButton.style.display = 'none';
                
                // Hide the whole form with a slide-out effect if needed
                interviewForm.style.transition = 'transform 0.5s ease-in-out';
                interviewForm.style.transform = 'translateX(-100%)';
        
                // Show questions container with a slide-in effect
                setTimeout(function () {
                    document.getElementById('questionsContainer').classList.remove('hidden');
                    document.getElementById('questionsContainer').style.transition = 'transform 0.5s ease-in-out';
                    document.getElementById('questionsContainer').style.transform = 'translateX(0)';
                    questions = data.questions; 
                    displayQuestion(); 
                }, 500); 
            })
            .catch(err => {
                alert('Error fetching questions, please try again.');
                console.error(err);
            });
        });
        

        function displayQuestion() {
            if (currentQuestionIndex < questions.length) {
                const currentQuestion = questions[currentQuestionIndex];
                document.getElementById('currentQuestion').innerHTML = `${currentQuestion}`;
                
                // Show answer container and buttons
                document.getElementById('answerContainer').classList.remove('hidden');
                document.getElementById('recordButton').classList.remove('hidden');
                document.getElementById('retryButton').classList.add('hidden'); 
                document.getElementById('submitResponseButton').classList.add('hidden'); 

                // Read aloud the question
                const utterance = new SpeechSynthesisUtterance(currentQuestion);
                speechSynthesis.speak(utterance);

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

            recordButton.onclick = function() {
                if (!isRecording) {
                    isRecording = true;
                    recordButton.style.backgroundColor = '#1967d2'; // Mic Icon
                    listenToAnswer();
                } else {
                    isRecording = false;
                    recordButton.style.backgroundColor = '#ea4335';
                }
            };
        }

        function listenToAnswer() {
            const recognizer = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognizer.lang = 'en-US';
            recognizer.interimResults = false;

            recognizer.start();

            recognizer.onresult = (event) => {
                userAnswer = event.results[0][0].transcript; 

                document.getElementById('userAnswer').style.display = "block";
                document.getElementById('userAnswer').innerText = userAnswer;
                
                document.getElementById('submitResponseButton').classList.remove('hidden');
            };

            recognizer.onerror = (event) => {
                alert("Voice recognition error. Please try again.");
                console.error(event.error);
            };
        }

        document.getElementById('submitResponseButton').addEventListener('click', function() {
            submitResponse(userAnswer, currentQuestionIndex);
        });

        function submitResponse(answer, currentIndex) {
            fetch('analyze-answer/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ answer, current_index: currentIndex })
            })
            .then(response => response.json())
            .then(data => {
                displaySuggestions(data.suggestions, data.ideal_answer);
            })
            .catch(err => {
                alert("Error analyzing answer, please try again.");
                console.error(err);
            });
        }

        function displaySuggestions(suggestions, idealAnswer) {
            const suggestionsList = suggestions.split('\n').filter(Boolean).map(item => <li>${item}</li>).join('');
           
            document.getElementById('suggestionsContainer').innerHTML =
                `<strong>Suggestions</strong><ul>${suggestionsList}</ul>`;
            document.getElementById('suggestionsContainer').classList.remove('hidden');

            document.getElementById('idealAnswerContainer').innerHTML =
                `<strong>Ideal Answer</strong><p>${idealAnswer}</p>`;
            document.getElementById('idealAnswerContainer').classList.remove('hidden');

            document.getElementById('nextButton').classList.remove('hidden');
            document.getElementById('recordButton').classList.add('hidden');
            document.getElementById('submitResponseButton').classList.add('hidden');
        }

        document.getElementById('nextButton').addEventListener('click', function() {
            currentQuestionIndex++;
            displayQuestion();
        });

        document.getElementById('retryButton').addEventListener('click', function() {
            userAnswer = ""; 
            document.getElementById('userAnswer').innerText = ""; 
            document.getElementById('recordButton').classList.remove('hidden');
        });

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
});