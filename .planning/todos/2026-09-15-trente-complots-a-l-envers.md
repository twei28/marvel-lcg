# Trente manigances annexes étaient dessinées à l'envers

**Constat de l'utilisateur, 15/09/2026**, capture à l'appui sur « Malevolent
Mimic » (`ok020`, némésis d'Okoye) : « et cette carte est à l'envers ».

## La cause, mesurée et non déduite

Le moteur ne tourne les scans QUE s'ils sont en paysage sur le disque
(`ImageCreator.TryRotateImage`, `engine/lib/image_creator.py:20`) :

```python
if width > height:
    img_io = img_io.rotate(90, expand=True)   # PIL : antihoraire
```

Le plateau applique ensuite `rotate(90deg)` en CSS, dans l'autre sens
(`.scan-a-tourner`, `ScanCard.css`), et la carte retombe à l'endroit.

⚠ **Un fichier déjà en portrait n'est PAS tourné par le moteur.** Il doit donc
être stocké exactement dans le sens que le moteur aurait produit, c'est-à-dire
la carte paysage tournée d'un quart de tour ANTIHORAIRE. Trente scans fan-made
étaient tournés dans l'autre sens : le plateau les affichait à 180°.

Vérification faite en comparant, côte à côte, ce que le serveur sert pour une
carte officielle (`/scan/01097b`, titre à gauche) et ce qu'il servait pour
`ok020` (titre à droite).

## Ce qui a été corrigé

Les 30 fichiers sont désormais stockés **en paysage à l'endroit**, comme les
scans officiels : c'est le moteur qui fait la rotation, et la convention
redevient unique. Les originaux de `sauvegardes-serveur/scans-originaux/` ont
suivi, sinon une future réduction aurait ramené le défaut.

⚠ **Chaque carte a été vue à l'œil, deux fois** : une planche de contrôle avant
(pour trier les cassées des bonnes) et une après (pour vérifier les trente).
Le tri était indispensable : sur les 37 manigances stockées en portrait, **7
étaient déjà dans le bon sens** (`ab013`, `sg020`, `dt096`, `dt102`, `nt014`,
`ip017`, `ip035`) et les tourner les aurait cassées.

Cas à part, non touché : `57039a` (« Choosing Sides »), une carte sans art
rendue en texte par le moteur.

## Le gate qui manque, et qui rendrait ça mécanique

Aucun contrôle n'attrape ce défaut : il faut un œil. Une règle simple le
rendrait mécanique : **une carte de type paysage doit être stockée en paysage**
(`w > h`), et le moteur s'occupe du reste. Il resterait à convertir les 7 scans
portrait-mais-corrects, puis à poser le contrôle sur les 866 cartes paysage.

⚠ Ne pas convertir ces 7-là sans la même vérification à l'œil : ils marchent
aujourd'hui.

## Statut

**Corrigé et déployé le 15/09/2026** (30 images, 14,9 Mo, `deployer.ps1 -Images`,
sans redémarrage : le cache d'images vit dans le processus d'une table, une
partie neuve relit les fichiers). Le gate reste à poser.
