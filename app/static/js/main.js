let currentQuestions = [];
let currentQuestionIndex = 0;
let currentFileId = null;
let currentQuestionId = null;

// DOM Elements
const currentQuestionElement = document.getElementById("current-question");
const answerInput = document.getElementById("answer-input");
const submitButton = document.getElementById("submit-answer");
const nextButton = document.getElementById("next-question");
const feedbackSection = document.getElementById("feedback-section");
const evaluationResult = document.getElementById("evaluation-result");
const uploadForm = document.getElementById("upload-form");
const uploadSection = document.getElementById("upload-section");
const questionSection = document.getElementById("question-section");
const selectedFileName = document.getElementById("selected-file-name");
const uploadStatus = document.getElementById("upload-status");
const errorMessage = document.getElementById("error-message");
const errorContainer = document.getElementById("error-container");
const retryButton = document.getElementById("retry-button");
const jobDetailsContainer = document.getElementById("job-details-container");
const toggleDetailsButton = document.getElementById("toggle-details");
const jobDetailsElement = document.getElementById("job-details");
const multipleChoiceContainer = document.getElementById("multiple-choice-container");
const optionsList = document.getElementById("options-list");

// Handle file selection
function handleFileSelection(event) {
  const file = event.target.files[0];
  if (file) {
    selectedFileName.textContent = file.name;
    uploadStatus.textContent = "Upload Status: Ready to upload";
    uploadStatus.classList.remove("success", "error", "processing");
    uploadStatus.classList.add("ready");
  }
}

// Handle file upload
async function handleFileUpload(event) {
  event.preventDefault(); // Prevent default form submission
  const fileInput = document.getElementById("job-file");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a file to upload");
    return;
  }

  // Check file size (e.g., max 10MB)
  const maxSize = 10 * 1024 * 1024; // 10MB
  if (file.size > maxSize) {
    alert("File size is too large. Please upload a file smaller than 10MB.");
    return;
  }

  uploadStatus.textContent = "Upload Status: Processing...";
  uploadStatus.classList.remove("ready", "success", "error");
  uploadStatus.classList.add("processing");

  const formData = new FormData();
  formData.append("document", file);

  try {
    const response = await fetch("/api/job", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Server error");
    }

    currentFileId = result.file_id;
    uploadStatus.textContent = "Upload Status: Success!";
    uploadStatus.classList.remove("processing");
    uploadStatus.classList.add("success");

    // Hide upload section and show question section
    uploadSection.classList.add("hidden");
    questionSection.classList.remove("hidden");

    // Fetch questions with the file_id
    await fetchQuestions();
  } catch (error) {
    console.error("Error uploading file:", error);
    uploadStatus.textContent = `Upload Status: Error - ${error.message}`;
    uploadStatus.classList.remove("processing");
    uploadStatus.classList.add("error");
  }
}

// Fetch questions with file_id
async function fetchQuestions() {
  if (!currentFileId) {
    console.error("No file_id available. Please upload a file first.");
    return;
  }

  try {
    const response = await fetch(`/api/questions?file_id=${currentFileId}`);
    const data = await response.json();

    if (response.status !== 200) {
      throw new Error(data.message || "Error fetching questions");
    }

    const question = data.question;
    currentQuestionId = data.question_id; // Store the question_id
    currentQuestions = [question]; // Wrap single question in array since our code expects an array
    displayCurrentQuestion();

    // Update job details display but keep it hidden
    updateJobDetailsDisplay(data.job_details);

    // Hide feedback section when moving to a new question
    feedbackSection.classList.add("hidden");

    // Hide error container if it was shown
    errorContainer.classList.add("hidden");
  } catch (error) {
    console.error("Error fetching questions:", error);
    currentQuestionElement.textContent = "";

    // Show error container with retry button
    errorContainer.classList.remove("hidden");
    errorMessage.textContent = error.message || "Error loading questions";
  }
}

// Update job details display
function updateJobDetailsDisplay(jobDetails) {
  if (!jobDetails) return;

  const html = `
        <div class="details-group">
            <h4>Job Title</h4>
            <p>${jobDetails.job_title}</p>
        </div>
        <div class="details-group">
            <h4>Job Description</h4>
            <p>${jobDetails.job_description}</p>
        </div>
        <div class="details-group">
            <h4>Skills</h4>
            <ul>
                ${jobDetails.skills.map((skill) => `<li><span>${skill}</span></li>`).join("")}
            </ul>
        </div>
    `;

  jobDetailsElement.innerHTML = html;
  // Only show the container if it's currently hidden
  if (jobDetailsContainer.classList.contains("hidden")) {
    jobDetailsContainer.classList.add("hidden");
  }
}

// Toggle job details visibility
function toggleJobDetails() {
  jobDetailsContainer.classList.toggle("hidden");
  const isHidden = jobDetailsContainer.classList.contains("hidden");
  toggleDetailsButton.textContent = isHidden ? "Show Job Details" : "Hide Job Details";
}

// Display the current question
function displayCurrentQuestion() {
  if (currentQuestions.length === 0) return;

  const questionData = currentQuestions[currentQuestionIndex];
  console.log("QUESTION DATA: ", questionData);

  // Calculate difficulty color based on score (0-10)
  const difficultyColor = getDifficultyColor(questionData.difficulty);

  currentQuestionElement.innerHTML = `
        <div class="question-container">
            <div class="difficulty-indicator" style="background-color: ${difficultyColor}">
                <span class="difficulty-text">Difficulty: ${questionData.difficulty}/10</span>
            </div>
            <div class="question-text">${questionData.question}</div>
            ${
              questionData.question_type === "code"
                ? `
                <div class="test-cases">
                    <h3>Test Cases:</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Input</th>
                                <th>Expected Output</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${questionData.test_cases
                              .map(
                                (test) => `
                            <tr>
                                <td><code>${JSON.stringify(test.input, null, 2)}</code></td>
                                <td><code>${JSON.stringify(test.expected_output, null, 2)}</code></td>
                            </tr>
                        `
                              )
                              .join("")}
                        </tbody>
                    </table>
                </div>
              `
                : `
                <div class="multiple-choice-options">
                    <h3>Select the correct answer:</h3>
                    <div class="options-container">
                        ${questionData.test_cases
                          .map(
                            (option, index) => `
                            <div class="option-item">
                                <input 
                                    type="radio" 
                                    id="option-${index}" 
                                    name="answer" 
                                    value="${JSON.stringify(option)}"
                                >
                                <label for="option-${index}">
                                    ${option}
                                </label>
                            </div>
                        `
                          )
                          .join("")}
                    </div>
                </div>
              `
            }
        </div>`;

  // Show/hide appropriate answer input based on question type
  if (questionData.question_type === "code") {
    answerInput.classList.remove("hidden");
    multipleChoiceContainer.classList.add("hidden");
  } else {
    answerInput.classList.add("hidden");
    multipleChoiceContainer.classList.remove("hidden");
  }

  // Reset answer input
  answerInput.value = "";
  const selectedOption = document.querySelector('input[name="answer"]:checked');
  if (selectedOption) {
    selectedOption.checked = false;
  }
}

// Helper function to get difficulty color
function getDifficultyColor(difficulty) {
  if (difficulty >= 7) return "#ff4444"; // Red for hard
  if (difficulty >= 4) return "#ffa500"; // Orange for medium
  return "#4CAF50"; // Green for easy
}

// Submit answer with file_id
async function submitAnswer() {
  let answer;

  if (currentQuestions[currentQuestionIndex].question_type === "code") {
    answer = answerInput.value.trim();
    if (!answer) {
      alert("Please provide an answer before submitting.");
      return;
    }
  } else {
    const selectedOption = document.querySelector('input[name="answer"]:checked');
    if (!selectedOption) {
      alert("Please select an answer before submitting.");
      return;
    }
    answer = selectedOption.value;
  }

  if (!currentFileId) {
    alert("No file uploaded. Please upload a job document first.");
    return;
  }

  if (!currentQuestionId) {
    alert("No question selected. Please fetch a question first.");
    return;
  }

  submitButton.disabled = true;
  submitButton.innerHTML = `
    <span class="loading">
      <span>Submitting...</span>
    </span>
  `;

  try {
    const response = await fetch("/api/evaluate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        file_id: currentFileId,
        question_id: currentQuestionId,
        answer: answer,
        // question_type: currentQuestions[currentQuestionIndex].question_type,
      }),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Server error");
    }

    displayFeedback(result);
    nextButton.disabled = false;
  } catch (error) {
    console.error("Error submitting answer:", error);
    alert("Error submitting answer: " + error.message);
  } finally {
    submitButton.disabled = false;
    submitButton.innerHTML = "Submit Answer";
  }
}

// Display feedback from evaluation
function displayFeedback(evaluation) {
  feedbackSection.classList.remove("hidden");

  const testCasesHtml = `
        ${
          evaluation.passed_test_cases.length > 0
            ? `
            <div class="test-cases-section passed">
                <h4>✅ Passed Test Cases:</h4>
                <ul>
                    ${evaluation.passed_test_cases
                      .map(
                        (test) => `
                    <li>
                        <strong>Input:</strong> <code>${JSON.stringify(test.input, null, 2)}</code><br>
                        <strong>Expected:</strong> <code>${JSON.stringify(test.expected_output, null, 2)}</code><br>
                    </li>
                `
                      )
                      .join("")}
                </ul>
            </div>
        `
            : ""
        }
        ${
          evaluation.failed_test_cases.length > 0
            ? `
            <div class="test-cases-section failed">
                <h4>❌ Failed Test Cases:</h4>
                <ul>
                    ${evaluation.failed_test_cases
                      .map(
                        (test) => `
                    <li>
                        <strong>Input:</strong> <code>${JSON.stringify(test.input, null, 2)}</code><br>
                        <strong>Expected:</strong> <code>${JSON.stringify(test.expected_output, null, 2)}</code><br>
                        <strong>Received:</strong> <code>${JSON.stringify(test.actual_output, null, 2)}</code>
                    </li>
                `
                      )
                      .join("")}
                </ul>
            </div>
        `
            : ""
        }
    `;

  evaluationResult.innerHTML = `
        <div class="score ${evaluation.score >= 7 ? "high-score" : evaluation.score >= 4 ? "medium-score" : "low-score"}">
            <p><strong>Score:</strong> ${evaluation.score}/10</p>
        </div>
        <div class="feedback">
            <p><strong>Feedback:</strong> ${evaluation.feedback}</p>
        </div>
        ${testCasesHtml}
    `;

  const nextButton = document.getElementById("next-question");
  if (evaluation.failed_test_cases.length > 0) {
    nextButton.disabled = true;
    nextButton.title = "Fix failed test cases before moving to the next question";
  } else {
    nextButton.disabled = false;
    nextButton.title = "Move to next question";
  }
}

// Event Listeners
submitButton.addEventListener("click", submitAnswer);
nextButton.addEventListener("click", fetchQuestions);
uploadForm.addEventListener("submit", handleFileUpload);
document.getElementById("job-file").addEventListener("change", handleFileSelection);
document.getElementById("back-button").addEventListener("click", handleBackClick);
retryButton.addEventListener("click", fetchQuestions);
toggleDetailsButton.addEventListener("click", toggleJobDetails);

// Initialize - Don't fetch questions initially
// fetchQuestions();

function handleBackClick() {
  // Reset the file input
  document.getElementById("job-file").value = "";
  selectedFileName.textContent = "No file selected";
  uploadStatus.textContent = "Upload Status: Not uploaded";
  uploadStatus.classList.remove("success", "error", "processing");

  // Show upload section and hide question section
  uploadSection.classList.remove("hidden");
  questionSection.classList.add("hidden");

  // Reset questions state
  currentQuestions = [];
  currentQuestionIndex = 0;
  currentFileId = null;
  currentQuestionId = null;

  // Hide feedback section when going back
  feedbackSection.classList.add("hidden");

  // Hide error container if it was shown
  errorContainer.classList.add("hidden");
}
