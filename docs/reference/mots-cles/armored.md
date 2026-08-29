# Armored (maison, pack `superior_iron_man`)

**Texte imprimé / définition** : « Armored 2. Guard. Patrol. » sur le minion némésis Tony Stark A.I. (si016). Guard et Patrol sont officiels (fiches dédiées). « Armored » n'existe NULLE PART ailleurs : ni dans le moteur, ni sur aucune des 4600+ cartes officielles déjà portées, ni dans le matériel fourni par l'auteur (pas de règles jointes au pack). Ce n'est pas un mot-clé officiel de Marvel Champions : c'est un mot-clé maison de l'auteur (Merlin), non défini.

**Décision utilisateur (29/08/2026)** : question posée avant d'écrire le script (carte de référence absente, aucune règle jointe — cas « mot-clé maison non défini sur les cartes fournies »). Choix retenu : **prévient les 2 premiers dégâts de CHAQUE instance de dégâts** subie par le minion, pas une seule fois dans la partie et pas seulement au combat (donc aussi une trahison qui infligerait des dégâts directement à ce minion, s'il en existait une).

**Mécanisme moteur** : pas de clé `desc` dédiée (contrairement à Guard/Patrol/Toughness) — codé directement dans `si016.py` via un Forced Interrupt sur `Message.WhenUnitWouldTakeDamage`, modèle `Armored Rhino Suit` (`core/rhino/01098.py`) :

```python
def armored_2(effect, message):
    message.PreventDamage(2, effect)

AbilityFactory.WhenUnitWouldTakeDamage(
    AbilityType.ForcedInterrupt,
    "This",
    armored_2,
)
```

**Carte exemple** : `si016` : Tony Stark A.I., seule carte du jeu à porter ce mot-clé.

**Pièges connus** :
- Ne pas confondre avec Toughness (une seule utilisation puis la carte de statut est défaussée) : Armored ici se recharge à chaque instance de dégâts, sans compteur ni statut.
- Réservé à cette seule carte : si un autre pack imprime un jour « Armored X », vérifier d'abord si l'interprétation retenue ici convient avant de la recopier telle quelle — ce n'est pas un mot-clé officiel avec une définition stable, juste l'arbitrage pris pour CETTE carte.

**Variantes maison** : aucune autre recensée pour l'instant.
