# Not Paylaşma Sitesi API

Bu proje, Flask, Flask-SQLAlchemy, Flask-RESTful ve Flask-JWT-Extended kullanılarak geliştirilen bir not paylaşma sitesi API'sini içermektedir. API, kullanıcıların hesap oluşturmasını, birbirlerini arkadaş olarak eklemesini, birbirlerini engellemesini ve not paylaşmasını sağlamaktadır. Notlar sadece metin formatında paylaşılabilir. Bu projede iki adet veri tabanı vardır: ilki sadece giriş bilgilerini tutar, ikincisi geriye kalan tüm bilgileri tutar. Authentification için JSON Web Token'ları kullanılır.

## Dosyalar

- `__init__.py`: Klasörün Python paketi olmasını ve dosyaların birbirini görmesini sağlar.
- `config.ini`: Konfigürasyonların tutulduğu dosya.
- `instance/credentials.db`: Kullanıcı e-posta ve hash'lenmiş şifrelerin tutulduğu veri tabanı.
- `instance/database.db`: Geri kalan tüm verilerin tutulduğu veri tabanı.
- `main.py`: Ana programın bulunduğu dosyadır. Sunucuyu çalıştırmak için bu dosya başlatılmalıdır.
- `models.py`: Veri tabanlarında kullanılacak MVC'ler burada tanımlandı.
- `README.md`: Projeyi tanımlayan bu dosya.
- `requirements.txt`: Projede kullanılan tüm kütüphanelerin olduğu dosya.
- `test.py`: Minik test scriptlerinin bulunduğu dosya.
- `views.py`: API Endpoint'leri bu klasörde tanımlandı.

## API Endpoint'leri

### Kullanıcı İşlemleri

- `POST /user/register`: Yeni bir kullanıcı hesabı oluşturur.

- `POST /user/login`: Kullanıcı girişi yapar ve bir JWT (JSON Web Token) döndürür.

- `POST /user/edit`: Kullanıcı bilgilerini günceller.

- `POST /user/delete`: Kullanıcı hesabını siler.

- `GET /user/view_profile`: Kullanıcının profil bilgilerini görüntüler.

- `POST /user/logout`: Kullanıcıyı oturumdan çıkarır ve JWT'yi geçersiz kılar.

### Engelleme İşlemleri

- `GET /block/block`: Bir kullanıcıyı engeller.

- `GET /block/unblock`: Engellenmiş bir kullanıcıyı engellemeyi kaldırır.

### Arkadaşlık İşlemleri

- `GET /friendship/request`: Bir kullanıcıya arkadaşlık isteği gönderir.

- `GET /friendship/unrequest`: Gönderilmiş bir arkadaşlık isteğini geri çeker.

- `GET /friendship/accept`: Bir arkadaşlık isteğini kabul eder.

- `GET /friendship/deny`: Bir arkadaşlık isteğini reddeder.

- `GET /friendship/unfriend`: Bir kullanıcıyı arkadaş listesinden çıkarır.

### Not İşlemleri

- `GET /post/create`: Bir not oluşturur.

- `GET /post/update`: Bir notu günceller.

- `GET /post/delete`: Bir notu siler.

- `GET /post/view`: Bir notu görüntüler.

## Kullanım

Aşağıda, API endpoint'lerinin kullanımına dair örnek isteklerin ve yanıtların bulunduğu birkaç senaryo verilmiştir:

# Yeni Kullanıcı Hesabı Oluşturma
POST /user/register
Content-Type: application/json

{
  "email": "example@example.com",
  "user_name": "John Doe",
  "password1": "password123",
  "password2": "password123"
}

# Kullanıcı Girişi
POST /user/login
Content-Type: application/json

{
  "email": "example@example.com",
  "password": "password123"
}

# Kullanıcı Bilgilerini Güncelleme
POST /user/edit
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "user_name": "John Doe",
  "email": "example@example.com",
  "country": "Turkey"
}

# Kullanıcı Hesabını Silme
POST /user/delete
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "email": "example@example.com",
  "password1": "password123"
  "password2": "password123"
}

# Kullanıcı Profilini Görüntüleme
GET /user/view_profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "user_name": "John Doe"
}

# Kullanıcı Oturumdan Çıkma
POST /user/logout
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Kullanıcıyı Engelleme
POST /block/block
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "user_name": "John Doe"
}

# Engeli Kaldırma
POST /block/unblock
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "user_name": "John Doe"
}

# Arkadaşlık İsteği Gönderme
POST /friendship/request
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "user_name": "John Doe"
}

# Arkadaşlık İsteğini İptal Etme
POST /friendship/unrequest
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "user_name": "John Doe"
}

# Arkadaşlık İsteğini Kabul Etme
POST /friendship/accept
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "user_name": "John Doe"
}

# Arkadaşlık İsteğini Reddetme
POST /friendship/deny
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "user_name": "John Doe"
}

# Arkadaşlıktan Çıkma
POST /friendship/unfriend
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "user_name": "John Doe"
}

# Not Oluşturma
POST /post/create
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "text": "Bu bir nottur."
}

# Notu Güncelleme
PUT /post/update
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
 
{
  "post_id": 123,
  "text": "Not güncellendi."
}

# Notu Silme
DELETE /post/delete
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "post_id": 123
}

# Notu Görüntüleme
GET /post/view?post_id=123
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "post_id": 123
}
