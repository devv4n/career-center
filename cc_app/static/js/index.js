document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.slide');
    const prevSlideButton = document.getElementById('prev-slide');
    const nextSlideButton = document.getElementById('next-slide');
    let currentSlideIndex = 0;

    // Функция для отображения текущего слайда
    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.remove('active'); // Убираем класс "active" у всех слайдов
            if (i === index) {
                slide.classList.add('active'); // Добавляем класс "active" текущему слайду
            }
        });
    }

    // Показываем первый слайд при загрузке
    showSlide(currentSlideIndex);

    // Кнопка "Назад"
    prevSlideButton.addEventListener('click', () => {
        currentSlideIndex = (currentSlideIndex - 1 + slides.length) % slides.length; // Циклический переход назад
        showSlide(currentSlideIndex);
    });

    // Кнопка "Вперед"
    nextSlideButton.addEventListener('click', () => {
        currentSlideIndex = (currentSlideIndex + 1) % slides.length; // Циклический переход вперед
        showSlide(currentSlideIndex);
    });
});
