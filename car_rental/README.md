# Avtomobil ijarasi axborot tizimi

Avtomobillar, mijozlar, ijara, ta'mirlash, ehtiyot qismlar va to'lovlarni
boshqaruvchi konsol dasturi (Python 3 + MongoDB).

## Maqsad

Avtomobil ijarasi hisobini bitta tizimda yuritish. Batafsil:
[loyiha xartiyasi](../docs/project-charter.md).

## O'rnatish va ishga tushirish

MongoDB ishlab turishi kerak.

```bash
cd car_rental
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Boshqa server uchun `MONGO_URI` muhit o'zgaruvchisini bering.

## Foydalanish

Parol bilan himoyalash uchun `ADMIN_PASSWORD` muhit o'zgaruvchisini bering.

Avval menyudan avtomobil va mijoz qo'shing, keyin ijara oching. Mashina
qaytganda ijarani yoping, to'lovni kiriting va hisobotlarni ko'ring.

## Jamoa

Matrasulova Zebiniso — loyiha rahbari va dasturchi.

## Tuzilma

| Joy | Vazifasi |
| --- | --- |
| `main.py` | konsol menyusi |
| `db.py` | ulanish va indekslar |
| `models/` | avtomobillar, mijozlar |
| `services/` | ijara, ta'mir, ombor, to'lov |
| `reports.py` | hisobotlar |
| `tests/` | biznes mantiq testlari |

Kolleksiyalar: `cars`, `customers`, `rentals`, `repairs`, `parts`, `payments`.
Ombor kirim-chiqimi `parts.movements` ichida saqlanadi.

## Testlar

```bash
pip install pytest
python -m pytest
```

Testlar xotiradagi soxta baza bilan ishlaydi, haqiqiy MongoDB talab qilmaydi.

## Cheklovlar

- Bir necha bosqichli amallar tranzaksiyasiz bajariladi.
- Foydalanuvchi rollari va parol yo'q.
- Oylik xarajatga faqat ehtiyot qism xaridlari kiradi.
