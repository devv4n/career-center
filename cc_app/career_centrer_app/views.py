from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .forms import StudentApplicationForm, VacancyForm
from .models import Vacancy, Event


def about(request):
    return render(request, 'about.html')


def home(request):
    images = [
        "https://kubsau.ru/upload/resize_cache/iblock/3f1/1024_1024_1/zsnluihlrdoqv7btqjgnyiv5eey6c3s9.jpg",
        "https://kubsau.ru/upload/resize_cache/iblock/b01/1024_1024_1/bfadmz0d8e8kscuuxe139l0980zfsyrg.jpg",
        "https://kubsau.ru/upload/resize_cache/iblock/5d0/1020_577_2/ybvf1ydod9m2zrr4unavyuf2ioshug72.jpg",
        "https://kubsau.ru/upload/resize_cache/iblock/5d7/1020_577_2/t3qr97wgnvb19sxqhhylw8g4ukbljtki.jpg"
    ]
    return render(request, 'home.html', {'images': images})


def vacancy_list(request):
    search_query = request.GET.get('search', '')
    job_types = request.GET.getlist('job_type')

    # Фильтрация вакансий
    vacancies = Vacancy.objects.filter(is_active=True).order_by('-created_at')
    if search_query:
        vacancies = vacancies.filter(title__icontains=search_query)
    if job_types:
        vacancies = vacancies.filter(job_type__in=job_types)

    # Пагинация
    paginator = Paginator(vacancies, 10)  # 10 вакансий на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vacancy_list.html', {
        'vacancies': page_obj.object_list,  # Объекты текущей страницы
        'page_obj': page_obj,               # Объект пагинации для шаблона
        'search_query': search_query,       # Для сохранения запроса в форме
        'job_types': job_types,             # Для сохранения фильтров в форме
    })

def vacancy_detail(request, id):
    vacancy = get_object_or_404(Vacancy, id=id, is_active=True)
    return render(request, 'vacancy.html', {'vacancy': vacancy})


def event_list(request):
    events = Event.objects.filter(is_active=True).order_by('-date')
    paginator = Paginator(events, 10)  # Показывать по 10 событий на странице

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'event_list.html', {'page_obj': page_obj})


def event_detail(request, id):
    event = get_object_or_404(Event, id=id, is_active=True)
    return render(request, 'event.html', {'event': event})


def student_application(request):
    vacancy_id = request.GET.get('vacancy')
    vacancy = None
    if vacancy_id:
        vacancy = get_object_or_404(Vacancy, id=vacancy_id, is_active=True)

    if request.method == 'POST':
        form = StudentApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            if vacancy:
                application.vacancy = vacancy
            application.save()

            # Отправка письма
            subject = 'Новая заявка студента'
            to_email = settings.APPLICATION_EMAIL
            context = {'application': application}
            message = render_to_string('emails/student.html', context)
            send_mail(
                subject,
                '',  # Пустой текстовый контент
                settings.DEFAULT_FROM_EMAIL,
                [to_email],
                html_message=message,
            )

            # Рендер того же шаблона с флагом успеха
            vacancies = Vacancy.objects.filter(is_active=True)
            form = StudentApplicationForm()  # Очистка формы после отправки
            return render(request, 'student_application.html', {
                'form': form,
                'vacancy': vacancy,
                'vacancies': vacancies,
                'success': True
            })
    else:
        form = StudentApplicationForm()
        if vacancy:
            form.fields['vacancy'].initial = vacancy.id

    vacancies = Vacancy.objects.filter(is_active=True)
    return render(request, 'student_application.html', {
        'form': form,
        'vacancy': vacancy,
        'vacancies': vacancies
    })


def submit_vacancy(request):
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.is_active = False  # Вакансия неактивна по умолчанию
            vacancy.save()

            # Уведомление администратора
            subject = 'Новая Заявка на Добавление Вакансии'
            to_email = settings.APPLICATION_EMAIL
            context = {'vacancy': vacancy}
            message = render_to_string('emails/vacancy.html', context)
            send_mail(
                subject,
                '',
                settings.DEFAULT_FROM_EMAIL,
                [to_email],
                html_message=message,
            )

            # Очистка формы после успешной отправки
            form = VacancyForm()  # Очистка формы после отправки
            events = Event.objects.filter(is_active=True)
            return render(request, 'submit_vacancy.html', {
                'form': form,
                'success': True
            })
    else:
        form = VacancyForm()

    return render(request, 'submit_vacancy.html', {
        'form': form,
    })