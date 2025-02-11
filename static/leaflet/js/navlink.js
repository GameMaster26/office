
// Add scroll shadow effect to navbar
window.onscroll = function () {
    var navbar = document.getElementById('fixed-navbar');
    if (window.pageYOffset > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
};
// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
// Active link highlighting based on scroll position (if anchors used)
const sections = document.querySelectorAll("section");
const navLi = document.querySelectorAll("nav .navbar-nav .nav-item .nav-link");
window.addEventListener("scroll", () => {
    let current = "";
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        if (scrollY >= sectionTop - 60) {
            current = section.getAttribute("id");
        }
    });
    navLi.forEach(li => {
        li.classList.remove("active");
        if (li.getAttribute("href") === "#" + current) {
            li.classList.add("active");
        }
    });
});