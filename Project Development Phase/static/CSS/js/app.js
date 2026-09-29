// =====================================================
// Q&A
// =====================================================

async function askQuestion() {

    const question =
        document.getElementById("question").value.trim();

    const result =
        document.getElementById("qaResult");


    if (!question) {

        result.innerText =
            "Please enter a question.";

        return;
    }


    result.innerText =
        "Thinking...";


    try {

        const response =
            await fetch("/qa", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            });


        const data =
            await response.json();


        if (data.error) {

            result.innerText =
                data.error;

        } else {

            result.innerText =
                data.answer;
        }


    } catch (error) {

        result.innerText =
            "Unable to connect to the server.";
    }
}



// =====================================================
// EXPLANATION
// =====================================================

async function explainTopic() {

    const topic =
        document.getElementById("topic").value.trim();

    const result =
        document.getElementById(
            "explanationResult"
        );


    if (!topic) {

        result.innerText =
            "Please enter a topic.";

        return;
    }


    result.innerText =
        "Generating explanation...";


    try {

        const response =
            await fetch("/explain", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    topic: topic
                })
            });


        const data =
            await response.json();


        if (data.error) {

            result.innerText =
                data.error;

        } else {

            result.innerText =
                data.explanation;
        }


    } catch (error) {

        result.innerText =
            "Unable to connect to the server.";
    }
}



// =====================================================
// SUMMARY
// =====================================================

async function summarizeText() {

    const text =
        document.getElementById(
            "summaryText"
        ).value.trim();

    const result =
        document.getElementById(
            "summaryResult"
        );


    if (!text) {

        result.innerText =
            "Please enter some text.";

        return;
    }


    result.innerText =
        "Summarizing...";


    try {

        const response =
            await fetch("/summarize", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    text: text
                })
            });


        const data =
            await response.json();


        if (data.error) {

            result.innerText =
                data.error;

        } else {

            result.innerText =
                data.summary;
        }


    } catch (error) {

        result.innerText =
            "Unable to connect to the server.";
    }
}



// =====================================================
// QUIZ
// =====================================================

async function generateQuiz() {

    const topic =
        document.getElementById(
            "quizTopic"
        ).value.trim();

    const result =
        document.getElementById(
            "quizResult"
        );


    if (!topic) {

        result.innerText =
            "Please enter a topic.";

        return;
    }


    result.innerText =
        "Generating quiz...";


    try {

        const response =
            await fetch("/quiz", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    topic: topic
                })
            });


        const data =
            await response.json();


        if (data.error) {

            result.innerText =
                data.error;

            return;
        }


        displayQuiz(data.quiz);


    } catch (error) {

        result.innerText =
            "Unable to connect to the server.";
    }
}



// =====================================================
// DISPLAY QUIZ
// =====================================================

function displayQuiz(quiz) {

    const result =
        document.getElementById(
            "quizResult"
        );


    result.innerHTML = "";


    quiz.forEach(
        function(question, index) {


            const questionBox =
                document.createElement(
                    "div"
                );


            questionBox.className =
                "quiz-question";


            const heading =
                document.createElement(
                    "h3"
                );


            heading.innerText =
                `${index + 1}. ${question.question}`;


            questionBox.appendChild(
                heading
            );


            question.options.forEach(
                function(option) {


                    const label =
                        document.createElement(
                            "label"
                        );


                    label.className =
                        "quiz-option";


                    const radio =
                        document.createElement(
                            "input"
                        );


                    radio.type =
                        "radio";


                    radio.name =
                        `question-${index}`;


                    radio.value =
                        option;


                    radio.addEventListener(
                        "change",
                        function() {


                            if (
                                option ===
                                question.answer
                            ) {

                                label.classList
                                    .add(
                                        "correct"
                                    );

                                label.innerHTML +=
                                    " ✓ Correct!";

                            } else {

                                label.classList
                                    .add(
                                        "wrong"
                                    );

                                label.innerHTML +=
                                    ` ✗ Correct answer: ${question.answer}`;
                            }

                        }
                    );


                    label.appendChild(
                        radio
                    );


                    label.appendChild(
                        document.createTextNode(
                            " " + option
                        )
                    );


                    questionBox.appendChild(
                        label
                    );

                }
            );


            result.appendChild(
                questionBox
            );

        }
    );
}



// =====================================================
// LEARNING RECOMMENDATIONS
// =====================================================

async function getLearningPath() {

    const topic =
        document.getElementById(
            "learningTopic"
        ).value.trim();

    const result =
        document.getElementById(
            "learningResult"
        );


    if (!topic) {

        result.innerText =
            "Please enter a topic.";

        return;
    }


    result.innerText =
        "Creating your learning path...";


    try {

        const response =
            await fetch(
                "/learn/recommendations",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        topic: topic
                    })
                }
            );


        const data =
            await response.json();


        if (data.error) {

            result.innerText =
                data.error;

        } else {

            result.innerText =
                data.recommendation;
        }


    } catch (error) {

        result.innerText =
            "Unable to connect to the server.";
    }
}