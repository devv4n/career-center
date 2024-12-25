import openpyxl
from django.http import HttpResponse
from django.contrib import admin
from .models import Event, Vacancy, StudentForm
from django.contrib.admin.actions import delete_selected as original_delete_selected


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'is_active')
    search_fields = ('name', 'description', 'location')
    list_filter = ('is_active', 'date')
    ordering = ('-date',)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'job_type', 'location', 'is_active', 'created_at')
    search_fields = ('title', 'employer', 'responsibilities', 'requirements', 'conditions', 'location', 'contact_person', 'contact_email')
    list_filter = ('job_type', 'is_active', 'created_at')
    ordering = ('-created_at',)
    actions = ['make_active', 'make_inactive', 'custom_delete_selected', 'export_to_excel']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Сделать выбранные вакансии активными"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Сделать выбранные вакансии неактивными"

    original_delete_selected.short_description = "Удалить выбранное"

    def export_to_excel(self, request, queryset):
        import openpyxl
        from django.http import HttpResponse

        # Создание Excel файла
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "Вакансии"

        # Заголовки колонок
        headers = [
            'ID', 'Название', 'Работодатель', 'Обязанности', 'Требования',
            'Условия', 'Локация', 'Контактное лицо', 'Телефон', 'Email',
            'Дополнительные контакты', 'Тип работы', 'Активна', 'Дата создания'
        ]
        worksheet.append(headers)

        # Добавление данных
        for vacancy in queryset:
            worksheet.append([
                vacancy.id,
                vacancy.title,
                vacancy.employer,
                vacancy.responsibilities,
                vacancy.requirements,
                vacancy.conditions,
                vacancy.location,
                vacancy.contact_person,
                vacancy.contact_phone,
                vacancy.contact_email,
                vacancy.additional_contacts or '',
                vacancy.get_job_type_display(),
                'Да' if vacancy.is_active else 'Нет',
                vacancy.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                ])

        # Генерация ответа
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="vacancies.xlsx"'
        workbook.save(response)
        return response

    export_to_excel.short_description = "Выгрузить выбранные вакансии в Excel"


@admin.register(StudentForm)
class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'vacancy', 'submitted_at')
    search_fields = ('first_name', 'last_name', 'email', 'vacancy__title')
    list_filter = ('vacancy', 'submitted_at')
    ordering = ('-submitted_at',)
    actions = ['export_to_excel']

    def export_to_excel(self, request, queryset):
        # Создание Excel файла
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "Заявки студентов"

        # Заголовки колонок (все поля модели StudentForm)
        headers = [
            'ID', 'Имя', 'Фамилия', 'Email', 'Телефон', 'Факультет', 'Навыки',
            'Опыт работы', 'Уровень образования', 'Другое образование', 'Примечание',
             'Вакансия', 'Дата подачи'
        ]
        worksheet.append(headers)

        # Добавление данных (все поля модели)
        for student in queryset:
            worksheet.append([
                student.id,
                student.first_name,
                student.last_name,
                student.email,
                student.phone,
                dict(StudentForm.FACULTY_CHOICES).get(student.faculty, 'Не указано'),
                student.skills,
                'Да' if student.work_experience else 'Нет',
                dict(StudentForm.EDUCATION_LEVEL_CHOICES).get(student.education_level, 'Не указано'),
                student.other_education or 'Не указано',
                student.note or 'Нет',
                student.vacancy.title if student.vacancy else 'Не указана',
                student.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
                ])

        # Генерация ответа
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="students.xlsx"'
        workbook.save(response)
        return response

    export_to_excel.short_description = "Выгрузить выбранные заявки студентов в Excel"