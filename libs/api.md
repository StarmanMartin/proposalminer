# API Zugriff

Durch das Aufkommen von Electronic Laboratory Notebooks (ELNs) wird der Zugriff auf die in NAOMI verwalteten Daten durch
andere Software immer wichtiger. Unser Ziel ist es, diesem Nutzungsszenario schrittweise immer besser gerecht zu werden.
Dazu wird incrementell eine Schnittstelle (API) aufgebaut, die den Zugriff auf Proposal-, Status-Report- und
Publikationsdaten erlaubt oder vereinfacht.

## Konzept

Für den Zugriff von anderen Applikationen wird eine neue Nutzer-Rolle eingeführt: `API Client`. Durch die
Rolle werden die Zugriffsberechtigungen geregelt.

Beispielsweise haben API Clients generell nur **Lesezugriff** und auch nur für bestimmte Endpunkte.

Aktuell müssen sich solche Nutzer über den normalen "Nutzername+Passwort"-Mechanismus anmelden und das erhaltene Cookie
bei der weiteren Kommunikation mitsenden.

Dieses Konzept erlaubt es dem UserOffice, die Nutzer wie gewohnt zu verwalten und ihnen bestimmte Technologien zuzuweisen.

Als Endpunkte wird eine kleine Menge der aktuell vorhandenen angeboten, im Speziellen jene für den Excel-Export.

### Ausblick

In Zukunft wird eventuell eine Token-basierte Authentifizierung angeboten, da diese die Implementierung von Clienten
weiter vereinfachen könnte, indem Login und Aufrechterhaltung einer Session nicht mehr notwendig sein würden.

Außerdem sind spezielle Endpunkte in Planung, die die Daten in JSON (oder anderen gewünschten Formaten) anbieten und
passende HTTP-Status-Codes zurückliefern.

## Schnittstellenbeschreibung

### `GET # API Zugriff

Durch das Aufkommen von Electronic Laboratory Notebooks (ELNs) wird der Zugriff auf die in NAOMI verwalteten Daten durch
andere Software immer wichtiger. Unser Ziel ist es, diesem Nutzungsszenario schrittweise immer besser gerecht zu werden.
Dazu wird incrementell eine Schnittstelle (API) aufgebaut, die den Zugriff auf Proposal-, Status-Report- und
Publikationsdaten erlaubt oder vereinfacht.

## Konzept

Für den Zugriff von anderen Applikationen wird eine neue Nutzer-Rolle eingeführt: `API Client`. Durch die
Rolle werden die Zugriffsberechtigungen geregelt.

Beispielsweise haben API Clients generell nur **Lesezugriff** und auch nur für bestimmte Endpunkte.

Aktuell müssen sich solche Nutzer über den normalen "Nutzername+Passwort"-Mechanismus anmelden und das erhaltene Cookie
bei der weiteren Kommunikation mitsenden.

Dieses Konzept erlaubt es dem UserOffice, die Nutzer wie gewohnt zu verwalten und ihnen bestimmte Technologien zuzuweisen.

Als Endpunkte wird eine kleine Menge der aktuell vorhandenen angeboten, im Speziellen jene für den Excel-Export.

### Ausblick

In Zukunft wird eventuell eine Token-basierte Authentifizierung angeboten, da diese die Implementierung von Clienten
weiter vereinfachen könnte, indem Login und Aufrechterhaltung einer Session nicht mehr notwendig sein würden.

Außerdem sind spezielle Endpunkte in Planung, die die Daten in JSON (oder anderen gewünschten Formaten) anbieten und
passende HTTP-Status-Codes zurückliefern.

## Schnittstellenbeschreibung

### `GET /proposal/exportAsExcel`
Liefert eine Proposalliste in Form eines Excel-Dokuments (`xls`-Format, nicht `xlsx`). Es werden
nur die Proposals für die Technologien des Nutzers exportiert.

#### Parameter
* `proposalcallnumber`*: Verpflichtende Angabe der Call-Nummer
* `status`: Proposal-Status und/oder Proposal-Akzeptanzstatus (`INCOMPLETE`, `NOT_VALIDATED`, `VALIDATED`, `UNDECIDED`,
  `ACCEPTED`, `REJECTED`, `ON_WAITLIST`, `ACCEPTED_WAS_ON_WAITLIST`, `REJECTED_WAS_ON_WAITLIST`), kann mehrfach angegeben
  werden
* `offset`: Index des ersten zu liefernden Eintrag, 0-basiert (hauptsächlich für Paginierung)
* `max`: Maximale Anzahl an Einträgen (hauptsächlich für Paginierung)
* `sort`: Sortierkriterium, z.B. `referenceKey` (hauptsächlich für Paginierung)
* `order`: Sortierreihenfolge, `asc` oder `desc` (hauptsächlich für Paginierung)

#### Status-Codes
* `200`: Bei Erfolg
* `302`: Wenn man entweder keine aktive Session hat, oder keine Berechtigung auf den Endpunkt zuzugreifen. Hinweise gibt
  der `Location`-Header der Antwort.

### `GET /publication/exportPublications`
Liefert eine Publikationsliste in Form eines Excel-Dokuments (`xls`-Format, nicht `xlsx`).

#### Parameter
* `exportType`: Typ des Ergebnisdatei (`EXCEL`, `RIS`, `BIBTEX`)
* `proposalcallnumber`: Angabe der Call-Nummer(n), kann mehrfach angegeben werden
* `publicationInstrument`: Angabe der Technologie-Kürzel, kann mehrfach angegeben werden
* `search`: Suchstring
* `year`: Einschränkung auf ein oder mehrere Jahr(e), kann mehrfach angegeben werden
* `status`: Publikationsstatus aus Sicht der KNMF (`UNDECIDED`, `ACKNOWLEDGED`, `NOT_ACKNOWLEDGED`, `INSUFFICIENT`),
  kann mehrfach angegeben werden
* `type`: Publikationstyp (`BOOK`, `JOURNAL`, `PHD_THESIS`, `PROCEEDINGS`, `POSTER`, `TALK`, `RESEARCH_DATA`, `OTHER`),
  kann mehrfach angegeben werden
* `origin`: Quelle, also ob vom Nutzer eingetragen oder automatisch importiert (`imported`)
* `offset`: Index des ersten zu liefernden Eintrag, 0-basiert (hauptsächlich für Paginierung)
* `max`: Maximale Anzahl an Einträgen (hauptsächlich für Paginierung)
* `sort`: Sortierkriterium, z.B. `referenceKey` (hauptsächlich für Paginierung)
* `order`: Sortierreihenfolge, `asc` oder `desc` (hauptsächlich für Paginierung)

#### Status-Codes
* `200`: Bei Erfolg
* `302`: Wenn man entweder keine aktive Session hat, oder keine Berechtigung auf den Endpunkt zuzugreifen. Hinweise gibt
  der `Location`-Header der Antwort.

### `GET /statusReport/export`
Liefert die Liste der Status-Reports in Form eines Excel-Dokuments (`xls`-Format, nicht `xlsx`).

#### Parameter
* `proposalcallnumber`: Angabe der Call-Nummer(n), kann mehrfach angegeben werden
* `search`: Suchstring
* `instrumentSpecificProjectStatusFilter_instruments`: Technologie-Kürzel-Filter, kann mehrfach angegeben werden
* `instrumentSpecificProjectStatusFilter_projectStatuses`: Projektstatus-Filter (`CANCELLED`, `NOT_YET_STARTED`,
  `BEHIND_SCHEDULE_AND_CRITICAL`, `BEHIND_SCHEDULE_BUT_NOT_CRITICAL`, `ON_TIME`, `CLOSED`, `LONGTERM_NOT_COMPLETED`,
  `SCHEDULED`, `UNSCHEDULED`),
  kann mehrfach angegeben werden
* `type`: Proposaltyp (`STANDARD`, `FAST_TRACK`, `LONG_TERM`, `PROPRIETARY`, `THIRD_PARTY_NON_PROPRIETARY`,
  `THIRD_PARTY_PROPRIETARY`, `HELMHOLTZ`, `INHOUSE`),
  kann mehrfach angegeben werden
* `acceptance`: Proposal-Akzeptanz-Status (`ACCEPTED`, `ACCEPTED_WAS_ON_WAITLIST`, `ON_WAITLIST`)
* `from`: Startdatum des Suchzeitraums in ISO-Format (`2024-04-17`)
* `to`: Enddatum des Suchzeitraums in ISO-Format (`2024-12-31`)
* `latestOnly`: Flag, ob man nur jeweils den letzten Report pro Technologie oder die ganze Historie möchte (`true` oder `false`)
* `withAttachments`: Flag, ob man die Attachments auch haben möchte (**Achtung! Ändert das Ausgabeformat in ZIP!**)
* `offset`: Index des ersten zu liefernden Eintrag, 0-basiert (hauptsächlich für Paginierung)
* `max`: Maximale Anzahl an Einträgen (hauptsächlich für Paginierung)
* `sort`: Sortierkriterium, z.B. `referenceKey` (hauptsächlich für Paginierung)
* `order`: Sortierreihenfolge, `asc` oder `desc` (hauptsächlich für Paginierung)

#### Status-Codes
* `200`: Bei Erfolg
* `302`: Wenn man entweder keine aktive Session hat, oder keine Berechtigung auf den Endpunkt zuzugreifen. Hinweise gibt
  der `Location`-Header der Antwort.`
Liefert eine Proposalliste in Form eines Excel-Dokuments (`xls`-Format, nicht `xlsx`). Es werden
nur die Proposals für die Technologien des Nutzers exportiert.

#### Parameter
* `proposalcallnumber`*: Verpflichtende Angabe der Call-Nummer
* `status`: Proposal-Status und/oder Proposal-Akzeptanzstatus (`INCOMPLETE`, `NOT_VALIDATED`, `VALIDATED`, `UNDECIDED`,
  `ACCEPTED`, `REJECTED`, `ON_WAITLIST`, `ACCEPTED_WAS_ON_WAITLIST`, `REJECTED_WAS_ON_WAITLIST`), kann mehrfach angegeben
  werden
* `offset`: Index des ersten zu liefernden Eintrag, 0-basiert (hauptsächlich für Paginierung)
* `max`: Maximale Anzahl an Einträgen (hauptsächlich für Paginierung)
* `sort`: Sortierkriterium, z.B. `referenceKey` (hauptsächlich für Paginierung)
* `order`: Sortierreihenfolge, `asc` oder `desc` (hauptsächlich für Paginierung)

#### Status-Codes
* `200`: Bei Erfolg
* `302`: Wenn man entweder keine aktive Session hat, oder keine Berechtigung auf den Endpunkt zuzugreifen. Hinweise gibt
  der `Location`-Header der Antwort.

### `GET /publication/exportPublications`
Liefert eine Publikationsliste in Form eines Excel-Dokuments (`xls`-Format, nicht `xlsx`).

#### Parameter
* `exportType`: Typ des Ergebnisdatei (`EXCEL`, `RIS`, `BIBTEX`)
* `proposalcallnumber`: Angabe der Call-Nummer(n), kann mehrfach angegeben werden
* `publicationInstrument`: Angabe der Technologie-Kürzel, kann mehrfach angegeben werden
* `search`: Suchstring
* `year`: Einschränkung auf ein oder mehrere Jahr(e), kann mehrfach angegeben werden
* `status`: Publikationsstatus aus Sicht der KNMF (`UNDECIDED`, `ACKNOWLEDGED`, `NOT_ACKNOWLEDGED`, `INSUFFICIENT`),
  kann mehrfach angegeben werden
* `type`: Publikationstyp (`BOOK`, `JOURNAL`, `PHD_THESIS`, `PROCEEDINGS`, `POSTER`, `TALK`, `RESEARCH_DATA`, `OTHER`),
  kann mehrfach angegeben werden
* `origin`: Quelle, also ob vom Nutzer eingetragen oder automatisch importiert (`imported`)
* `offset`: Index des ersten zu liefernden Eintrag, 0-basiert (hauptsächlich für Paginierung)
* `max`: Maximale Anzahl an Einträgen (hauptsächlich für Paginierung)
* `sort`: Sortierkriterium, z.B. `referenceKey` (hauptsächlich für Paginierung)
* `order`: Sortierreihenfolge, `asc` oder `desc` (hauptsächlich für Paginierung)

#### Status-Codes
* `200`: Bei Erfolg
* `302`: Wenn man entweder keine aktive Session hat, oder keine Berechtigung auf den Endpunkt zuzugreifen. Hinweise gibt
  der `Location`-Header der Antwort.

### `GET /statusReport/export`
Liefert die Liste der Status-Reports in Form eines Excel-Dokuments (`xls`-Format, nicht `xlsx`).

#### Parameter
* `proposalcallnumber`: Angabe der Call-Nummer(n), kann mehrfach angegeben werden
* `search`: Suchstring
* `instrumentSpecificProjectStatusFilter_instruments`: Technologie-Kürzel-Filter, kann mehrfach angegeben werden
* `instrumentSpecificProjectStatusFilter_projectStatuses`: Projektstatus-Filter (`CANCELLED`, `NOT_YET_STARTED`,
  `BEHIND_SCHEDULE_AND_CRITICAL`, `BEHIND_SCHEDULE_BUT_NOT_CRITICAL`, `ON_TIME`, `CLOSED`, `LONGTERM_NOT_COMPLETED`,
  `SCHEDULED`, `UNSCHEDULED`),
  kann mehrfach angegeben werden
* `type`: Proposaltyp (`STANDARD`, `FAST_TRACK`, `LONG_TERM`, `PROPRIETARY`, `THIRD_PARTY_NON_PROPRIETARY`,
  `THIRD_PARTY_PROPRIETARY`, `HELMHOLTZ`, `INHOUSE`),
  kann mehrfach angegeben werden
* `acceptance`: Proposal-Akzeptanz-Status (`ACCEPTED`, `ACCEPTED_WAS_ON_WAITLIST`, `ON_WAITLIST`)
* `from`: Startdatum des Suchzeitraums in ISO-Format (`2024-04-17`)
* `to`: Enddatum des Suchzeitraums in ISO-Format (`2024-12-31`)
* `latestOnly`: Flag, ob man nur jeweils den letzten Report pro Technologie oder die ganze Historie möchte (`true` oder `false`)
* `withAttachments`: Flag, ob man die Attachments auch haben möchte (**Achtung! Ändert das Ausgabeformat in ZIP!**)
* `offset`: Index des ersten zu liefernden Eintrag, 0-basiert (hauptsächlich für Paginierung)
* `max`: Maximale Anzahl an Einträgen (hauptsächlich für Paginierung)
* `sort`: Sortierkriterium, z.B. `referenceKey` (hauptsächlich für Paginierung)
* `order`: Sortierreihenfolge, `asc` oder `desc` (hauptsächlich für Paginierung)

#### Status-Codes
* `200`: Bei Erfolg
* `302`: Wenn man entweder keine aktive Session hat, oder keine Berechtigung auf den Endpunkt zuzugreifen. Hinweise gibt
  der `Location`-Header der Antwort.