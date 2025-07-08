# Lawn Irrigation System для Home Assistant

Интеграция для Home Assistant для управления системой автополива газона через HACS.

## Возможности

- 🌱 Управление несколькими зонами полива
- ⏱️ Настраиваемое время полива для каждой зоны
- 🌧️ Проверка погодных условий (опционально)
- 📱 Простая настройка через UI
- 🔄 Автоматическое последовательное выполнение программ полива
- 📊 Мониторинг состояния системы через сенсоры

## Установка

### Через HACS (рекомендуется)

1. Откройте HACS в Home Assistant
1. Перейдите в раздел “Интеграции”
1. Нажмите на три точки в правом верхнем углу
1. Выберите “Пользовательские репозитории”
1. Добавьте URL: `https://github.com/Extreem461/Irri-`
1. Категория: “Integration”
1. Нажмите “Добавить”
1. Найдите “Lawn Irrigation System” и установите
1. Перезагрузите Home Assistant

### Ручная установка

1. Скачайте все файлы из этого репозитория
1. Скопируйте папку `lawn_irrigation` в `custom_components/`
1. Перезагрузите Home Assistant

## Настройка

1. Перейдите в “Настройки” → “Устройства и службы”
1. Нажмите “Добавить интеграцию”
1. Найдите “Lawn Irrigation System”
1. Введите имя системы
1. Добавьте зоны полива:
- Название зоны
- Связанный переключатель (switch entity)
- Время полива по умолчанию
1. Настройте дополнительные параметры (опционально):
- Проверка погодных условий
- Датчик дождя

## Использование

### Сущности

После настройки будут созданы следующие сущности:

**Переключатели (Switch):**

- `switch.lawn_irrigation_system` - Главный переключатель системы
- `switch.lawn_irrigation_zone_*` - Переключатели для каждой зоны

**Сенсоры (Sensor):**

- `sensor.lawn_irrigation_state` - Состояние системы
- `sensor.lawn_irrigation_remaining_time` - Оставшееся время
- `sensor.lawn_irrigation_active_zones` - Количество активных зон

### Сервисы

Интеграция предоставляет следующие сервисы:

#### `lawn_irrigation.start_irrigation`

Запускает полив всех зон последовательно.

```yaml
service: lawn_irrigation.start_irrigation
data:
  duration: 15  # Опционально, в минутах
```

#### `lawn_irrigation.stop_irrigation`

Останавливает весь полив.

```yaml
service: lawn_irrigation.stop_irrigation
```

#### `lawn_irrigation.run_zone`

Запускает конкретную зону.

```yaml
service: lawn_irrigation.run_zone
data:
  zone_id: "Front Lawn"
  duration: 10  # Опционально, в минутах
```

#### `lawn_irrigation.run_program`

Запускает программу полива для выбранных зон.

```yaml
service: lawn_irrigation.run_program
data:
  program_name: "Morning Watering"
  zones:  # Опционально
    - "Front Lawn"
    - "Back Lawn"
```

### Автоматизация

Пример автоматизации для утреннего полива:

```yaml
automation:
  - alias: "Morning Lawn Irrigation"
    trigger:
      platform: time
      at: "06:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.outdoor_humidity
        below: 80
      - condition: state
        entity_id: weather.home
        state: "sunny"
    action:
      - service: lawn_irrigation.start_irrigation
        data:
          duration: 15
```

Пример автоматизации с проверкой дождя:

```yaml
automation:
  - alias: "Stop Irrigation on Rain"
    trigger:
      platform: state
      entity_id: binary_sensor.rain_sensor
      to: "on"
    action:
      - service: lawn_irrigation.stop_irrigation
```

## Требования

- Home Assistant 2024.1.0+
- Настроенные switch entities для каждой зоны полива
- Опционально: датчик дождя для автоматической проверки погоды

## Поддержка

Если у вас возникли проблемы или предложения, пожалуйста, создайте issue в [репозитории GitHub](https://github.com/yourusername/lawn-irrigation-hacs/issues).

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл <LICENSE> для подробностей.

## Changelog

### v1.0.0

- Первый релиз
- Базовая функциональность управления зонами полива
- Поддержка HACS
- Интеграция с Home Assistant UI
