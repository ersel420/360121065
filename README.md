
# 360121065 - E-Commerce Website Demo with Django

A simple e-commerce website demo made with Django. It was made as a project of the BLY2005 course from Marmara University Computer Programming.

## :star: Start
### :star: Instructions
1. Download repository.
2. Extract in a folder.
3. Open folder with Visual Studio Code.

### :star: Commands

```bash
py manage.py runserver
```

### :star: Admin
1. **Admin Pag:**  &rarr; http://127.0.0.1:8000/admin
2. **✉️**  &rarr; user@admin.com
3. **🔑**  &rarr; admin

## :star: Accounts

|E-Mail Adress|Password|Account Type|
| ------------ | ------------ | ------------ |
|user@admin.com|admin|Superuser|
|user@test.com|test|Normaluser|
|a@a.com|ezekielartiff|Normaluser|
|d@d.com|123|Normaluser|

## :star: Apps
- **mytemplate**  &rarr; Core.
- **website**  &rarr; Homepage, information, services etc...
- **cart**  &rarr; Cart management.
- **account**  &rarr; User management operations such as registration, login, profile, dashboard etc..
- **payment**  &rarr; Payment and order management.

## :star: Packages
- **[Pillow](https://github.com/python-pillow/Pillow "Pillow")**  &rarr; Used for image management.
```bash
pip install Pillow
```
- **[Six](https://github.com/benjaminp/six "Six")**  &rarr; Used in token creation.
```bash
pip install six
```
- **[Iyzipay](https://github.com/iyzico/iyzipay-python "Iyzipay")**  &rarr; Used for payment management.
```bash
pip install iyzipay
```
## :star: Cards for Payment

Click [here](https://github.com/iyzico/iyzipay-python/blob/master/README.md#mock-test-cards "here") for original.

### :star: Normal Cards
Card Number| Bank| Card Type
-----------| ----| ---------
5526080000000006 | Akbank| Master Card
4603450000000000 | Denizbank| Visa
4729150000000005 | Denizbank Bonus| Visa
5311570000000005 | Finansbank| Master Card
9792030000000000 | Finansbank| Troy
5400360000000003 | Garanti Bankası| Master Card
374427000000003  | Garanti Bankası| American Express
5528790000000008 | Halkbank| Master Card
5504720000000003 | HSBC Bank| Master Card
4543590000000006 | Türkiye İş Bankası| Visa
4157920000000002 | Vakıfbank| Visa
5451030000000000 | Yapı ve Kredi Bankası| Master Card

### :star: Cross Border Test Cards

Card Number      | Country
-----------| -------
5400010000000004 | Non-Turkish

### :star: Error Test Cards

Card Number| Description
-----------| -----------
5406670000000009  | Success but cannot be cancelled, refund or post auth
4111111111111129  | Not sufficient funds
4129111111111111  | Do not honour
4128111111111112  | Invalid transaction
4127111111111113  | Lost card
4126111111111114  | Stolen card
4125111111111115  | Expired card
4124111111111116  | Invalid cvc2
4123111111111117  | Not permitted to card holder
4122111111111118  | Not permitted to terminal
4121111111111119  | Fraud suspect
4120111111111110  | Pickup card
4130111111111118  | General error
4131111111111117  | Success but mdStatus is 0
4141111111111115  | Success but mdStatus is 4
4151111111111112  | 3dsecure initialize failed

## :star: Database
### :star: Website App Models

```python
class Category(models.Model):
    name = models.CharField(max_length = 100, db_index = True)
    slug = models.SlugField(max_length = 105, unique = True)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('website:categoryFilter', args = [self.slug])

    def __str__(self):
        return self.name
    
class Service(models.Model):
    category =  models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    image = models.ImageField(upload_to = 'static/website/img/')
    bigImage = models.ImageField(upload_to = 'static/website/img/')
    slug = models.SlugField(max_length = 105, unique = True)
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    is_active = models.BooleanField(default = True)

    class Meta:
        verbose_name_plural = 'Services'

    def get_absolute_url(self):
        return reverse('website:serviceDetail', args = [self.slug])

    def __str__(self):
        return self.name

    @property
    def cName(self):
        return self.category.name
```
### :star: Cart App Models

```python
class CartItem(models.Model):
    user = models.ForeignKey(UserBase, on_delete = models.CASCADE)
    item =  models.ForeignKey(Service, on_delete = models.CASCADE)
    itemQty = models.IntegerField()

    class Meta:
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return str(self.user)

    @property
    def sCategory(self):
        return self.item.cName

    @property
    def sDescription(self):
        return self.item.description

    @property
    def sImageUrl(self):
        return self.item.image.url

    @property
    def sName(self):
        return self.item.name

    @property
    def sID(self):
        return self.item.id

    @property
    def sPrice(self):
        return self.item.price

    @property
    def sUrl(self):
        return self.item.get_absolute_url
```

### :star: Account App Models

```python
class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff = True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser = True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email = email, user_name = user_name,**other_fields)
        user.set_password(password)
        user.save()
        return user

class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique = True)
    user_name = models.CharField(max_length = 50, unique = True)
    firstName = models.CharField(max_length = 50)
    lastName = models.CharField(max_length = 50)
    phoneNumber = models.CharField(max_length = 11, unique = True)
    address = models.TextField(max_length = 500, blank = True)
    is_active = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add = True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"
    
    def __str__(self):
        return self.user_name

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently = False,
        )
```

### :star: Payment App Models

```python
class Order(models.Model):
    user = models.ForeignKey(UserBase, on_delete = models.CASCADE)
    totalPaid = models.DecimalField(max_digits = 15, decimal_places = 2)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = 'Orders'
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)

    @property
    def uID(self):
        return self.user.id

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    price = models.DecimalField(max_digits = 7, decimal_places = 2, default = 1)
    qty = models.PositiveIntegerField(default = 1)

    class Meta:
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return str(self.order.id)

    def total(self):
        return self.price * self.qty

    @property
    def sName(self):
        return self.service.name

    @property
    def sPrice(self):
        return self.service.price

    @property
    def sUrl(self):
        return self.service.get_absolute_url
```

### :star: Database Diagram
![Database Diagram](https://i.hizliresim.com/3vkbwow.png)

## :star: Template
Click [here](https://templatemo.com/tm-526-vanilla "here") for original template. **(Templatemo 526 Vanilla)**
