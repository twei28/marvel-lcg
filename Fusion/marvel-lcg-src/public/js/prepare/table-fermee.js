// table-fermee.js — dire au joueur que sa table n'existe plus.
//
// ⚠ POURQUOI CE FICHIER EXISTE, mesure du 16/09/2026. Une table fermee laisse
// son onglet ouvert : Caddy ne trouve plus de processus derriere le port, rend
// un 502, et `sonderSalon` avalait l'echec sans un mot (`catch { return }`).
// Resultat observe dans les journaux : 525 requetes en quinze minutes, toutes
// en erreur, pour un ecran que son proprietaire croyait encore vivant.
//
// Ce module ne sonde RIEN : c'est `app.js` qui sait, lui qui interroge deja le
// salon. Il ne fait que MONTRER, sur le modele d'annonce.js — pose sur
// `document.body`, hors du cycle de rendu du wizard, qu'un redessin ne derange
// pas.
import { t } from "/public/js/prepare/langue.js";

let bandeau = null;

function construire() {
  const style = document.createElement("style");
  style.textContent = `
    .table-fermee {
      position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
      z-index: 9100; display: flex; align-items: center; gap: 14px;
      max-width: min(640px, calc(100vw - 24px)); padding: 10px 16px;
      border: 1px solid #f2665a; border-radius: 10px;
      background: linear-gradient(180deg, rgba(46,16,14,.98), rgba(24,10,9,.98));
      box-shadow: 0 8px 30px rgba(0,0,0,.55);
      font: 14px/1.4 system-ui, sans-serif;
    }
    .table-fermee-texte { color: #f6c9c4; font-size: .85rem; }
    .table-fermee-texte b { color: #ffd9d4; display: block; font-size: .95rem; }
    .table-fermee-bouton {
      flex: none; font: inherit; font-size: .8rem; font-weight: 700;
      color: #2b0f0d; background: #f2665a; border: 0; border-radius: 99px;
      padding: 6px 14px; cursor: pointer; white-space: nowrap;
    }
  `;
  document.head.appendChild(style);

  const boite = document.createElement("div");
  boite.className = "table-fermee";
  boite.setAttribute("role", "status");

  const texte = document.createElement("div");
  texte.className = "table-fermee-texte";
  const titre = document.createElement("b");
  titre.textContent = t("Cette table a été fermée.");
  const detail = document.createElement("span");
  detail.textContent = t("Ta partie n'est plus en cours. Reviens à l'accueil pour en lancer une autre.");
  texte.append(titre, detail);

  const bouton = document.createElement("button");
  bouton.type = "button";
  bouton.className = "table-fermee-bouton";
  bouton.textContent = t("Revenir à l'accueil");
  // Le SITE, pas la table : c'est le domaine parent qui sait rouvrir une place.
  bouton.addEventListener("click", () => {
    window.location.href = "https://" + window.location.hostname.split(".").slice(1).join(".") + "/";
  });

  boite.append(texte, bouton);
  return boite;
}

/** Montre ou cache le bandeau. Idempotent : `app.js` l'appelle a chaque tour. */
export function montrerTableFermee(visible) {
  if (visible && !bandeau) {
    bandeau = construire();
    document.body.appendChild(bandeau);
  } else if (!visible && bandeau) {
    bandeau.remove();
    bandeau = null;
  }
}
