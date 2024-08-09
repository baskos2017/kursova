let currentSlide = 0;

function showSlide(index) {
    const slides = document.querySelectorAll('.slide');
    if (index >= slides.length) { currentSlide = 0; }
    if (index < 0) { currentSlide = slides.length - 1; }
    slides.forEach(slide => slide.style.display = 'none');
    slides[currentSlide].style.display = 'block';
}

document.querySelector('.next').onclick = () => showSlide(++currentSlide);
document.querySelector('.prev').onclick = () => showSlide(--currentSlide);
showSlide(currentSlide);
