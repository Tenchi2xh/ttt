const numBackgrounds = 300;

function setRandomBackground() {
    let n = Math.floor(1 + Math.random() * numBackgrounds);

    if (n === 5) {
        ++n;  // 5 has gone missing. If anyone has found 5, please let me know.
    }

    let formatted = n.toString().padStart(3, "0");
    document.documentElement.style.setProperty("--random-bg", `url("backgrounds/${formatted}.png")`);
}

setRandomBackground();
