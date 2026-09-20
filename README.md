# Tauron Outage Notifier

[![HACS](https://img.shields.io/badge/HACS-Custom-orange)](https://hacs.xyz/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.11.0+-blue)](https://www.home-assistant.io/)

Integracja dla Home Assistant, która informuje o planowanych i nieprzewidzianych
wyłączeniach prądu dla podanego adresu, korzystając z publicznego API Tauron Dystrybucja (Polska).

Wyłączenia są prezentowane jako kalendarz, jako zdarzenie pojawiające się w momencie
ogłoszenia nowego wyłączenia oraz jako proste sensory — dzięki czemu możesz budować
własne powiadomienia bez pisania szablonów.

**Wymaga Home Assistant 2024.11.0 lub nowszego.**

## Instalacja

### HACS (zalecane)

1. HACS → **Integracje** → menu (⋮) → **Repozytoria niestandardowe**
2. URL: `https://github.com/Eales/tauron-outage-notifier`, kategoria: **Integracja**
3. Zainstaluj **Tauron Outage Notifier**, a następnie zrestartuj Home Assistant

### Ręcznie

Skopiuj folder `custom_components/tauron_outage_notifier` do katalogu `config`
Home Assistanta i zrestartuj.

## Konfiguracja

1. `Ustawienia` → `Urządzenia i usługi` → `Dodaj integrację`
2. Wyszukaj `Tauron Outage Notifier`
3. Wpisz co najmniej 3 znaki nazwy miejscowości, a następnie wybierz swoją miejscowość
4. Wpisz co najmniej 3 znaki nazwy ulicy, a następnie wybierz swoją ulicę
5. Wpisz numer domu

Dodaj integrację wielokrotnie, aby monitorować wiele adresów.

API Tauronu wymaga podania ulicy, dlatego adresy w miejscowościach bez nazwanych
ulic nie mogą być skonfigurowane.

## Interwał odpytywania

API jest odpytywane co **60 minut** domyślnie; możesz zmienić to przyciskiem
`Konfiguruj` integracji (15–1440 minut).

Tauron ogłasza planowane wyłączenia z kilkudniowym wyprzedzeniem, więc częste
odpytywanie nie przynosi większych korzyści. Jeden adres przy domyślnym interwale
to około 24 żądań dziennie.

## Encje

Każdy adres tworzy jedno urządzenie. Każdy aspekt *aktualnego* wyłączenia —
tego trwającego lub następnego gdy nic nie działa — jest oddzielną encją.

| Encja | Typ | Opis |
| --- | --- | --- |
| `Status` | sensor (enum) | `Brak wyłączeń` / `Wyłączenie ogłoszone` / `Wyłączenie w trakcie` |
| `Początek wyłączenia` | sensor (timestamp) | Kiedy zaczyna się |
| `Koniec wyłączenia` | sensor (timestamp) | Kiedy kończy się |
| `Czas trwania` | sensor (duration) | Jak długo trwa (w godzinach) |
| `Opis wyłączenia` | sensor | To co Tauron opublikował |
| `Zapowiedziane wyłączenia` | sensor | Ile wyłączeń mieści się w kolejnych 30 dniach |
| `Wyłączenia prądu` | kalendarz | Każde wyłączenie jako zdarzenie kalendarza |
| `Nowe wyłączenie` | zdarzenie | Występuje gdy Tauron ogłosi nowe wyłączenie |
| `Wyłączenie w trakcie` | binary_sensor | `on` gdy wyłączenie jest aktywne |

## Dlaczego zapytania na poziomie adresu?

Ta integracja zapytuje API Tauronu po **GAID miasta + GAID ulicy + numerze domu**,
a nie po dzielnicy lub gminie. Oznacza to, że powiadomienia są precyzyjne
do Twojej ulicy — np. "Podłęże 632" — zamiast działać dla całego miasta.

## Automatyzacje

Integracja nigdy nie powiadamia samodzielnie — jedynie eksponuje encje.

### Powiadomienie gdy ogłoszono nowe wyłączenie

```yaml
automation:
  - alias: "Tauron - nowe wyłączenie"
    triggers:
      - trigger: state
        entity_id: event.<entity_id>_new_outage
    conditions:
      - condition: template
        value_template: "{{ trigger.to_state.state not in ['unknown', 'unavailable'] }}"
    actions:
      - action: notify.persistent_notification
        data:
          title: "Uwaga - planowane wyłączenie prądu"
          message: >-
            {{ trigger.to_state.attributes.start | as_datetime | as_local
               | as_timestamp | timestamp_custom('%d.%m %H:%M') }}
            - {{ trigger.to_state.attributes.end | as_datetime | as_local
               | as_timestamp | timestamp_custom('%H:%M') }}
            {{ trigger.to_state.attributes.description }}
```

### Przypomnienie przed rozpoczęciem wyłączenia

```yaml
automation:
  - alias: "Tauron - wkrótce wyłączenie"
    triggers:
      - trigger: calendar
        entity_id: calendar.<entity_id>_outages
        event: start
        offset: "-02:00:00"
    actions:
      - action: notify.persistent_notification
        data:
          title: "Wkrótce nie będzie prądu"
          message: "{{ trigger.calendar_event.description }}"
```

## Licencja

MIT
