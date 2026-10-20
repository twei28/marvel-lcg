# Galactic Storm, lot GS-6 (scénario 3 « Hala Ultimatum » gs138-gs155 et modulaire « Accuser Corps »
gs156-gs160) : questions pour l'utilisateur (20/10/2026)

Une question par point, recommandation en premier, ce que chaque option change en jeu. La lecture
recommandée est celle qui est codée aujourd'hui ; rien d'autre n'a été tranché en silence. Scans : copies
réduites dans `Fusion/marvel-lcg-src/assets/pics/<card_id>.png`, originaux dans
`sauvegardes-serveur/scans-originaux/<card_id>.png`.

## Décisions déjà prises (GS-0, briques communes), appliquées dans ce lot : closes

- **Conventions de lecture** (étoile = renvoi au texte, silhouette après un nombre = « par joueur »,
  pastille orange = points de vie, Y rouge = icône de boost) : appliquées telles quelles.
- **Immunité du mechant HIDDEN** (`AbilityFactory.CannotBeAffectedByPlayerCards`) : brique déjà codée le
  20/10/2026, réutilisée sans modification.
- **Ids** : `gs` + numéro imprimé sur trois chiffres (+a/b pour les deux faces du mechant et des
  manigances principales) ; un card_id par numéro, exemplaires comptés dans les paquets.
- **Icônes de ressource** du Hero Action de gs144/gs145 (« Spend [energy][mental][physical] ») : relues
  par découpe (`.planning/galactic-storm/defs/_crop_tmp.py`, image analysée directement) et comparées à
  gs002 Cosmic Influx (RES=R, icône poing), gs003 Fuel the Fire (RES=B, icône nœuds reliés) et gs004
  Pursued by the Flame (RES=Y, icône éclair) : la lecture initiale (éclair/nœuds/poing = Y/B/R) est
  CONFIRMÉE par la découpe.

## Q1. gs150 : nom imprimé « House of Fiyero », pas « House of Fiero »

La transcription GS-0 (`transcriptions/hala-ultimatum.md`) et l'INVENTAIRE.md avaient lu « House of
Fiero » (sans « y »). La relecture directe du scan inséré (`assets/pics/gs150.png`, visible à l'écran
pendant ce lot) montre clairement « HOUSE OF FIYERO ». Scan : `gs150.png`.
1. **(Recommandé) « House of Fiyero » (nom corrigé, code appliqué).** Change en jeu : rien (nom
   d'affichage seulement), mais corrige une erreur de transcription qui se serait propagée.
2. Garder « Fiero » comme la transcription GS-0 l'avait figé : faux par rapport au scan.
3. Autre (préciser).

## Q2. gs152 : « Secrets of Detention Core » (transcription) contre « Secrets of Detention Cells »
(note antérieure de l'INVENTAIRE.md section 1)

La transcription GS-0 elle-même (lue directement sur le scan, `transcriptions/hala-ultimatum.md` ligne
289) donne « Secrets of Detention Core ». Une note antérieure de synthèse dans `INVENTAIRE.md` §1 (« noms
de fichier qui diffèrent du nom imprimé ») avait écrit « Secrets of Detention Cells » en passant, sans
fiche de transcription dédiée à l'appui. Scan : `gs152.png`.
1. **(Recommandé) « Secrets of Detention Core », la lecture DIRECTE du scan via la fiche de
   transcription dédiée (source la plus fiable).** Change en jeu : rien (nom d'affichage).
2. « Secrets of Detention Cells », la note de synthèse. Change en jeu : rien non plus, mais contredit la
   fiche de transcription dédiée sans raison identifiée.
3. Autre (préciser, par exemple en comparant une nouvelle fois le scan).

## Q3. HIDDEN, moitié attaque : que se passe-t-il si `against_player` est None ?

Le texte dit « whenever a PLAYER would be attacked by the villain, that player is dealt a facedown
encounter card ». Le message `Message.WhenUnitWouldAttack` porte `against_player`, qui peut être `None`
si l'attaque de base ne vise pas directement un joueur (cas rares : attaque indirecte, règle déjà
rencontrée pour les attaques d'ennemi contre ennemi dans la brique commune du 20/10/2026). Code actuel
(`hala_ultimatum/__init__.py`, `VillainNAttaquePasTantQuilEstCache`) : l'attaque est TOUJOURS annulée
(`SetBeInstead`), mais AUCUNE carte n'est distribuée si `against_player` est `None`.
1. **(Recommandé) Annuler l'attaque dans tous les cas, ne distribuer une carte que si un joueur précis
   est identifié.** Change en jeu : dans le cas rare d'une attaque HIDDEN sans joueur visé directement
   (situation non rencontrée en test), l'attaque disparaît simplement sans contrepartie — cohérent avec
   le principe « le mechant HIDDEN n'attaque jamais », moins cohérent avec « cette carte EST distribuée »
   au pied de la lettre.
2. Ne jamais annuler l'attaque si aucun joueur n'est identifié (laisser l'attaque normale se dérouler
   dans ce cas limite). Change en jeu : un mechant HIDDEN pourrait exceptionnellement infliger des dégâts
   directs dans un scénario multijoueur avancé (ex. redirection d'attaque par une autre carte) — contredit
   le principe HIDDEN.
3. Autre (préciser).

## Q4. gs143 Hala, gs141b Hidden Might of Hala (1B) : compteurs « hideout » non prouvés par le harnais

Limite outillage détaillée dans `tools/cas/hala_ultimatum.py` (bloc gs141b) et les deux gabarits : le
compteur `'hideout'` posé pendant la mise en place du scénario se lit à 0 au moment de la vérification du
cas de test, alors que le handler pose bien la valeur correcte EN COURS D'EXÉCUTION (tracé par impression
directe, confirmé). Le MÊME symptôme se reproduit à l'identique avec la fabrique OFFICIELLE
`AbilityFactory.ThisEnterPlayWithCounters` (testée isolément, même résultat) : ce n'est donc pas un défaut
de ce script précis, mais une limite du harnais de test (ou du moteur) sur les compteurs posés pendant la
fenêtre de mise en place de scénario, non identifiée précisément faute de temps.
1. **(Recommandé) Garder le code tel qu'écrit (calcul `2 + 2*Worlds.GetPlayerNumIcon`, `Faces.
   PlaceCountersOn`), le signaler comme NON PROUVÉ par le harnais de test, et vérifier le nombre de jetons
   de repli posés à la mise en place lors d'une VRAIE partie (un joueur : 4 attendus ; deux joueurs : 6).**
   Change en jeu : si le défaut est réel (pas seulement un artefact du harnais), Hala pourrait entrer en
   jeu sans ses jetons de repli, ce qui ferait avancer la manigance principale 1B vers 2A dès le premier
   sbire vaincu (puisque `RetirerRepli` échouerait toujours faute de jeton, déclenchant immédiatement la
   branche « If you cannot » partout où elle existe) — DONC un défaut potentiellement SÉRIEUX s'il se
   confirme en vraie partie, à vérifier en priorité absolue avant toute partie réelle avec ce scénario.
2. Réécrire le mécanisme autrement (ex. poser les jetons depuis le Setup de gs141a plutôt que depuis
   l'AfterCardEnterPlay de gs143) en espérant contourner la limite — tenté une fois pendant ce lot
   (diagnostic), le symptôme persistait identique même depuis WhenCardSetup. Change en jeu : aucun
   changement de règle, tentative de contournement technique seulement.
3. Autre (préciser, par exemple demander un diagnostic plus approfondi du moteur avant la prochaine
   partie).

## Q5. gs156/gs160 : dégâts non mesurés après une activation forcée par script (`DoActivate`)

Détaillé dans `ACCUSER-CORPS-GABARITS.md`, section « Pistes à reprendre ». Les cas `[ac] gs156` (bonus
+1 ATK d'une attaque) et `[ac] gs160` (« each ACCUSER CORPS enemy activates against you ») mesurent tous
les deux 0 dégât sur l'identité du joueur après une attaque/activation forcée, alors que le même
mécanisme de base (`face.DoActivate`) FONCTIONNE dans `[hu] gs155` (mesuré différemment, via
`cartes_distribuees` plutôt que `degats_identite`, puisque le mechant y est HIDDEN).
1. **(Recommandé) Ne rien changer dans le code (il suit le modèle officiel 11051 Ancient Grudge à
   l'identique), noter le défaut de preuve, et vérifier ces deux capacités en partie réelle avant de les
   considérer acquises.** Change en jeu : si un défaut réel existe (pilote de test qui défend
   automatiquement, ou ciblage différent du prévu), gs156 et gs160 pourraient ne pas infliger les dégâts
   imprimés en vraie partie — à vérifier en priorité.
2. Réécrire ces deux capacités avec une méthode différente (ex. `Enemy.AttackCharacter` au lieu de
   `DoActivate`) sans certitude que cela change le résultat du test. Change en jeu : aucun changement de
   règle prévu, tentative de contournement technique.
3. Autre (préciser).

## Q6. gs144 : Hero Action (défausse par dépense de ressources) non prouvée par le harnais

`[hu] gs144 Hero Action` échoue (« gs144 est encore en jeu ») alors que le MÊME modèle de coût
(`Cost("YBR")`, `PlayerActionToDiscardThis`) est utilisé avec succès ailleurs dans le dépôt (01118 Sonic
Converter, gs083 Optic Blast Cannon du lot GS-4, dont le gabarit affiche « Carte terminée : OUI »).
1. **(Recommandé) Ne rien changer dans le code (modèle identique à des cartes déjà validées), noter le
   défaut de preuve de CE cas précis (possible ordre de paiement du pilote de test avec trois couleurs
   différentes), et vérifier en partie réelle.** Change en jeu : aucun changement de règle prévu.
2. Retravailler le cas de test avec un montage différent (main contenant plus de cartes de chaque
   couleur, pour laisser plus de choix au pilote automatique). Non tenté faute de temps.
3. Autre (préciser).

## Q7. gs153 : « discard cards from the encounter deck until... » ne défausse pas la carte neutre attendue

`[hu] gs153 ... DEJA un tenace` échoue (« 01186 dans la defausse rencontre = 0 »), alors que la recherche
elle-même semble aboutir (`en_jeu: ["gs149"]` passe dans le même cas). Cause non élucidée faute de temps.
1. **(Recommandé) Ne rien changer dans le code, noter le défaut de preuve, vérifier en partie réelle.**
   Change en jeu : aucun changement de règle prévu ; si un défaut réel existe, la défausse-jusqu'à
   pourrait laisser le deck rencontre dans un état incorrect (carte neutre non défaussée alors qu'elle
   aurait dû l'être).
2. Retravailler `Worlds.DiscardEncounterCardsUntil` avec un `CardFinder` différent. Non tenté faute de
   temps.
3. Autre (préciser).

## Q8. gs154 : « +2 boost icons » (`HasBoostIcon.GainBoostIcons`) sans aucun cas de test fiable

C'est la PREMIÈRE utilisation de cette API publique (`game/card/face/attribute/has_boost_icon.py`,
`GainBoostIcons`) dans tout le dépôt — aucune carte existante ne la cite comme modèle. Le cas écrit
pendant ce lot utilisait une sonde de mise au point (toujours rouge par construction) et a été retiré de
la batterie finale faute d'un montage fiable.
1. **(Recommandé) Garder le code (l'API est documentée, publique, et le mécanisme — augmenter le compte
   d'icônes de boost d'une carte en cours de résolution — correspond exactement au texte imprimé), et
   vérifier en partie réelle (compter les icônes de boost effectivement ajoutées quand l'ennemi qui
   s'active a un tenace).** Change en jeu : aucun changement de règle prévu ; capacité non prouvée par le
   harnais à ce jour.
2. Chercher une autre API pour le même effet. Non tenté faute de temps, aucune alternative identifiée
   dans le moteur.
3. Autre (préciser).

## Q9. Encounter_sets en mode Expert : « Standard » seul ou « Standard » + « Expert » ?

REGLES.md §10 cite « Encounter deck: Hala Ultimatum, Accuser Corps, Standard » SANS mentionner « Expert »,
contrairement à la convention générale du livret (et à Kree Sentry, lot GS-4, qui ajoute le set « expert »
en mode Expert). Le code actuel (`inserer_gs6.py`, `scenarios()`) AJOUTE « expert » aux
`encounter_sets` en mode Expert, par cohérence avec Kree Sentry plutôt que par lecture littérale de
REGLES.md §10.
1. **(Recommandé) Garder l'ajout du set « expert » en mode Expert (cohérence avec Kree Sentry et la
   convention générale Marvel Champions), le texte de REGLES.md §10 étant probablement elliptique plutôt
   qu'une exception volontaire.** Change en jeu : en mode Expert, le deck rencontre contient en plus les
   cartes officielles du set « Expert » du moteur, comme pour Kree Sentry.
2. Lecture littérale : SEULEMENT « Standard » dans les deux modes, jamais « Expert ». Change en jeu : un
   deck rencontre identique en Standard et en Expert (hors le stade du mechant et le set modulaire),
   contrairement à la convention générale.
3. Autre (préciser, par exemple demander confirmation à l'auteur).

## Q10. Accuser Corps : modulaire complet (7 cartes) sans règle « N sur M », contrairement à Imperial Guard

REGLES.md §10 mentionne seulement « Accuser Corps can be removed/added via customization rules », sans la
règle « N cartes sur M » qu'Imperial Guard porte (livret p.14, lot GS-4). Le code actuel
(`accuser_corps_cards.py`, `inserer_gs6.py`) monte le set modulaire COMPLET (7 cartes, pas de
`random_pick`).
1. **(Recommandé) Set modulaire complet, sans tirage partiel (lecture littérale de REGLES.md : aucune
   règle de ce genre n'est citée pour Accuser Corps).** Change en jeu : les 7 cartes d'Accuser Corps sont
   TOUTES disponibles dans le deck rencontre quand ce modulaire est choisi, contrairement à Imperial
   Guard (9 cartes sur 23).
2. Appliquer quand même une règle de tirage partiel par analogie avec Imperial Guard. Change en jeu : un
   sous-ensemble aléatoire d'Accuser Corps à chaque partie — non étayé par le texte actuel.
3. Autre (préciser, par exemple demander confirmation à l'auteur ou chercher une règle manquante dans le
   livret).
