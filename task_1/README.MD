## 1. Проектирование базы данных

## Вариант 1: Одна общая таблица для пациентов и сотрудников

### Структура:

1. ID (уникальный идентификатор)
2. ФИО
3. Дата рождения
4. Телефон
5. Номер медкарты (NULL для сотрудников)
6. ИНН (NULL для пациентов)
7. Роль (Пациент/Сотрудник/Оба)

### Плюсы:

1. Простая структура, все данные хранятся в одной таблице.
2. Легко добавлять новых людей, независимо от роли.
3. Удобно, если человек имеет обе роли (пациент и сотрудник), все данные в одном месте.

### Минусы:

1. Наличие NULL-значений в некоторых полях (медкарта у сотрудников, ИНН у пациентов).
2. Сложнее поддерживать целостность данных, если таблица сильно вырастет.
3. Меньше гибкости в расширении, если нужно будет добавить специфические атрибуты для одной из ролей.

###  Удобство использования:

- Простое для понимания, но может быть труднее поддерживать, если структура будет расти.

### Расширяемость:

- Необходимо будет добавлять поля для новых атрибутов, что может усложнить дизайн.

### Целостность данных:

- Целостность данных будет поддерживаться проще за счет одной таблицы, но возможны ошибки из-за пустых полей.

### Производительность:

- Производительность может пострадать при большом объеме данных, так как придется работать с большим количеством NULL-значений.

## Вариант 2: Раздельные таблицы для пациентов и сотрудников + таблица связей

## Структура:

1. Таблица "Люди":
- ID
- ФИО
- Дата рождения
- Телефон

2. Таблица "Пациенты":
- ID (ссылка на таблицу "Люди")
- Номер медкарты

3. Таблица "Сотрудники":
- ID (ссылка на таблицу "Люди")
- ИНН

4. Таблица связей "Роли":
- ID_Человека
- Роль (Пациент/Сотрудник)

### Плюсы:

1. Гибкость в добавлении новых атрибутов и ролей.
2. Чистые данные: нет NULL-значений в полях, где они не нужны.
3. Легче поддерживать данные, если человек имеет обе роли.

### Минусы:

1. Усложняется структура базы данных, нужно делать большее количество JOIN-запросов.
2. Для простых операций требуется больше SQL-запросов, что может снизить производительность.

### Удобство использования:

- Менее удобно для простых операций, требует объединения нескольких таблиц.

### Расширяемость:

- Легко добавлять новые атрибуты и роли.

### Целостность данных:

- Высокий уровень целостности данных за счет раздельного хранения информации по ролям.

### Производительность:

- Сложные JOIN-запросы могут снижать производительность при большом объеме данных, однако это компенсируется более компактной структурой данных.