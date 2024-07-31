from django.core.management.base import BaseCommand
from shop.models import Patientd
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Fixes problematic added_time values in the Patientd model'

    def handle(self, *args, **options):
        # Retrieve all records with problematic added_time values
        problematic_records = Patientd.objects.exclude(added_time__regex=r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')

        # Output the problematic records
        for record in problematic_records:
            self.stdout.write(self.style.WARNING(f"ID: {record.id}, added_time: {record.added_time}"))

        # Manually correct the values and save the records
        for record in problematic_records:
            try:
                parsed_datetime = parse_datetime(record.added_time)
                record.added_time = parsed_datetime
                record.save()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error updating record {record.id}: {e}"))
