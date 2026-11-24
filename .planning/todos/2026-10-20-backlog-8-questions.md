# Backlog 8 (connexion et inscription) : points restés ouverts (20/10/2026)

La fiche du 09/10 tranche la mise en page, le bandeau mobile, les deux corrections de texte et le pied de page.
Elle ne tranche pas les points ci-dessous : rien n'a été codé pour eux.

## 1. Palette : TRANCHÉE le 20/10/2026 (Épuré)

Décision de l'utilisateur : ces pages passent en Épuré (fond #111318, surface #1c2028, champ #292e38, filet #383e49, accent bleu #3f86e0,
titres en Bangers), jetons repris de `Fusion/marvel-lcg-src/public/css/affichage-epure-pages.css`. Appliqué au gabarit commun
(connexion, inscription, réinitialisation, confirmations, page des créateurs). L'ancien habillage rouge reste dans le code derrière
`EPURE_FORMULAIRE` (False pour y revenir). Le mode sobre redéfinit les variables par-dessus dans les deux cas.

## 2. Sélecteur FR / EN sur mobile : TRANCHÉE (oui), FAIT
Les mêmes boutons que sur PC, à droite du bandeau.

## 3. Illustration de la scène : TRANCHÉE, la mascotte du moment reste.

## 4. Accents sur tout le site : TRANCHÉE (oui), FAIT
Remis sur toutes les pages rendues par `site/orchestrateur.py` (reprise, signalements, attente, arrêt, installation de l'appli, Discord,
administration, pied de page, barre) et dans les clés de `site/langue.py`. Laissés tels quels volontairement :
- les codes machine comparés par le code ou le client (`"invite inconnu"`, `"pas connecte"`, `"siege invalide"` de l'API d'invitation,
  états et statuts de base de données) ;
- les commentaires et docstrings, les journaux techniques, les chaînes d'erreur internes.
Hors périmètre « accents seulement » : quelques messages restent en français brut, sans passer par `lang.t` (ex. « Trop de tentatives »,
« Ton compte a expiré ... »). À traduire, si souhaité, dans un autre passage.
