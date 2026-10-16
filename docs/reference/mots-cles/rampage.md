# Rampage X

**Texte imprimé / définition** : mot-clé MAISON de l'auteur Inkwire (aspects TMNT),
défini sur la carte même par son texte de rappel :

> ★ Rampage 3. *(As an additional cost for this card, take 3 damage and discard 3
> cards from the top of your deck.)*

Huit cartes le portent, toutes des ÉVÉNEMENTS au trait FERAL, tous à coût étoilé
(« 1★ », « 3★ ») :

| Aspect | Carte | X |
|---|---|---|
| Aggression | Apex Predator (`ua002`) | 2 |
| Aggression | Demolish (`ua015`) | 3 |
| Justice | Dire Straits | 3 |
| Justice | Feral Cunning | 2 |
| Leadership | Down the Drain | 2 |
| Leadership | Rubble Rouser | 3 |
| Protection | Primal Provisions | 2 |
| Protection | Autodefenestration | 2 |

⚠ La consigne de départ en listait SEPT : **Autodefenestration** (Protection, coût
0★, « DEFENSE. FERAL. NYC. ») porte aussi « ★ Rampage 2 ». Relevé sur le scan le
16/10/2026. Les card_id exacts de toutes les cartes sont dans
`Fusion/marvel-lcg-src/tools/tmnt_aspects_numerotation.tsv`.

**Le « ★ » devant Rampage** : ce n'est PAS une capacité permanente d'encart ni un
effet Boost. C'est l'icône étoile des Rules Reference v1.8 (entrée « Star Icon »,
p. 40) : une étoile posée à côté d'une valeur (ici le COÛT, « 3★ ») rappelle
qu'une capacité obligatoire du texte modifie l'usage de cette valeur ; l'étoile
du texte marque la capacité correspondante. **Aucun effet en soi, zéro ligne de
code** : seul le coût additionnel compte. Dans `cards.json`, le coût s'écrit avec
l'étoile, comme les officielles (`60048` Army of One : `"Cost": "1*"`), et le texte
garde « [star] Rampage 3. ».

**Règles officielles appliquées** (Rules Reference v1.8, « Cost », p. 13-14) :

- Un coût additionnel se paie EN MÊME TEMPS que le coût en ressources ; si l'on ne
  peut pas tout payer, on ne paie rien et la carte ne se résout pas.
- « If taking damage is a cost, that cost is not considered paid unless all of
  that damage was taken. » Un Tough sur l'identité empêche les dégâts : le coût
  n'est PAS payé, l'effet n'a pas lieu. Comportement commun à tous les coûts
  `CostFunc.TakeDamage` du moteur (`TakeDamageOnCall`), non spécifique à Rampage.
- Payer le coût peut vaincre son propre héros : rien ne l'interdit (même lecture
  que le correctif du 10/09/2026 dans `TakeDamageOnCall`). La partie est alors
  perdue pour ce joueur.

**Lectures arbitrées (questions ouvertes à l'utilisateur, la lecture codée est la
plus fidèle trouvée)** :

1. **Deck de moins de X cartes.** CONFIRMÉ par l'utilisateur le 16/10/2026. Lecture codée : la carte reste JOUABLE ; on
   défausse ce qui reste, le deck s'épuise, on remélange la défausse, on prend
   1 carte rencontre et rien n'est défaussé du nouveau deck (Rules Reference,
   « Player Deck », p. 33 : « If the player's deck empties while the player was
   discarding cards from their deck, no further cards are discarded from the newly
   shuffled deck »). C'est l'arbitrage utilisateur DÉJÀ rendu le 25/09/2026 pour
   tout coût « discard the top N cards of your deck » (`CostFunc.DiscardDeckTopCards`,
   signalements 21/22 de Yarro) : Rampage le réutilise tel quel, il n'en crée pas
   un second. Seul un deck ET une défausse vides rendent le coût impayable.
2. **Forme alter-ego.** Rien dans « take X damage » ne vise la forme : l'identité
   subit les dégâts dans les deux formes, le coût est payable en alter-ego. Les
   huit porteurs sont toutefois des « Hero Action » / « Hero Response » /
   « Hero Interrupt » (vérifié sur les scans) : la question ne se pose pas en
   pratique tant qu'aucune carte « Alter-Ego » ne porte Rampage.

**Mécanisme moteur** : `CostFunc.Rampage(X)` (`src/game/ability/cost_func.py`,
AJOUT du 16/10/2026). UN seul coût, qui compose les deux coûts existants dans
l'ordre imprimé : `CostFunc.TakeDamage(X, "YourIdentity")` (règle des dégâts
empêchés comprise) puis `CostFunc.DiscardDeckTopCards("YourDeck", X)` (règle du
deck court comprise). Les cartes défaussées restent lisibles par
`effect.cost_func.Get(CostFunc.Rampage).return_discarded_cards`.

Une ligne dans le script de la carte, sur la capacité de JEU de l'événement :

```python
AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, demolish)
.SetPlay().SetLabel('attack').SetTarget(Enemy)
.SetCostFunc(CostFunc.Rampage(3)),
```

**Carte exemple** : `ua015` Demolish (pack `tmnt_aspect_aggression`),
`src/cards/pack/tmnt_aspect_aggression/ua015.py`. Cas dédiés :
`Fusion/marvel-lcg-src/tools/cas/rampage.py`.

**Pièges connus** :

- Ne PAS coder Rampage comme deux `SetCostFunc` séparés : ça marche, mais la carte
  perd l'endroit unique où lire les cartes défaussées, et une relecture du
  mot-clé devrait se faire à deux endroits.
- Ne PAS le poser sur une capacité `WhenCardPlayed` / `Response` après coup : c'est
  un COÛT, il se paie avant que l'événement ne se résolve, et un coût impayé
  annule tout l'effet.
- Le coût étoilé (« 3* ») : ne pas ajouter le X de Rampage au coût en ressources ;
  l'étoile n'est qu'un rappel.

**Variantes maison** : aucune connue hors TMNT.
