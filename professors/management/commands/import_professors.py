import csv
from django.core.management.base import BaseCommand
from professors.models import Professor, Department, Major, Subject

class Command(BaseCommand):
    help = 'Load professors data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # Create or get default Department and Major
        default_department, _ = Department.objects.get_or_create(name='Fakultas Ilmu Komputer dan Teknologi Informasi')
        default_major, _ = Major.objects.get_or_create(name='Sistem Informasi')

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                professor_name = row['Professors']
                subject_names = row['Subjects'].split(',')

                # Create or get Professor
                professor, created = Professor.objects.get_or_create(
                    name=professor_name,
                    defaults={'department': default_department, 'major': default_major}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created professor: {professor_name}'))

                # Add Subjects to Professor
                for subject_name in subject_names:
                    subject_name = subject_name.strip()  # Remove any extra whitespace
                    subject, _ = Subject.objects.get_or_create(name=subject_name)
                    professor.subjects.add(subject)

                professor.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
