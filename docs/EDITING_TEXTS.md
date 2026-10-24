# Jak zmieniać teksty strony

1. Otwórz [edycję template.html na GitHubie](https://github.com/marsellewoczko/worlds-2026-calendar/edit/main/template.html).
2. Wyszukaj `const strings`. Sekcja `en` zawiera angielskie teksty, a `pl` polskie. Każdy tekst ma teraz osobną linię.
3. Zmień treść pomiędzy apostrofami przy właściwym kluczu. Zachowaj nazwy kluczy, przecinki, nawiasy i apostrofy ograniczające tekst. Apostrof wewnątrz tekstu zapisz jako `\'` (np. `don\'t`); nie dodawaj surowych nowych linii w środku napisu.
4. Zmień obie wersje językowe. Kliknij **Commit changes**, wpisz opis i zapisz na `main` (albo użyj PR, jeśli tak wymaga repozytorium).
5. Otwórz **Actions → Sync and publish Worlds 2026 calendar**. Zmiana template.html automatycznie uruchamia publikację. Po sukcesie odśwież stronę i sprawdź PL oraz EN. Twarde odświeżenie może pomóc, jeśli przeglądarka pokazuje poprzednią wersję.

| Klucz | Tekst na stronie |
| --- | --- |
| `headline` | Główny nagłówek; `<br>` łamie linię, `<em>…</em>` wyróżnia tekst |
| `lead` | Opis pod głównym nagłówkiem |
| `eyebrow` | Mały napis nad sekcją subskrypcji |
| `subscribeTitle` | Nagłówek subskrypcji |
| `apple` | Przycisk Apple Calendar / Outlook |
| `copy` | Przycisk kopiowania linku |
| `guide` | Instrukcja dodania kalendarza |
| `matchesLabel`, `timezoneLabel` | Etykiety liczby meczów i strefy czasowej |
| `scheduleLabel`, `scheduleTitle` | Nagłówki sekcji terminarza |
| `credit`, `portfolio` | Podpis autora i tekst o pozostałych projektach |
| `disclaimer` | Informacja o niezależnym projekcie fanowskim i źródle |
| `updated` | Etykieta ostatniej aktualizacji; zachowaj `%%UPDATED%%` |

Większość tych napisów występuje również jako domyślny angielski tekst w HTML nad skryptem. Interaktywna strona korzysta z `strings`; dla spójności domyślnego HTML warto zmienić też jego angielską kopię przy odpowiednim `id` (np. `id="lead"`).

Tytuł karty przeglądarki zmienisz na początku pliku w `<title>`. Opisy dla wyszukiwarek i podglądów linków są w `meta name="description"`, `og:title` i `og:description`. Link autora i link źródła są w `<footer>`.

Teksty statusów meczów (`Zakończony`, `Na żywo` itd.) są w obiekcie `states` wewnątrz funkcji `render`. Komunikaty po skopiowaniu linku i awaryjne okno kopiowania są w obsłudze przycisku `copy` nad `strings`.

Nie edytuj generowanego `site/index.html` — kolejne wdrożenie go zastąpi. Nazwy drużyn, daty i wyniki pochodzą z API. Notatki kalendarza ICS są generowane osobno w funkcji `make_ics` w `sync.py`; nie zmieniają się przez edycję `strings`.

Sekcja „Co zobaczysz w swoim kalendarzu?” korzysta z kluczy `insideTitle`, `insideGuide`, `spoilerNotice`, `exampleLabel`, `exampleOpen`, `exampleDetails` i `refreshNotice` w obu wersjach `strings`. Przykład musi pozostać wyraźnie oznaczony jako poglądowy.

Zrzut kalendarza znajduje się w `assets/calendar-example.jpg`; generator kopiuje go do publikowanej strony. `exampleImage` zmienia opis alternatywny, a `exampleOpen` podpis rozwijanego podglądu.
