function applyScrollEffects() {
    const scrollEffects = document.querySelectorAll('.scroll-effect');
    scrollEffects.forEach(effect => {
        const rect = effect.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom >= 0) {
            effect.classList.add('visible');
        } else {
            effect.classList.remove('visible');
        }
    });

    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom >= 0) {
            section.classList.add('visible');
        } else {
            section.classList.remove('visible');
        }
    });

    const testimonials = document.querySelectorAll('.testimonial');
    testimonials.forEach(testimonial => {
        const rect = testimonial.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom >= 0) {
            testimonial.classList.add('visible');
        } else {
            testimonial.classList.remove('visible');
        }
    });
}

// Run the scroll effect logic on load
window.addEventListener('load', applyScrollEffects);

// Also run on scroll
window.addEventListener('scroll', applyScrollEffects);