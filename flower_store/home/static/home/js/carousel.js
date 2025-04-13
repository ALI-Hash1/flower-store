<script>
    let currentSlide = 0;

    function showSlide(index) {
        const carouselImages = document.getElementById('carouselImages');
        const totalSlides = carouselImages.children.length;
        currentSlide = (index + totalSlides) % totalSlides;
        carouselImages.style.transform = `translateX(-${currentSlide * 100}%)`;
    }

    function nextSlide() {
        showSlide(currentSlide + 1);
    }

    function prevSlide() {
        showSlide(currentSlide - 1);
    }
</script>