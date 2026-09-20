# Współtworzenie Tauron Outage Notifier

Dziękujemy za chęć wniesienia wkładu w rozwój tej integracji!

## Zgłaszanie problemów

Jeśli napotykasz błąd, utwórz [issue](https://github.com/Eales/tauron-outage-notifier/issues) z:
- Opis problemu
- Wersja Home Assistant
- Wersja integracji
- Logi błędów (jeśli dostępne)
- Kroki do odtworzenia

## Proponowanie zmian

1. Utwórz [fork](https://github.com/Eales/tauron-outage-notifier/fork) repozytorium
2. Stwórz nową gałąź (`git checkout -b feature/moja-funkcja`)
3. Wprowadź zmiany
4. Uruchom testy (jeśli dostępne)
5. Zatwierdź zmiany (`git commit -m 'Dodaj moją funkcję'`)
6. Wyślij Pull Request

## Standardy kodu

- Używaj Python 3.12+ typizacji (`from __future__ import annotations`)
- Zachowuj spójność z istniejącym stylem kodu
- Dodawaj komentarze docstring do nowych funkcji i klas
- Upewnij się że wszystkie nowe encje mają `_attr_translation_key`
- Zaktualizuj `strings.json` i pliki tłumaczeń przy dodawaniu nowych encji

## Testy

Ta integracja korzysta z Home Assistant test framework. Aby uruchomić testy:

```bash
pip install pytest
pytest tests/ -v
```

## Zasady

- Nie zmieniaj plików konfiguracyjnych użytkowników bez ich zgody
- Nie dodawaj żadnych danych wrażliwych do repozytorium
- Utrzymuj kompatybilność wsteczną gdzie to możliwe
