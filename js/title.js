const acronyms = [
    "tactical tile texturer",
    "tenchi's terminal toys",
    "tenchi's terminal typography",
    "tenchi's text tiler",
    "tenchi's tiling toolkit",
    "terminal text transformer",
    "terminal tile toolkit",
    "terminal tile typography",
    "terminal typography toolkit",
    "text to tiles",
    "textured terminal transmitter",
    "tiny tile tool",

    "teenage terminal turtles",
    "the turing test",
    "totally transparent tuna",
    "totally tubular tool",
];

// Shuffle
for (let i = acronyms.length - 1; i >= 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [acronyms[i], acronyms[j]] = [acronyms[j], acronyms[i]];
}

const typingSpeed = 80;
const deleteSpeed = 50;
const typingWait = 500;
const deleteWait = 5000;

function animateLogo() {
    const logo = document.querySelector(".logo a");

    let currentAcronym = 0;

    function typeAcronym() {
        const acronym = acronyms[currentAcronym];
        let currentText = "";
        let i = 0;

        const typing = setInterval(() => {
            if (i < acronym.length) {
                currentText += acronym[i];
                logo.textContent = `ttt: ${currentText}`;
                i++;
            } else {
                clearInterval(typing);
                setTimeout(() => {
                    deleteAcronym();
                }, deleteWait);
            }
        }, typingSpeed);
    }

    function deleteAcronym() {
        let currentText = logo.textContent;
        const deletingInterval = setInterval(() => {
            if (currentText.length > 4) { // Keep "ttt:" intact
                currentText = currentText.slice(0, -1);
                logo.textContent = currentText;
            } else {
                clearInterval(deletingInterval);
                setTimeout(() => {
                    currentAcronym = (currentAcronym + 1) % acronyms.length;
                    typeAcronym();
                }, typingWait);
            }
        }, deleteSpeed);
    }

    typeAcronym();
}

document.addEventListener("DOMContentLoaded", function() {
    animateLogo();
});
