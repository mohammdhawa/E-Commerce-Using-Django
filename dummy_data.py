import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from faker import Faker
import random
from products.models import (Product, ProductImages, Brand, Review)
from django.contrib.auth.models import User


mystr_tr = """
Yazılım Mühendisliği Bölümü, Türkiye'nin ihtiyacı olan geniş kapsamlı yazılımların ülke içinde en güvenilir biçimde yapılabilmesi, giderek kritik hâle gelen metro, havaalanı yönetimi, nükleer reaktör yönetimi, savunma ve benzeri alanlarda kullanılacak yazılımların sıfır hataya yakın tekniklerle ülkemizde geliştirilebilmesi misyonu doğrultusunda çalışacak yazılımcılar yetiştirmeyi amaçlamaktadır.  Bu konularda, çağdaş teorik ve pratik bilgilerle donatılmış yazılım mühendislerini yetiştirmek, ekonominin gereksinim duyduğu teknolojiyi yönlendirebilmek bakımından çok önemlidir. Bu görevi, üniversitelerin yazılım mühendisliği bölümleri üstlenmiştir. 
"""

mystr_tr2 = """Yazılım Mühendisliği Bölümü, Türkiye'nin ihtiyacı olan geniş kapsamlı yazılımların ülke içinde en güvenilir biçimde yapılabilmesi, giderek kritik hâle gelen metro, havaalanı yönetimi, nükleer reaktör yönetimi"""

mystr_ar = "بالطبع أصبحت الهواتف الذكية والتكنولوجيا عمومًا جزء لا يتجزأ من حياة الطالب اليومية على مستوى العالم، وليس في الوطن العربي فقط. لكن مع وجود التسهيلات التكنولوجية تلك، تتغير معها الخبرات المأخوذة من قبل الطلّاب في المدارس. اليوم في أراجيك تعليم سوف نتحدث عن  إيجابيات وسلبيات تواجد الهواتف الذكية في المدارس مع الطلاب داخل الفصول وخارجها، لن نتحدث عن أجهزة الحاسوب المحمولة أو الـ iPad مثلًا، إنها ماكينات إنتاجية في المقام الأول، ومنافعها أكثر من سلبياتها. لكن الهواتف أخف، أسرع، أصغر، وتستطيع صنع الكثير جدًا بمعيار السلبية والإيجابية أكثر من أي جهاز آخر."

mystr_ar2 = "أجل، توجد بالطبع فروض صفيّة يتم عملها بشكل تفاعليّ بين المُعلم والطلبة. وهنا يأتي دور الهواتف الذكية بالتأكيد. هنا يمكن للطالب أن يُخرج لوحة مفاتيح بلوتوث من حقيبته، ويبدأ في الكتابة على الهاتف مباشرة بعد أن يقوم بعمل اقتران بين الهاتف واللوحة."


def seed_users(n):
    fake = Faker()
    for _ in range(n):
        User.objects.create(
            username=fake.user_name(),
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password='MoH.1822'
        )


def seed_brand(n):
    # fake = Faker()

    images = ['01.jpg', '02.jpg', '03.jpg', '04.jpg', '05.jpg',
              '06.jpg', '07.jpg', '08.jpg', '09.jpg', '10.jpg']

    for i in range(n):
        Brand.objects.create(
            name_en=f"Brand Name {i + 1}",
            name_tr=f"Marka Adı {i + 1}",
            name_ar=f"العلامة التجارية {i + 1}",
            image=f"brands/{random.choice(images)}"
        )


def seed_product(n):
    fake = Faker()

    brands = Brand.objects.all()

    images = ['01.jpg', '02.jpg', '03.jpg', '04.jpg', '05.jpg',
              '06.jpg', '07.jpg', '08.jpg', '09.jpg', '10.jpg']
    flag_types = ['New', 'Feature', 'Sale']
    flag = 'New'


    for i in range(n):
        Product.objects.create(
            name_en=fake.name(),
            name_tr=f"Ürün adı {i + 1}",
            name_ar=f"المنتيج رقم {i+1}",
            flag_en=flag,
            flag_tr=flag,
            flag_ar=flag,
            price=round(random.uniform(1.99, 99.99), 2),
            image=f"products/{random.choice(images)}",
            quantity=random.randint(5, 20),
            sku=random.randint(111111, 999999),
            subtitle_en=fake.text(max_nb_chars=200),
            subtitle_tr=mystr_tr2,
            subtitle_ar=mystr_ar2,
            description_en=fake.text(max_nb_chars=2000),
            description_tr=mystr_tr,
            description_ar=mystr_ar,
            brand=random.choice(brands),
        )


def seed_product_images():
    images = ['01.jpg', '02.jpg', '03.jpg', '04.jpg', '05.jpg',
              '06.jpg', '07.jpg', '08.jpg', '09.jpg', '10.jpg']

    products = Product.objects.all()

    for product in products:
        for _ in range(random.randint(1, 5)):
            ProductImages.objects.create(
                product=product,
                image=f"products/{random.choice(images)}"
            )


def seed_review():
    fake = Faker()

    users = User.objects.all()
    products = Product.objects.all()
    review_ar = "ونفس الأمر ينتقل إلى حيّز الطلبة كذلك بين بعضهم البعض، يمكن للطلب أن يصور زميله في أي وضعية غير جيدة، أو بدون علمه أو موافقته، وينشرها على الانترنت ليصير فجأة محل سخرية من الجميع، وفي النهاية تتتشكل في داخله عقد نفسية كثيرة يمكن أن تدمر حياته في المستقبل. "

    review_tr = "Matematik, fen bilimleri ve ilgili mühendislik disiplinine özgü konularda yeterli bilgi birikimi; bu alanlardaki kuramsal ve uygulamalı bilgileri, karmaşık mühendislik problemlerinin çözümünde kullanabilme becerisi."

    for product in products:
        for _ in range(random.randint(1, 5)):
            Review.objects.create(
                user=random.choice(users),
                product=product,
                review_en=fake.text(max_nb_chars=200),
                review_tr=review_tr,
                review_ar=review_ar,
                rate=random.randint(1, 5),
                review_date=fake.date_time()
            )


# seed_users(10)
# seed_brand(50)
# seed_product(50)
# seed_product_images()
# seed_review()
# set_product()
