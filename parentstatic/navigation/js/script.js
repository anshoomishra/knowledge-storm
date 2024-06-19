document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.getElementById('navbar');

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Simulate user authentication check
    const userAuthenticated = true; // Change this to your actual authentication check
    const userDropdown = document.getElementById('userDropdown');
    if (!userAuthenticated) {
        userDropdown.style.display = 'none';
    }
});
