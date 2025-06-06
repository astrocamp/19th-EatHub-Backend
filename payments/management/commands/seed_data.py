from django.core.management.base import BaseCommand
from payments.models import Product

class Command(BaseCommand):
    help = 'Seed initial payment products'

    def handle(self, *args, **kwargs):
        plans = [
            {
                "name": "vip_monthly_plan",
                "plan_type": "monthly",
                "amount": 990,
                "interval_days": 30,
            },
            {
                "name": "vip_yearly_plan",
                "plan_type": "yearly",
                "amount": 10690,
                "interval_days": 365,
            }
        ]

        for plan in plans:
            obj, created = Product.objects.get_or_create(
                name=plan["name"],
                defaults=plan
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created: {obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Already exists: {obj.name}"))