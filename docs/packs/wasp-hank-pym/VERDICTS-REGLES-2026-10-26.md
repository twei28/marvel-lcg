# Verdicts Wasp (Hank Pym) : Q6 à Q18 (règles RR v1.8 + scans)

Images : `Fusion/marvel-lcg-src/assets/pics/<code>.jpg`. Q1 à Q5 : A, réponses de l'utilisateur.

Bilan : **0 DOUTE RÉEL**. A confirmé : Q6, Q7, Q10, Q14, Q15, Q16, Q17, Q18 (Q11 et Q17 avec un petit correctif). Le code doit changer : **Q8 (léger), Q9, Q12, Q13**.

---

**Q6. hp004 Resize at Will** (hp004.jpg)
Texte : « Action: Change form. Then, if you are in: GIANT hero form, make a basic attack without exhausting. TINY hero form, make a basic thwart without exhausting. »
Verdict : **A confirmé** (obligatoire).
Règle : MAY, « The word "may" indicates that a specified player has the option to resolve the text that follows ». Sans « may », le texte est obligatoire. Une cible existe toujours (le vilain, le complot principal).

**Q7. hp006 Pym Particles** (hp006.jpg)
Texte : « ready each Size Manipulation upgrade you control and place a total of 2 pym counters on them. If none were placed this way, you may change form. »
Verdict : **A confirmé**. Poser un compteur à la fois, au choix, permet toutes les répartitions (2+0, 1+1). Le résultat est identique à B, et la règle ne dit rien d'autre.

**Q8. hp007 Infinite Avengers Mansion** (hp007.jpg)
Texte : « Exhaust this card → place 1 pym counter on a card you control and shuffle 1 identity-specific card from your discard pile into your deck. »
Verdict : **B partiel, petit changement de code**. « identity-specific » codé comme il faut (IDENTITY-SPECIFIC CARD : « designated by the identity icon printed in the bottom right corner »). En revanche, « a card you control » inclut l'identité (OWNERSHIP AND CONTROL : « Identity cards are owned and controlled by the player playing as that identity ») et le Mansion lui-même. Le code (hp007.py l.9) exclut les deux sans appui dans le texte. Les cartes en jeu suffisent : un compteur se pose sur une carte en jeu. Effet pratique faible, puisque seuls Size Manipulation et Ant-Man lisent les compteurs pym. Correctif : retirer le filtre `face is not this and not Identity.IsType(face)`.

**Q9. hp009 Bio-Synthetic Wings** (hp009.jpg)
Texte : « remove X threat from among schemes, where X is equal to the number of times you have changed form this turn. »
Verdict : **B : le code doit changer** (répartition entre manigances).
Règle et usage : « from among schemes » est la formule officielle de répartition (17029 Agile Flight « Remove a total of up to 5 threat from among schemes (as you choose) »). Le projet a déjà tranché ce point sur Storm 36010 (CORRECTIF du 10/10/2026 : « Remove 3 threat from AMONG » = réparti) et sur 04038. Modèle : `RemoveThreatFromSchemesTotal(effect.targets, X, effect)` avec `SetTarget(Scheme2, range=(1, X), repeat_rules="Threat")`. Aujourd'hui hp009 utilise `RemoveThreatFromSchemes` sur une seule cible.

**Q10. hp010 Huge Surprise** (hp010.jpg)
Texte : « Hero Action: Attach this card to an enemy → Until the end of the round, that enemy loses steady and stalwart, and takes 4 damage after it is stunned or confused. This card gains temporary. »
Verdict : **A confirmé**. L'amélioration ne porte pas de « Attach to » : elle entre dans votre zone de jeu (PLAYER'S PLAY AREA : « upgrade cards are placed in a player's play area when they enter play »). L'attacher à un ennemi est le COÛT de la Hero Action (COST ARROW ICON). « takes 4 damage after it is stunned or confused » jusqu'à la fin du round = une Réponse forcée à chaque Sonné/Désorienté posé. « loses steady and stalwart » = perte des mots-clés. « gains temporary » = défaussée en fin de round (TEMPORARY).

**Q11. hp012 The Stinger** (hp012.jpg)
Texte : « deal X damage divided among enemies you choose, where X is equal to the number of times you have changed form this turn. »
Verdict : **A confirmé, avec un petit correctif**. Avec `repeat_rules="Health"`, le code permet déjà de choisir plusieurs fois le même ennemi : la répartition est donc libre, comme la Wasp officielle (« deal a total of 4 damage divided among enemies you choose »). Défaut : `range=(1, 6)` puis `[:x]` laisse choisir MOINS de X emplacements, et des dégâts se perdent. Or « deal X damage » oblige à infliger les X. Correctif : nombre d'emplacements = X exactement.

**Q12. hp013 Identity Crisis : « Shadow of the Past » / « Pursued by the Past »** (hp013.jpg)
Texte : « if there are 5 or more crisis counters here, find Shadow of the Past and reveal it. If you cannot, place 7 pursuit counters on Pursued by the Past. »
Verdict : **B : le code doit changer. Ces cartes ne manquent PAS : ce sont des cartes OFFICIELLES déjà présentes dans le moteur.**
- `01190` Shadow of the Past, set **Standard** (cards.json l.3485) : « Reveal your set-aside nemesis minion… Shuffle the rest of your set-aside nemesis encounter set into the encounter deck ».
- `45075a/b` Pursued by the Past, Environnement Permanent du set **Standard III** (cards.json l.45488).
Règle : FIND, « a player searches each game area where that card could be found (play area, set-aside area, player deck, discard pile, encounter deck, etc.) ». À 5 compteurs ou plus, on cherche donc 01190 (deck rencontre + défausse) et on la révèle. Si le scénario joue avec Standard III, on ne la trouve pas : on pose alors 7 compteurs pursuit sur 45075. Ce n'est pas un trou du zip : **l'entrée n°7 du BACKLOG (ajoutée le 26/10) repose sur une erreur et doit être retirée ou corrigée.** Le choix de l'utilisateur (« coder sans ces cartes ») partait de cette erreur : à lui signaler.

**Q13. hp013 « Then, exhaust Hank Pym → discard this obligation »** (hp013.jpg)
Texte : « Alter-Ego Action: Choose to take 1 damage or place 1 threat on the main scheme for each crisis counter here. Then, exhaust Hank Pym → discard this obligation. »
Verdict : **B : le code doit changer.** TOUT ce qui précède la flèche est le coût de l'Action.
Règle : COST ARROW ICON, « Non-bolded text before the cost arrow icon must be paid and/or resolved in full before the text after the cost arrow icon can be resolved ». COST : « If multiple costs … require payment, those costs must be paid simultaneously ». Les obligations officielles suivent ce modèle (40160 Manufactured Drama : « Exhaust your identity and discard 1 card … for each support you control → discard this card »). Conséquence : l'Action n'est offerte que si Hank Pym est redressé. Le code actuel (hp013.py) laisse subir les dégâts ou la menace même si Hank est déjà incliné, puis garde l'obligation. Correctif : coût = incliner l'identité + choix dégâts/menace ; effet = défausser.

**Q14. hp014 Return of the Prodigal Son** (hp014.jpg)
Texte : « place the upgrade or support in play with the highest cost facedown under here » ; « Boost: Reveal this card. »
Verdict : **A confirmé**. La manigance annexe est dans la zone du vilain. « in play » sans « you control » vise tous les joueurs (IN PLAY), une seule carte. Égalité : le joueur qui résout choisit. Boost « Reveal this card » : révéler une manigance annexe la met en jeu.

**Q15. hp015 Ultron « Find the set-aside Seized Control »** (hp015.jpg, hp016.jpg)
Texte : « When Revealed: Find the set-aside Seized Control attachment and reveal it. If you cannot, seek a HACKED card from the encounter deck and reveal it. »
Verdict : **A confirmé dans les faits, mais la justification est corrigée.** Aucune carte n'ordonne de mettre Seized Control de côté à part. Il est mis de côté AVEC tout le set némésis (NEMESIS ENCOUNTER SET : « At the start of the game, each player sets aside the cards from their associated nemesis set, out of play »). Ultron sort par 01190 Shadow of the Past (« Reveal your set-aside nemesis minion… [puis] Shuffle the rest »). Il est révélé AVANT le mélange : son When Revealed trouve donc Seized Control encore mis de côté. Même chose par 45075b. La branche « If you cannot » (HACKED) ne joue que si Ultron est révélé une 2e fois. Le `BeginGameWithSetAside(["hp016"])` produit le même effet. **À vérifier** : hp016 ne doit pas exister en double (une copie dans le set némésis + une copie générée par BeginGameWithSetAside).

**Q16. hp016 Seized Control** (hp016.jpg)
Texte : « When the attached character would take any amount of damage, place it here instead. Then, if there is at least X damage here, discard this card. X is equal to the resource cost of the card tucked under here. »
Verdict : **A confirmé**. Les dégâts deviennent des jetons sur la carte (remplacement « instead »). TUCK : « Tucked cards are not in play ». Aucun modificateur en jeu ne s'applique donc à la carte glissée : coût = coût imprimé.

**Q17. hp017 Take Over Signal** (hp017.jpg)
Texte : « Treat attached ally as a HACKED minion with a blank text box. Attached minion's SCH is equal to its printed THW and it does not take consequential damage. »
Verdict : **A confirmé**. `TreatAttachedCardAsMinion` remplace la face par un sbire générique (texte vide), SCH = `printed_thwart`. Les sbires ne subissent jamais de dégâts consécutifs (CONSEQUENTIAL DAMAGE : seulement « After an ally attacks/thwarts »). Rien à coder en plus. Deux points relevés en relisant le code, hors question :
(a) le sbire doit avoir le trait **HACKED** : le code fait `CopyTrait(allie)`, il faut vérifier que HACKED s'ajoute (les traits ne font pas partie du texte : TRAITS « not considered to be part of a card's printed text box », donc garder ceux de l'allié est correct) ;
(b) hp017.py ajoute « surge » quand aucun allié n'est trouvé dans le deck : ce n'est **pas imprimé** sur la carte.

**Q18. Icônes de ressource**
Verdict : **A confirmé**, à l'œil sur chaque scan contre `RES` de cards.json : hp002 G (étoile verte = wild), hp003 R (poing), hp004 B (cerveau-molécule), hp005 B, hp006 G, hp007 R, hp008 B, hp009 Y (éclair), hp010 R, hp011 Y, hp012 Y. Tout concorde. Coûts imprimés des identités : hp001a = 2 mentales (Bumble Bee), hp001b = 1 mentale, hp001c = 2 physiques. Icônes boost : hp013 2, hp015 1, hp016/017/018 2, hp014 0 (★ Boost) : conforme à `desc.Boost`.
