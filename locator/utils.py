from typing import Any, Dict

DS_CHOICES = [ 
        ('РП-4', 'Substation-4'),
        ('РП-5', 'Substation-5'),
        ('РП-6', 'Substation-6'),
        ('РП-7', 'Substation-7'),
        ('РП-8', 'Substation-8'),
        ]

MCC_CHOICES = [ 
        ('MCC-1', 'Motor Control Center 1'),
        ('MCC-2', 'Motor Control Center 2'),
        ('MCC-3', 'Motor Control Center 3'),
        ('MCC-4', 'Motor Control Center 4'),
        ('MCC-5', 'Motor Control Center 5'),
        ('MCC-6', 'Motor Control Center 6'),
        ('MCC-7', 'Motor Control Center 7'),
        ('MCC-8', 'Motor Control Center 8'),
        ('MCC-9', 'Motor Control Center 9'),
        ('MCC-10', 'Motor Control Center 10'),
        ('MCC-11', 'Motor Control Center 11'),
        ]

LEVELS = [
    ('Не вказaно', 'Не вказaно'),
    ('4.8', '4.8m'),
    ('8.0', '8.0m'),
    ('11.2', '11.2m'),
    ('15.4', '15.4m'),
    ('21.0', '21.0m'),
    ('25.6', '25.6m'),
    ('28.0', '28.0m'),
    ('32.0', '32.0m'),
]


class DataMixin:
    title_page = None
    extra_context = {}

    def __init__(self) -> None:
        if self.title_page:
            self.extra_context['title'] = self.title_page
