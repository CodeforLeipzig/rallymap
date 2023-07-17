# RallyMap

[![license](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![readme style](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg)](https://github.com/RichardLitt/standard-readme)
[![make help](https://img.shields.io/badge/make-help-brightgreen.svg)](https://gitlab.com/depressiveRobot/make-help)

Demonstrator zur Visualisierung von angemeldeten Versammlungen in Leipzig.

![Screenshot RallyMap](./docs/Screenshot%202023-06-11%20at%2016.33.34.png)

Das Projekt stellt das Versammlungsgeschehen in Leipzig auf einer interaktiven Karte dar. Dabei werden die Orte und Straßen, auf den Versammlungen stattfinden, farblich markiert. Mit einem Klick auf eine Markierung werden Informationen wie etwa Thema/Motto, Art, Datum und Zeitraum der Versammlung angezeigt.

Mit dem Projekt soll das Potential von [Open Data](https://de.wikipedia.org/wiki/Open_Data) (offenen Daten) aufgezeigt werden.

Die Idee wurde zum [Leipzig Open Data Hackathon 2023](https://www.leipzig.de/buergerservice-und-verwaltung/unsere-stadt/statistik-und-zahlen/open-data/hackathon-2023) im Rahmen der [Data Week Leipzig 2023](https://2023.dataweek.de/) eingereicht und hat den 2. Platz in der Kategorie "Offenes Thema" erreicht.

## Installation

Für die Installation und Ausfürhung wird [Docker](https://www.docker.com/) benötigt.

Mit `make build` wird das benötigte Python-Image gebaut.

## Nutzung

Für das Berechnen der Routen wird der Dienst [openrouteservice](https://openrouteservice.org/) verwendet. Um den Dienst zu nutzen, wird ein API-Key benötigt, für den wiederum eine [kostenlose Registrierung](https://openrouteservice.org/dev/#/login) notwendig ist.

Um den API-Key festzulegen, muss die Datei `env.example` nach `.env` kopiert werden und dort unter der Variable `ORS_API_KEY` gesetzt werden.

Die aufzulösenden Rohdaten der Versammlungen befinden sich in der Datei [rallies.csv](./src/main/resources/rallies.csv).

Mit `make load` werden die Versammlungsdaten zu Koordinaten und Routen aufgelöst und eine HTML-Datei unter `docs/index.html` erzeugt.

Um die aufgelösten Versammlungsdaten anzuschauen, einfach die Datei [index.html](./docs/index.html) in einem Browser öffnen.

## Beteiligung

Fragen und Probleme bitte [hier](https://github.com/CodeforLeipzig/rallymap/issues) melden. [PRs](https://github.com/CodeforLeipzig/rallymap/pulls) sind willkommen.

## License

MIT © [Code for Leipzig](https://codefor.de/leipzig/)

Lizenz siehe Datei [LICENSE](./LICENSE).

Idee und Entwicklung durch [Marvin Frommhold](https://mfrommhold.de/).
