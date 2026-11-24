# Restricted

**Texte imprimé / définition** : « Restricted. » Un héros ne peut pas
avoir plus de deux cartes Restricted en jeu sous son contrôle en même
temps (limite globale, toutes cartes Restricted confondues, pas par
carte). C'est un compteur (`Restricted 1` en général), réinitialisé à sa
valeur imprimée à chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Restricted` sur la carte, lue nativement
par le moteur. `HasRestricted`
(`src/game/card/face/attribute/has_restricted.py`) enregistre l'attribut
`Restricted` -> `printed_restricted`, et vérifie la limite via
`CheckRestrictedLimit`, qui délègue à
`player.limit_restricted.CheckLimit` (voir
`src/game/player/limit_monitor/restricted_limit.py`). Le contrôle
s'applique à l'entrée en jeu (`OnWouldEnterPlay`, peut empêcher la carte
d'entrer en jeu si la limite est dépassée), à la sortie de jeu et au
retournement d'une carte (recalcul de la limite). **Aucun script requis**
pour la restriction elle-même : c'est une des « bases automatiques » du
guide, à ne pas recoder inutilement dans le `.py` de la carte.

**Carte exemple** : `03009` : * Captain America's Shield (`desc` contient
`"Restricted": "1"`), lu directement depuis `desc` pour la limite
Restricted elle-même. Un fichier `03009.py` existe bien
(`src/cards/pack/cap/captain_america/03009.py`), mais son contenu
(`AbilityFactory.GiveKeywordToAttached(CardFinder(name="Captain
America"), defense=1, retaliate=1)`) code la capacité imprimée
d'attachement de la carte (donner Defense 1 et Retaliate 1 à Captain
America), pas le mot-clé Restricted. Le script ne doit pas et ne recode
pas la limite Restricted.

**Pièges connus** : ne pas ajouter de logique de comptage Restricted dans
le `.py` d'une carte : c'est entièrement pris en charge par le moteur via
`limit_restricted`. Le cas `03009` est un exemple concret et vérifié où le
script existant sert exclusivement à une autre capacité imprimée que le
mot-clé lui-même ; toute nouvelle fiche/carte Restricted doit vérifier de
la même façon (via `find`) si un script présent code autre chose que la
restriction.

**Variantes maison** : aucune recensée pour l'instant.

## Pièges vus au portage de Raza Longknife (26/10/2026)

- **« You can control 1 additional upgrade that has the restricted keyword »** (`rl008`, comme `hz004`, `20001a` Venom) : `GiveKeywordToAttached("You", control_additional_restricted=CardFinder(card_type=Upgrade))`.
- Mesure (`[rl] rl008`) : Blaster et Sabre (Restricted) en jeu, jouer le Bouclier de Captain America (`03009`, Restricted) : AVEC le Bras les trois restent en jeu ; SANS le Bras seules DEUX des trois restent (clé de cas `rl_en_jeu_parmi`). Le moteur ne laisse donc pas trois Restricted en jeu.
