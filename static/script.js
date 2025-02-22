const lenis = new Lenis();
lenis.on("scroll", ScrollTrigger.update);
gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
});
gsap.ticker.lagSmoothing(0)


gsap.registerPlugin(ScrollTrigger);

ScrollTrigger.create({
    trigger: ".pinned",
    start: "top top",
    endTrigger: ".whitespace",
    end: "bottom top",
    pin: true,
    pinSpacing: false,
});

ScrollTrigger.create({
    trigger: ".header-info",
    start: "top top",
    endTrigger: ".whitespace",
    end: "bottom top",
    pin: true,
    pinSpacing: false
});


ScrollTrigger.create({
    trigger: ".pinned",
    start: "top top",
    endTrigger: ".header-info",
    end: "bottom bottom",
    onUpdate: (self) => {
        const rotation = self.progress * 360
        gsap.to(".revealer", { rotation });
    },
});


ScrollTrigger.create({
    trigger: ".pinned",
    start: "top top",
    endTrigger: ".header-info",
    end: "bottom bottom",
    onUpdate: (self) => {
        const progress = self.progress;
        const clipPath = `polygon(
    ${45 - 45 * progress}% ${0 + 0 * progress}%,
    ${55 + 45 * progress}% ${0 + 0 * progress}%,
    ${55 + 45 * progress}% ${100 - 0 * progress}%,
    ${45 - 45 * progress}% ${100 - 0 * progress}% 
            )`;
        gsap.to(".revealer-1, .revealer-2", {
            clipPath: clipPath,
            ease: "none",
            duration: 0,
        });
    },
});
ScrollTrigger.create({
    trigger: ".header-info",
    start: "top top",
    end: "bottom 50%",
    scrub: 1,
    onUpdate: (self) => {
        const progress = self.progress;
        const left = 35 + 15 * progress;
        gsap.to(".revealer", {
            left: `${left}%`,
            ease: "none",
            duration: 0,
        });
    },
});


ScrollTrigger.create({
    trigger: ".whitespace",
    start: "top 50%",
    end: "bottom bottom",
    scrub: 1,
    onUpdate: (self) => {
        const scale = 1 + 16 * self.progress;
        gsap.to(".revealer", {
            scale: scale,
            ease: "none",
            duration: 0,
        });
    },
});

document.getElementById('navbarToggler').addEventListener('click', function () {
    document.getElementById('navbarLinks').classList.toggle('active');
});





var menu = document.querySelector("#nav i");
var cross = document.querySelector("#full i");

// GSAP animation timeline for the menu
var tl = gsap.timeline();
tl.to("#full", {
    right: 0,
    duration: 0.5
});
tl.from("#full h4", {
    x: 150,
    duration: 0.3,
    stagger: 0.2,
    opacity: 0
});
tl.from("#full i", {
    opacity: 0
});
tl.pause();

// Event listeners for menu and close icons
menu.addEventListener("click", function () {
    tl.play();
});

cross.addEventListener("click", function () {
    tl.reverse();
});



var pos = document.documentElement;
pos.addEventListener('mousemove', e => {
    pos.style.setProperty('--x', e.clientX + 'px')
    pos.style.setProperty('--y', e.clienty + 'px')
})
