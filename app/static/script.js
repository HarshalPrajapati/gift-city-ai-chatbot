function getCurrentTime() {

    const now = new Date();

    return now.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

}

function fillQuestion(text) {

    document
        .getElementById("question")
        .value = text;

    document
        .getElementById("question")
        .focus();

}

function scrollToBottom() {

    const chatBox =
        document.getElementById("chat-box");

    chatBox.scrollTop =
        chatBox.scrollHeight;

}

function copyAnswer(button) {

    const text =
        button.parentElement.innerText
        .replace("Copy", "");

    navigator.clipboard.writeText(text);

    button.innerHTML = "Copied!";

    setTimeout(() => {

        button.innerHTML = "Copy";

    }, 1500);

}

async function askQuestion() {

    const questionBox =
        document.getElementById("question");

    const question =
        questionBox.value.trim();

    if (!question) return;

    const chatBox =
        document.getElementById("chat-box");

    // -------------------------
    // User Message
    // -------------------------

    chatBox.innerHTML += `

        <div class="user-message">

            <strong>You</strong>

            <small style="float:right;">
                ${getCurrentTime()}
            </small>

            <br><br>

            ${question}

        </div>

    `;

    questionBox.value = "";

    scrollToBottom();

    // -------------------------
    // Assistant Placeholder
    // -------------------------

    const loadingId =
        "loading-" + Date.now();

    chatBox.innerHTML += `

        <div
            class="bot-message"
            id="${loadingId}"
        >

            <strong>Assistant</strong>

            <small style="float:right;">
                ${getCurrentTime()}
            </small>

            <br><br>

            <span class="answer"></span>

        </div>

    `;

    scrollToBottom();

    const answerSpan =
        document.querySelector(
            `#${loadingId} .answer`
        );

    try {

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                        "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );

        const reader =
            response.body.getReader();

        const decoder =
            new TextDecoder();

        let fullAnswer = "";

        while (true) {

            const {
                done,
                value
            } = await reader.read();

            if (done)
                break;

            const chunk =
                decoder.decode(value);

            fullAnswer += chunk;

            answerSpan.innerHTML = marked.parse(fullAnswer);

            scrollToBottom();

        }

        // answerSpan.innerHTML += `

        //     <br><br>

        //     <button
        //         class="copy-btn"
        //         onclick="copyAnswer(this)"
        //     >
        //         Copy
        //     </button>

        // `;

    }

    catch(error){

        answerSpan.innerHTML =
            "❌ Unable to contact chatbot.";

        console.error(error);

    }

}

document
.getElementById("question")
.addEventListener(

    "keydown",

    function(event){

        if(

            event.key==="Enter"

            &&

            !event.shiftKey

        ){

            event.preventDefault();

            askQuestion();

        }

    }

);

window.onload = () => {

    document
        .getElementById("chat-box")
        .innerHTML = `

        <div class="bot-message">

            <strong>🤖 GIFT City AI Assistant</strong>

            <br><br>

            Welcome!

            <br><br>

            I can help you with:

            <ul>

                <li>⚡ Power Connection</li>

                <li>💧 Water Connection</li>

                <li>📞 CRM Services</li>

                <li>🏢 Residential Buildings</li>

                <li>🏬 Commercial Buildings</li>

            </ul>

        </div>

    `;

    document
        .getElementById("question")
        .focus();

};