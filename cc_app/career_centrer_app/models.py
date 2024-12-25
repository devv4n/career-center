from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название мероприятия")
    description = models.TextField(verbose_name="Описание")
    date = models.DateTimeField(verbose_name="Дата и время")
    location = models.CharField(max_length=255, verbose_name="Место проведения")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Мероприятие"  # Название в единственном числе
        verbose_name_plural = "Мероприятия"  # Название во множественном числе

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    JOB_TYPE_CHOICES = [
        ('FULL_TIME', 'Полный день'),
        ('PART_TIME', 'Частичная занятость'),
        ('REMOTE', 'Удаленная работа'),
        ('CONTRACT', 'Контракт'),
    ]

    title = models.CharField(max_length=200, verbose_name="Вакансия")
    employer = models.CharField(max_length=255, verbose_name="Работодатель")
    responsibilities = models.TextField(verbose_name="Обязанности")
    requirements = models.TextField(verbose_name="Требования к претенденту")
    conditions = models.TextField(verbose_name="Условия работы, льготы")
    location = models.CharField(max_length=255, verbose_name="Предполагаемое место работы")
    contact_person = models.CharField(max_length=255, verbose_name="Контактное лицо")
    contact_phone = models.CharField(max_length=20, verbose_name="Телефон")
    contact_email = models.EmailField(verbose_name="Электронная почта")
    additional_contacts = models.TextField(blank=True, null=True, verbose_name="Дополнительная контактная информация")

    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='FULL_TIME', verbose_name="Тип занятости")
    is_active = models.BooleanField(default=False, verbose_name="Активна")  # По умолчанию неактивна
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Вакансия"  # Название в единственном числе
        verbose_name_plural = "Вакансии"  # Название во множественном числе

    def __str__(self):
        return self.title


class StudentForm(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ('SPO', 'Среднее профессиональное образование'),
        ('BA', 'Высшее образование - бакалавриат'),
        ('MA', 'Высшее образование - магистратура'),
        ('SPECIALIST', 'Высшее образование - специалитет'),
        ('PHC', 'Высшее образование - подготовка кадров высшей квалификации'),
        ('OTHER', 'Другое')
    ]

    FACULTY_CHOICES = [
        ('AGROECOLOGY', 'Агрономии и экологии'),
        ('AGROCHEMISTRY', 'Агрохимии и защиты растений'),
        ('ARCHITECTURE', 'Архитектурно-строительный'),
        ('VETERINARY', 'Ветеринарной медицины'),
        ('HYDROMELIORATION', 'Гидромелиорации'),
        ('LAND_MANAGEMENT', 'Землеустроительный'),
        ('ZOOTECHNICS', 'Зоотехнии'),
        ('DIGITAL_ECONOMY', 'Институт цифровой экономики и инноваций'),
        ('MECHANIZATION', 'Механизации'),
        ('FOOD_PRODUCTION', 'Пищевых производств и биотехнологий'),
        ('HORTICULTURE', 'Плодоовощеводства и виноградарства'),
        ('APPLIED_INFORMATICS', 'Прикладной информатики'),
        ('MANAGEMENT', 'Управления'),
        ('ACCOUNTING_FINANCE', 'Учетно-финансовый'),
        ('FINANCE_CREDIT', 'Финансы и кредит'),
        ('ECONOMICS', 'Экономический'),
        ('ENERGY', 'Энергетики'),
        ('LAW', 'Юридический'),
    ]

    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Электронная почта')
    phone = models.CharField(max_length=15, verbose_name='Номер телефона')
    faculty = models.CharField(
        max_length=50,
        choices=FACULTY_CHOICES,
        verbose_name='Факультет',
    )
    skills = models.TextField(verbose_name='Какими навыками Вы обладаете?')
    work_experience = models.BooleanField(default=False, verbose_name='Имеете ли Вы опыт работы в данной сфере?')
    education_level = models.CharField(
        max_length=100,
        choices=EDUCATION_LEVEL_CHOICES,
        verbose_name='Какой у Вас уровень образования?'
    )
    other_education = models.CharField(max_length=100, blank=True, null=True, verbose_name='Другое образование')
    note = models.TextField(blank=True, null=True, verbose_name='Примечание')
    resume = models.FileField(upload_to='resumes/', null=True, blank=True, verbose_name='Резюме')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=True,related_name='applications', verbose_name="Вакансия")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи")

    class Meta:
        verbose_name = "Отклик"  # Название в единственном числе
        verbose_name_plural = "Отклики"  # Название во множественном числе

    def __str__(self):
        return f"{self.first_name} {self.last_name}"