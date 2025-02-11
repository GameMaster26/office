
        // Detect scrolling
        window.onscroll = function() {
            const backToTopButton = document.getElementById("back-to-top");
    
            if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
                // Show the button if scrolled down more than 300px
                backToTopButton.style.display = "block";
            } else {
                // Hide the button if scrolled up
                backToTopButton.style.display = "none";
            }
        };
    
        // Smooth scrolling for back to top button
        document.getElementById("back-to-top").addEventListener("click", function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });