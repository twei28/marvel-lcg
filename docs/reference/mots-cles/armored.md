# Armored (maison, pack `superior_iron_man`)

**Texte imprimé / définition** : « Armored 2. Guard. Patrol. » sur le minion némésis Tony Stark A.I. (si016). Guard et Patrol sont officiels (fiches dédiées). « Armored » n'existe NULLE PART ailleurs : ni dans le moteur, ni sur aucune des 4600+ cartes officielles déjà portées, ni dans le matériel fourni par l'auteur (pas de règles jointes au pack). Ce n'est pas un mot-clé officiel de Marvel Champions : c'est un mot-clé maison de l'auteur (Merlin), non défini.

**Définition** (glossaire fan-made de MC4DB, adoptée le 29/09/2026) :

> « When a character with this keyword would take any amount of damage
> **from an attack**, prevent X of that damage. »

⚠ **Ce qui a changé le 29/09/2026.** L'arbitrage du 29/08/2026 (question posée avant d'écrire le script, carte de référence absente, aucune règle jointe) prévenait 2 dégâts de **chaque** instance, attaque ou non. MC4DB limite aux dégâts **d'une attaque** : une trahison ou une capacité qui blesse ce minion passe en entier. Le script porte désormais `is_from_attack=True`. La carte n'imprime rien qui contredise le glossaire.

**Mécanisme moteur** : pas de clé `desc` dédiée (contrairement à Guard/Patrol/Toughness) — codé directement dans `si016.py` via un Forced Interrupt sur `Message.WhenUnitWouldTakeDamage`, modèle `Armored Rhino Suit` (`core/rhino/01098.py`) :

```python
def armored_2(effect, message):
    message.PreventDamage(2, effect)

AbilityFactory.WhenUnitWouldTakeDamage(
    AbilityType.ForcedInterrupt,
    "This",
    armored_2,
    is_from_attack=True,
)
```

**Carte exemple** : `si016` : Tony Stark A.I., seule carte du jeu à porter ce mot-clé.

**Pièges connus** :
- Ne pas confondre avec Toughness (une seule utilisation puis la carte de statut est défaussée) : Armored se recharge à chaque attaque, sans compteur ni statut.
- **Hors attaque, rien n'est prévenu** : cas « des degats HORS attaque passent en entier » (3 dégâts directs, 3 subis), rouge avec l'ancien script. Il reste vert sous substitution (témoin d'absence d'effet) ; c'est le cas « une ATTAQUE de base du heros ne le blesse pas » qui prouve le module.
- Réservé à cette seule carte : si un autre pack imprime un jour « Armored X », vérifier d'abord si l'interprétation retenue ici convient avant de la recopier telle quelle — ce n'est pas un mot-clé officiel avec une définition stable, juste l'arbitrage pris pour CETTE carte.

**Variantes maison** : aucune autre recensée pour l'instant.
