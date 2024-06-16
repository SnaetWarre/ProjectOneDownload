# Pulse Pilot

**VOORNAAM NAAM:** Warre Snaet

**Sparringpartner:** Andrei Vasilache

**Projectsamenvatting in max 10 woorden:** Geavanceerde multimeter voor sporters (hartslag, temperatuur, luchtkwaliteit)

**Projecttitel:** Pulse Pilot


# Feedforward gesprekken

## Gesprek 1 (Datum: 23/05/2024)

Lector: Pieter-Jan Beeckman

Vragen voor dit gesprek: 

- vraag 1: Fritzing files nakijken

Dit is de feedback op mijn vragen.

- feedback 1: 
  3.3V in oranje zetten
  Buzzerbedrading controleren 
  Sda / scl in een andere kleur zetten (duidelijkheid)
  Controleer dat bedrading niet te veel over elkaar loopt (vermijd mogelijkheid op verwarring)

## Gesprek 2 (Datum: 24/05/2024)

Lector: Stijn Walcarius

Vragen voor dit gesprek:

-  vraag 1: Is de database dat ik momenteel heb gemaakt voldoende/in orde voor mijn project.

Dit is de feedback op mijn vragen.

- feedback 1: Toevoegen usertable -> settings (maxbpm kunnen bijhouden). De rest is in orde. 

## Feedback Fritzing (Datum: 24/05/2024)

Lector: Geert Desloovere + Pieter-Jan Beeckman

Dit is de feedback op ingediende fritzing files:

24 mei op 16:21
breadboard voedingen verkeerd aangesloten + en - !!!!! alles zal defect zijn! Opmerking verwijderen: bredboard voedingen verkeerd aangesloten + en - !!!!! alles zal defect zijn!
DESLOOVERE Geert

24 mei op 16:21
motor niet rechtstreeks op pi aansluiten, maar met transistor
DESLOOVERE Geert

24 mei op 16:21
one wire heeft ook pull up weerstand nodig
DESLOOVERE Geert

24 mei op 16:21
knop voorzien van veiligheidsweerstand
DESLOOVERE Geert

24 mei op 16:21
waar staat externe voeding in schema?
BEECKMAN Pieter-Jan


## feedback tourmoment (Datum: 28/05/2024)

lectoren: Stijn Walcarius & Pieter-Jan Beeckman

feedback:

- "Voeding 180 graden gedraait = voorbereiding
- Draden moeten hier en daar nog van kleur veranderen?
- Toggle vrij goed maar de knutseldag nog erin zetten 
- Issue werken & branching
- Geen foto’s -> belangerijk voor instructables

## consult Electronics (datum 30/05/2024)

lector: Pieter-jan Beeckman

vragen:
- correcte schakeling?
- waarom mcp kapot?

feedback: 
 - 5v aan air quality sensor v1.3 geschakeld, terwijl mcp3008 aan 3.3V werd geschakeld --> kapot
 - rest schakeling in orde


## feedback backend (Datum: 30/05/2024)

lector: Pieter-Jan Beeckman

feedback:

- ipv "while true" met een while status werken
- laat threads elk apart opstarten ipv allemaal te samen (zodat je met sessionID kan laten werken)
- Zorg dat je aan je sessionID kan komen zodat je deze kan meegeven in je history table

## feedback tourmoment (Datum: 04/06/2024)

feedback:

- toggle op orde brengen
- github (opnieuw) in orde brengen


## feedback consult (Datum: 05/06/2024)

lector: Tijn Veraghtert 

vraag: Switchen van onboard powersupply naar raspberryPi 5V pin?

feedback: 

- Zou moeten lukken, geen zware sensoren/actuatoren (Pieter-jan Beeckman was ook aanwezig en vond het ook veilig)



