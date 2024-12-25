document.addEventListener('DOMContentLoaded', () => {
    const themeToggleButton = document.getElementById('theme-toggle');
    const body = document.body;
    let isDarkTheme = true;

    // Переключение темы
    themeToggleButton.addEventListener('click', () => {
        isDarkTheme = !isDarkTheme;

        if (isDarkTheme) {
            body.classList.remove('light-theme');
            themeToggleButton.textContent = '🌙'; // Луна для темной темы
        } else {
            body.classList.add('light-theme');
            themeToggleButton.textContent = '☀️'; // Солнце для светлой темы
        }
    });

    // Календарь
    const calendarContainer = document.getElementById('calendar');
    const currentDate = new Date();
    const monthNames = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"];

    // Загрузка событий
    async function fetchEvents() {
        try {
            const response = await fetch('/api/events/');
            if (!response.ok) throw new Error('Ошибка загрузки событий');
            return await response.json();
        } catch (error) {
            console.error(error);
            return [];
        }
    }

    // Функция для отображения календаря
    async function generateCalendar(month, year) {
        const events = await fetchEvents(); // Получаем события
        const firstDayOfMonth = new Date(year, month).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        let calendarHTML = `<h3>${monthNames[month]} ${year}</h3><table><tr>`;
        for (let i = 0; i < 7; i++) {
            calendarHTML += `<th>${['П', 'В', 'С', 'Ч', 'П', 'С', 'В'][i]}</th>`;
        }
        calendarHTML += `</tr><tr>`;

        // Пустые ячейки до первого дня месяца
        for (let i = 0; i < firstDayOfMonth; i++) {
            calendarHTML += `<td></td>`;
        }

        // Дни месяца
        for (let day = 1; day <= daysInMonth; day++) {
            if ((firstDayOfMonth + day - 1) % 7 === 0 && day !== 1) {
                calendarHTML += `</tr><tr>`;
            }

            const dateString = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            const dayEvents = events.filter(event => event.date === dateString);

            if (dayEvents.length > 0) {
                calendarHTML += `<td class="event-day" data-date="${dateString}">
                                    ${day}
                                    <span class="event-count">${dayEvents.length}</span>
                                </td>`;
            } else {
                calendarHTML += `<td>${day}</td>`;
            }
        }

        calendarHTML += `</tr></table>`;
        calendarContainer.innerHTML = calendarHTML;

        // Добавляем обработчики кликов на дни с событиями
        document.querySelectorAll('.event-day').forEach(cell => {
            cell.addEventListener('click', () => {
                const date = cell.getAttribute('data-date');
                const dayEvents = events.filter(event => event.date === date);
                showEventDetails(dayEvents);
            });
        });
    }

    // Показ деталей события и добавление в локальный календарь
    function showEventDetails(events) {
        const event = events[0]; // Для простоты берем первое событие
        if (confirm(`Добавить событие "${event.title}" в ваш календарь?`)) {
            addToLocalCalendar(event);
        }
    }

    function addToLocalCalendar(event) {
        const start = `${event.date}T${event.time}`;
        const end = new Date(new Date(start).getTime() + 2 * 60 * 60 * 1000).toISOString();

        const calendarEvent = {
            title: event.title,
            start,
            end,
            description: event.description,
            location: event.location
        };

        try {
            const url = `https://calendar.google.com/calendar/r/eventedit?text=${encodeURIComponent(calendarEvent.title)}&dates=${start}/${end}&details=${encodeURIComponent(calendarEvent.description)}&location=${encodeURIComponent(calendarEvent.location)}`;
            window.open(url, '_blank');
        } catch (error) {
            console.error('Ошибка при добавлении в календарь:', error);
            alert('Не удалось добавить событие в календарь.');
        }
    }

    // Генерируем календарь
    generateCalendar(currentDate.getMonth(), currentDate.getFullYear());
});
