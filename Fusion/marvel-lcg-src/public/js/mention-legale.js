// mention-legale.js : la mention légale des pages hors plateau (10/10/2026).
//
// Texte validé mot pour mot par l'utilisateur : ne pas le reformuler. Les
// traductions anglaises sont dans prepare/dico-en.js, comme le reste du site.
//
// Deux formes :
//   - la LIGNE COURTE, posée en pied de page (petite, grise) sur toute page qui
//     charge ce module ;
//   - le TEXTE COMPLET, posé à la place dans l'élément `[data-mention-legale]`
//     quand la page en a un (crédits).
// Le plateau ne charge pas ce module : il n'y a rien à y voir.
"use strict";

// Les phrases restent écrites dans `t("…")` : la gate des traductions du site
// (ui-app/src/site-langue.test.ts) ne vérifie que les littéraux.
import { t } from "/public/js/prepare/langue.js";

const style = document.createElement("style");
style.textContent = `
  .mention-legale {
    box-sizing: border-box; width: 100%; max-width: 100%; margin: 0; padding: 14px 16px 18px;
    text-align: center; font: 11px/1.5 system-ui, sans-serif; color: #80868f;
    overflow-wrap: anywhere;
  }
  .mention-legale-complete { font-size: 13px; line-height: 1.6; max-width: 46rem; margin: 0 auto; }
  html[data-affichage="sobre"] .mention-legale { color: var(--mute, #7d828a); }
`;
document.head.appendChild(style);

const cible = document.querySelector("[data-mention-legale]");
if (cible) {
    cible.classList.add("mention-legale", "mention-legale-complete");
    cible.textContent = t("Projet de fans, gratuit et non officiel. Marvel Champions: The Card Game est un jeu de Fantasy Flight Games (Asmodee). Les personnages et illustrations Marvel appartiennent à Marvel. Ce site n'est ni affilié à ces sociétés ni approuvé par elles. Il sert de vitrine et d'outil de jeu : il faut posséder le jeu pour l'utiliser.");
} else {
    const pied = document.createElement("footer");
    pied.className = "mention-legale";
    pied.textContent = t("Projet de fans non officiel · Marvel Champions © Fantasy Flight Games (Asmodee) · Personnages © Marvel · Il faut posséder le jeu pour jouer");
    // Les petites pages qui centrent leur unique carte avec un `body` en flex
    // LIGNE (rejoindre, authenticate) auraient mis le pied À CÔTÉ de la carte :
    // le flex passe à la ligne, le pied prend toute une ligne sous la carte, et
    // les deux lignes restent centrées. (Une colonne élargissait la carte au
    // téléphone : en ligne, elle peut encore rétrécir.)
    const corps = getComputedStyle(document.body);
    if (corps.display === "flex" && corps.flexDirection === "row") {
        document.body.style.flexWrap = "wrap";
        document.body.style.alignContent = "center";
        pied.style.flex = "0 0 100%";
    }
    document.body.appendChild(pied);
}
