const numBackgrounds = 300;

function setRandomBackground() {
    let n = Math.floor(1 + Math.random() * numBackgrounds);

    if (n === 5) {
        ++n;  // 5 has gone missing. If anyone has found 5, please let me know.
    }

    let formatted = n.toString().padStart(3, "0");
    document.documentElement.style.setProperty("--random-bg", `url("backgrounds/${formatted}.png")`);
}

document.addEventListener("DOMContentLoaded", function () {
    const headings = document.querySelectorAll("main h1, main h2, main h3");
    const tocLinks = document.querySelectorAll(".sticky-toc a");

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    tocLinks.forEach((link) => {
                        link.classList.toggle("active", link.getAttribute("href") === `#${entry.target.id}`);
                    });
                }
            });
        },
        { rootMargin: "-50px 0px -70% 0px", threshold: 0.6 }
    );

    headings.forEach((heading) => observer.observe(heading));
});

setRandomBackground();
