# catalog/management/commands/_private.py

from faker import Faker
from catalog.models import Category, Brand, Product
from suppliers.models import Supplier
from inventory.models import movementType, Cellar, inventoryMovement
from users.models import User
import random

fake = Faker()


def create_categories():
    categories = ['Electrónica', 'Ropa', 'Hogar', 'Juguetes', 'Alimentos']
    for category_name in categories:
        Category.objects.get_or_create(name=category_name)


def create_brands():
    brands = ['Sony', 'Nike', 'Samsung', 'Mattel', 'Nestlé']
    for brand_name in brands:
        Brand.objects.get_or_create(name=brand_name)


def create_suppliers():
    for _ in range(3):
        Supplier.objects.get_or_create(
            rut_nif=fake.unique.ssn(),
            defaults={
                'trade_name': fake.company(),
                'company_name': fake.company(),
                'email': fake.email(),
                'telephone_number': fake.phone_number(),
                'website': fake.url(),
                'direction': fake.address(),
                'pay_conditions': 'Contado',
                'currency': 'CLP',
                'state': 'ACT'
            }
        )


def create_products():
    categories = list(Category.objects.all())
    brands = list(Brand.objects.all())
    suppliers = list(Supplier.objects.all())
    for _ in range(10):
        product = Product.objects.create(
            sku=fake.unique.random_number(digits=5),
            name=fake.word(),
            category=random.choice(categories),
            brand=random.choice(brands),
            uom_purchase='Unidad',
            uom_sale='Unidad',
            price=random.randint(1000, 100000),
            iva_tax=19.00,
            minimum_stock=10,
            maximum_stock=100
        )
        product.supplier.set(random.sample(
            suppliers, k=random.randint(1, len(suppliers))))


def create_inventory_movements():
    # Asegúrate de tener al menos un usuario, bodega y tipo de movimiento
    user, _ = User.objects.get_or_create(username='admin')
    cellar, _ = Cellar.objects.get_or_create(cellar_name='Bodega Principal')

    # Crear tipos de movimiento si no existen
    movement_types = {
        'IN': 'Ingreso',
        'OUT': 'Salida',
        'ADJ': 'Ajuste',
        'DEVOL': 'Devolucion',
        'TRANS': 'Transferencia'
    }
    for code, name in movement_types.items():
        movementType.objects.get_or_create(movement_type=code)

    products = list(Product.objects.all())
    suppliers = list(Supplier.objects.all())
    movement_types_instances = list(movementType.objects.all())

    for _ in range(10):
        inventoryMovement.objects.create(
            product=random.choice(products),
            cellar=cellar,
            user=user,
            supplier=random.choice(suppliers),
            movement_type=random.choice(movement_types_instances),
            quantity=random.randint(1, 50)
        )
