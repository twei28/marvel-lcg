# Vérification groupe trap-recompenses (hs125 à hs140, hs200 à hs205)

Scans lus un par un. Les textes d'ambiance sont ignorés. Aucun fichier de données modifié.
Constat général : stats, noms, traits, types, PV, boost, quantités (Trap x/16) tous conformes. Les écarts sont des libellés de texte et des étoiles ★.

## Récapitulatif

| card_id | verdict | résumé |
|---|---|---|
| hs125 | ÉCART | ATK imprimé « 2★ », JSON "2" sans étoile ; texte reformulé (même effet) |
| hs126 | ÉCART | idem hs125 (Trap 2/16) |
| hs127 | ÉCART | ATK « 2★ » absent du desc ; reformulation du Forced Response |
| hs128 | ÉCART | idem hs127 (Trap 4/16) |
| hs129 | ÉCART | « When Revealed » ajouté au JSON, absent du scan ; « If your identity was exhausted this way » reformulé |
| hs130 | ÉCART | idem hs129 |
| hs131 | ÉCART | « When Revealed » ajouté, absent du scan |
| hs132 | ÉCART | idem hs131 |
| hs133 | ÉCART | « When Revealed » ajouté, absent du scan ; Interrupt reformulé (« event » / « event card ») |
| hs134 | ÉCART | idem hs133 |
| hs135 | CONFORME | Tranquilizer Darts (icône mentale plausible, voir note) |
| hs136 | CONFORME | idem |
| hs137 | CONFORME | idem |
| hs138 | CONFORME | Swinging Boulder, « Choose one » en 4 puces = JSON |
| hs139 | CONFORME | idem |
| hs140 | CONFORME | idem |
| hs200 | ÉCART | ★ devant « Interrupt » absent du texte JSON ; ATK « 2★ » : étoile non transcrite |
| hs201 | ÉCART | ★ devant « Response » absent ; ATK « 2★ » non transcrite |
| hs202 | ÉCART | deux ★ devant les phrases de texte absents ; THW/ATK « 0★ » non transcrites |
| hs203 | ÉCART | mineur : « ready a friendly character. That character gains » fondu en « and that character gains » |
| hs204 | CONFORME | Vermin sbire, tout correspond |
| hs205 | ÉCART | scan : « Forced Interrupt: When Lizard attacks, the attack gains piercing » ; JSON : « Lizard's attacks gain piercing » sans label |

Totaux : 7 CONFORMES, 15 ÉCARTS, 0 DOUTES.

## Détail des écarts

### hs125, hs126 (Ferocious Lion, Minion, Trap 1/16 et 2/16)
- Scan : SCH 0, ATK « 2★ », PV 2, traits Trap. Animal. Texte : « ★ While Ferocious Lion is attacking, it gets +1 ATK if the attack is undefended. / Forced Response: After a character the engaged player controls attacks Kraven The Hunter, Ferocious Lion attacks the engaged player. »
- JSON : ATK "2" ; « [star] While attacking, Ferocious Lion gets +1 ATK if the attack is undefended. / Forced Response: After a character controlled by the engaged player attacks Kraven The Hunter, Ferocious Lion attacks that player. »
- Différences : étoile de la stat ATK absente du desc ; formulations différentes. Effet jeu : identique, sauf si le moteur lit l'étoile de la stat.

### hs127, hs128 (Fierce Cheetah, Minion, Trap 3/16 et 4/16)
- Scan : ATK « 2★ ». « ★ Fierce Cheetah's attacks gain piercing. / Forced Response: After a character the engaged player controls attacks Kraven The Hunter, Fierce Cheetah attacks the engaged player. »
- JSON : ATK "2" ; même reformulation (« controlled by the engaged player », « that player »). Effet jeu : identique.

### hs129, hs130 (Bear Trap, Attachment)
- Scan (aucun libellé « When Revealed ») : « Choose to either exhaust your identity or attach Bear Trap to your identity. If your identity was exhausted this way, discard Bear Trap. / Forced Interrupt: When the hero phase ends, you take 1 damage. / Action: Spend a [icône poing, probablement physique, icône douteuse] resource and take 2 damage → discard Bear Trap. »
- JSON : « <b>When Revealed</b>: Choose to either exhaust your identity or attach this card to your identity. If you exhausted your identity, discard this card. ... take 1 damage. ... Action: Spend a [physical] resource and take 2 damage → discard this card. »
- Différences : libellé « When Revealed » ajouté (absent du scan, la carte est imprimée comme une phrase de résolution à la révélation) ; reformulation. Effet jeu : le déclencheur à la révélation est une interprétation de la transcription, cohérente avec la règle d'une carte de rencontre, à valider.

### hs131, hs132 (Capture Net, Attachment)
- Scan : même phrase d'ouverture sans libellé ; « Forced Interrupt: When the hero phase ends, spend a [poing] resource or exhaust your identity. / Interrupt: When you would attack, spend a [poing] resource → discard Capture Net instead. »
- JSON : « When Revealed » ajouté ; reste identique au sens. Icône poing = physique supposée (douteuse).

### hs133, hs134 (Quicksand, Attachment)
- Scan : THW -1, ATK -1, DEF -1 (conformes au JSON). « Interrupt: When you play an event, cancel the effects of that event and discard it → discard Quicksand. » Pas de libellé « When Revealed ».
- JSON : « When Revealed » ajouté ; « When you play an event card, cancel its effects and discard that event → discard Quicksand. » Effet jeu : identique.

### hs200 (Vermin, allié, Hunt Campaign / Basic)
- Scan : coût 2, THW 0 (1 icône), ATK « 2★ » (2 icônes), PV 2, traits Mutate. Predator., icône de ressource en bas à gauche = poing sur fond orange/rouge (physique). Texte : « Vermin enters play with 3 rat counters. / ★ Interrupt: When Vermin attacks, remove 1 rat counter from here → Vermin does not take consequential damage for this attack. »
- JSON : « <b>Interrupt</b>: When Vermin attacks, remove a rat counter from him → ... » sans [star]. THW "0*", ATK "2**" (convention de comptage d'icônes, l'étoile superscript n'est pas distinguée). Effet jeu : ★ non transcrit ; le reste identique.

### hs201 (Scorpion)
- Scan : coût 3, THW 1 (1 icône), ATK « 2★ » (1 icône), PV non lu sur l'image (pas de PV visible, la pastille du coin est le coût), ressource éclair jaune. « ★ Response: After Scorpion attacks and damages an enemy, deal 1 damage to Scorpion → stun that enemy and deal 1 damage to it. »
- JSON : même texte sans [star], HP "3". Note : le scan ne montre pas de PV distinct (pastille « 3 » = coût), la valeur HP 3 du JSON est invérifiable sur le scan. Idem hs200 (HP 2), hs202, hs203 : les PV d'un allié ne sont pas imprimés lisiblement sur ces scans.

### hs202 (Lizard allié)
- Scan : coût 3, THW « 0★ », ATK « 0★ », ressource bleue (même icône à deux nœuds que hs135). « ★ While you are in alter-ego form, Lizard gets +3 THW. / ★ While you are in hero form, Lizard gets +3 ATK. »
- JSON : mêmes phrases sans [star]. Effet jeu : identique.

### hs203 (Vulture allié)
- Scan : « Action: Exhaust Vulture and deal 1 damage to him → ready a friendly character. That character gains the AERIAL trait until the end of the phase. » Ressource : étoile verte (wild probable, icône douteuse). Pas de ★ dans le texte.
- JSON : « ... → ready a friendly character and that character gains the [[AERIAL]] trait until the end of the phase. » Effet jeu : identique.

### hs205 (Lizard sbire)
- Scan : SCH 0, ATK 3, PV 6, boost 3 icônes. « Quickstrike. Retaliate 1. / Forced Interrupt: When Lizard attacks, the attack gains piercing. »
- JSON : « Quickstrike. Retaliate 1. / Lizard's attacks gain piercing. » (sans Forced Interrupt). Effet jeu : proche (perçant sur ses attaques), mais le scan est un déclencheur Forced Interrupt, pas un effet permanent.

## Conformes (une ligne)
- hs135, hs136, hs137 : Tranquilizer Darts, Treachery, « When Revealed: Choose to either spend a [icône à deux nœuds reliés, probablement mentale, même forme que la ressource bleue de hs202] resource or confuse your identity. If you cannot, take 1 damage. » JSON équivalent.
- hs138, hs139, hs140 : Swinging Boulder, « When Revealed: Choose one: exhaust your identity / discard an ally you control / discard an upgrade you control / you take 3 damage. »
- hs204 : Vermin sbire, SCH 0, ATK 2, PV 2, boost 2, traits Mutate. Rat., texte conforme (« remove 1 rat counter from him » = « remove a rat counter »).
