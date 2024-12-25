const filterToggle = document.getElementById('filter-toggle');
const filterDropdown = document.getElementById('filter-dropdown');
const applyFiltersButton = document.getElementById('apply-filters');
const filterOptions = document.querySelectorAll('.filter-option');

// Открытие/закрытие выпадающего списка
filterToggle.addEventListener('click', () => {
    filterDropdown.style.display = filterDropdown.style.display === 'block' ? 'none' : 'block';
});

// Применение фильтров
applyFiltersButton.addEventListener('click', () => {
    const selectedFilters = Array.from(filterOptions)
        .filter(option => option.checked)
        .map(option => option.value);

    console.log('Примененные фильтры:', selectedFilters); // Можно заменить на логику фильтрации вакансий
    filterDropdown.style.display = 'none'; // Закрытие списка после применения
});
