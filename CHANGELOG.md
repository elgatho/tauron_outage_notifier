# Historia zmian

Wszystkie istotne zmiany tej integracji będą udokumentowane w tym pliku.

Format opiera się na [Keep a Changelog](https://keepachangelog.com/pl/)
a ta integracja przestrzega [Semver](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2026-09-20

### Dodano
- Filtrowanie wyłączeń na podstawie kolumny `lokalizacja` — wyłączenia
  z lokalizacją zaczynającą się od "ul." są pomijane
- Pełna zmiana nazwy projektu na **Tauron Outage Notifier**

### Zmieniono
- Nazwa domeny z `tauron_dystrybucja` na `tauron_outage_notifier`
- Dokumentacja i tłumaczenia zaktualizowane do nowej nazwy

## [0.3.0] - 2025-01-01

### Dodano
- Migracja konfiguracji z wersji 1 (proste nazwy) do wersji 2 (GAID)
- Obsługa wielu adresów
- Integracja z kalendarzem Home Assistant
- Encja zdarzenia `new_outage`

### Zmieniono
- Przeniesienie logiki do dedykowanego coordinadora
- Ulepszona obsługa błędów API

## [0.2.0] - 2024-01-01

### Dodano
- Konfiguracja przez flow (city → street → house number)
- Pierwsza wersja integracji
