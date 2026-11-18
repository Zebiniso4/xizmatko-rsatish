# Avtomobil ta'mirlash xizmati boshqaruv tizimi — Texnik topshiriq

Ushbu hujjat avtomobillar, mijozlar, ta'mirlash ishlari, ehtiyot qismlar va to'lovlarni yagona tizimda boshqarish dasturini ishlab chiqish talablarini belgilaydi.

## 1. Umumiy ma'lumotlar

- **Tizim nomi:** Avtomobil ta'mirlash xizmati boshqaruv tizimi (AvtoServis).
- **Maqsad:** avtoservis faoliyatini avtomatlashtirish: mijoz va avtomobillar bazasini yuritish, ta'mirlash buyurtmalarini kuzatish, ehtiyot qismlar omborini nazorat qilish va to'lovlarni hisobga olish.
- **Qamrov:** bitta avtoservis (kelajakda bir nechta filialga kengaytirish imkoniyati bilan).
- **Hal qilinadigan muammolar:** qog'ozdagi hisobning yo'qolishi, ehtiyot qismlar qoldig'ining noaniqligi, qarzdorlikni nazorat qilishdagi qiyinchiliklar, hisobot tayyorlashga ketadigan vaqt.
- **Maqsadli foydalanuvchilar:** avtoservis egasi, administrator, usta-mexaniklar, omborchi va kassir.

## 2. Foydalanuvchi rollari

| Rol | Asosiy huquqlari |
| --- | --- |
| Administrator (egasi) | Barcha modullarga kirish, foydalanuvchilarni boshqarish, hisobotlarni ko'rish, narxlarni belgilash |
| Qabul qiluvchi (menejer) | Mijoz va avtomobil qo'shish, buyurtma ochish, ustaga biriktirish, buyurtma holatini kuzatish |
| Usta-mexanik | O'ziga biriktirilgan buyurtmalarni ko'rish, bajarilgan ishlar va ishlatilgan qismlarni kiritish, holatni o'zgartirish |
| Omborchi | Ehtiyot qismlarni qabul qilish, chiqarish, qoldiqni nazorat qilish, inventarizatsiya |
| Kassir | To'lovlarni qabul qilish, chek va kvitansiya chiqarish, qarzdorlikni ko'rish |

## 3. Funksional talablar

### 3.1. Avtomobillar moduli

- Avtomobil qo'shish, tahrirlash, o'chirish (arxivlash): davlat raqami, VIN-kod, marka, model, ishlab chiqarilgan yil, rangi, dvigatel turi, probeg.
- Avtomobilni mijozga biriktirish; bitta mijozda bir nechta avtomobil bo'lishi mumkin.
- Avtomobilning to'liq ta'mirlash tarixini ko'rish (sana, ishlar, qismlar, summa).
- Davlat raqami yoki VIN bo'yicha tezkor qidiruv.
- Navbatdagi texnik ko'rik va moy almashtirish muddatini eslatish.

### 3.2. Mijozlar moduli

- Mijoz kartasi: F.I.O., telefon, manzil, izoh, ro'yxatdan o'tgan sana.
- Mijozning avtomobillari, buyurtmalari va to'lovlari tarixi.
- Qarzdorlik holati va umumiy xarid summasi.
- Doimiy mijozlar uchun chegirma belgilash imkoniyati.

### 3.3. Ta'mirlash ishlari moduli

- Buyurtma (ta'mirlash varaqasi) ochish: mijoz, avtomobil, kelgan sana, probeg, mijoz bildirgan nosozlik.
- Xizmatlar ro'yxatidan (ish turlari) tanlash; har bir xizmatning narxi va bajarilish normasi (soat).
- Ustani biriktirish va bir buyurtmaga bir nechta usta qo'shish.
- Buyurtma holatlari: *Yangi*, *Diagnostika*, *Tasdiqlash kutilmoqda*, *Jarayonda*, *Ehtiyot qism kutilmoqda*, *Tayyor*, *Topshirildi*, *Bekor qilindi*.
- Buyurtmaga ishlatilgan ehtiyot qismlarni qo'shish; qism qo'shilganda ombor qoldig'i avtomatik kamayadi.
- Buyurtma yakuniy summasini avtomatik hisoblash (ishlar + qismlar − chegirma).
- Buyurtma bo'yicha dalolatnoma (akt) va hisob-fakturani PDF ko'rinishida chiqarish.

### 3.4. Ehtiyot qismlar moduli

- Qismlar katalogi: nomi, artikul (kod), ishlab chiqaruvchi, mos keladigan marka/modellar, o'lchov birligi.
- Kirim (yetkazib beruvchidan qabul qilish) va chiqim (buyurtmaga sarflash, sotish) operatsiyalari.
- Sotib olish va sotish narxi, ustama foizi.
- Joriy qoldiqni ko'rish va minimal qoldiq belgilash; minimumdan kam qolganda ogohlantirish.
- Yetkazib beruvchilar ro'yxati va ular bilan hisob-kitob.
- Inventarizatsiya: haqiqiy va tizimdagi qoldiqni solishtirish.

### 3.5. To'lovlar moduli

- To'lov qabul qilish usullari: naqd, plastik karta, pul o'tkazmasi.
- Bitta buyurtma bo'yicha avans va qisman to'lovlar (bo'lib to'lash).
- Qarzdorlikni avtomatik hisoblash va qarzdor mijozlar ro'yxati.
- Kvitansiya (chek) chiqarish va to'lovlar jurnali.
- Kunlik kassa hisoboti (kirim, chiqim, qoldiq).

### 3.6. Hisobotlar moduli

- Davr bo'yicha daromad va xarajat hisoboti (kun, hafta, oy).
- Ustalar bo'yicha bajarilgan ishlar va ish haqi hisobi.
- Eng ko'p ishlatiladigan xizmatlar va ehtiyot qismlar.
- Ombor qoldig'i va qarzdorlar hisoboti.
- Hisobotlarni Excel va PDF formatiga eksport qilish.

## 4. Ma'lumotlar bazasi

Asosiy jadvallar (yoki kolleksiyalar) va ular orasidagi bog'lanishlar:

| Jadval | Asosiy maydonlar | Bog'lanish |
| --- | --- | --- |
| clients | id, full_name, phone, address, discount, created_at | 1 mijoz — ko'p avtomobil |
| cars | id, client_id, plate_number, vin, brand, model, year, color, mileage | clients ga tegishli |
| services | id, name, price, norm_hours | orders_services orqali buyurtmalarga bog'lanadi |
| workers | id, full_name, phone, position, salary_percent | ustalar |
| orders | id, car_id, client_id, status, complaint, mileage, opened_at, closed_at, total, discount | cars va clients ga tegishli |
| orders_services | order_id, service_id, worker_id, quantity, price | orders ↔ services ↔ workers |
| parts | id, name, article, manufacturer, unit, buy_price, sell_price, stock, min_stock | ombor qoldig'i |
| orders_parts | order_id, part_id, quantity, price | orders ↔ parts |
| suppliers | id, name, phone, address | yetkazib beruvchilar |
| stock_moves | id, part_id, supplier_id, type (kirim/chiqim), quantity, price, date | parts ga tegishli |
| payments | id, order_id, amount, method, paid_at, cashier_id | orders ga tegishli |
| users | id, login, password_hash, role, is_active | tizimga kirish |

Talablar: har bir jadvalda yaratilgan va o'zgartirilgan vaqt saqlanadi; o'chirish "yumshoq" (arxivlash) tarzida amalga oshiriladi; telefon va davlat raqami maydonlari noyob bo'lishi kerak.

## 5. Nofunksional talablar

- **Xavfsizlik:** login va parol bilan kirish, parollar xesh ko'rinishida saqlanadi, rollar bo'yicha kirish huquqlari, barcha muhim amallar (o'chirish, narx o'zgartirish) jurnalga yoziladi.
- **Tezlik:** oddiy so'rovlarga javob 2 soniyadan oshmasligi, hisobotlar 10 soniya ichida shakllanishi kerak.
- **Ishonchlilik:** ma'lumotlar bazasining har kunlik avtomatik zaxira nusxasi; ma'lumotlarni tiklash imkoniyati.
- **Hajm:** kamida 10 000 mijoz va 50 000 buyurtmani sekinlashmasdan saqlashi kerak.
- **Qulaylik:** interfeys o'zbek tilida (kirill va lotin, keyinchalik rus tili qo'shish imkoniyati), yangi xodim 1 soat ichida o'rganishi mumkin bo'lishi kerak.
- **Moslik:** zamonaviy brauzerlar (Chrome, Firefox, Edge) va mobil qurilmalarda to'g'ri ishlashi.

## 6. Texnologiyalar va interfeys

| Qatlam | Tavsiya etilgan variant |
| --- | --- |
| Dasturlash tili (backend) | Python (FastAPI yoki Django) |
| Ma'lumotlar bazasi | MongoDB yoki PostgreSQL |
| Frontend | HTML/CSS/JavaScript (yoki React) |
| Hisobotlar | PDF va Excel (openpyxl, ReportLab) |
| Joylashtirish | Linux server, Docker |

**Interfeys talablari:**

- Asosiy oyna: bugungi buyurtmalar, qarzdorlar, minimal qoldiqdagi qismlar haqida qisqa ko'rsatkichlar.
- Chap tomonda modullar menyusi: Buyurtmalar, Mijozlar, Avtomobillar, Ombor, To'lovlar, Hisobotlar, Sozlamalar.
- Har bir ro'yxatda qidiruv, filtr va saralash bo'lishi shart.
- Buyurtma sahifasida holatlar rang bilan ajratib ko'rsatiladi.
- Formalar xato kiritilganda aniq izoh beradi.

## 7. Ish bosqichlari va muddatlar

| Bosqich | Mazmuni | Muddat |
| --- | --- | --- |
| 1. Tahlil | Talablarni aniqlash, texnik topshiriqni tasdiqlash | 1 hafta |
| 2. Loyihalash | Ma'lumotlar bazasi sxemasi, interfeys maketlari | 1 hafta |
| 3. Ishlab chiqish | Modullarni yozish: mijozlar, avtomobillar, buyurtmalar, ombor, to'lovlar, hisobotlar | 4 hafta |
| 4. Sinov | Funksional va xavfsizlik sinovlari, xatolarni tuzatish | 1 hafta |
| 5. Joriy etish | Serverga o'rnatish, ma'lumotlarni ko'chirish, xodimlarni o'rgatish | 1 hafta |

Umumiy muddat: taxminan 8 hafta.

## 8. Qabul qilish mezonlari

- Barcha 3-bo'limdagi funksiyalar xatosiz ishlaydi.
- Buyurtma yaratilganda ombor qoldig'i to'g'ri kamayadi va yakuniy summa to'g'ri hisoblanadi.
- Qisman to'lov qilinganda qarzdorlik to'g'ri ko'rsatiladi.
- Hisobotlar Excel va PDF formatida yuklab olinadi, ma'lumotlari bazadagi yozuvlarga mos keladi.
- Rollar bo'yicha kirish cheklovlari ishlaydi: usta kassa va hisobotlarni ko'ra olmaydi.
- Dastur sinov ma'lumotlari (kamida 50 mijoz, 100 buyurtma) bilan belgilangan tezlikda ishlaydi.
- Foydalanuvchi qo'llanmasi va ma'lumotlar bazasi tavsifi topshiriladi.
