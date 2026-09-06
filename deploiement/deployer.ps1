# =============================================================================
#  NarwhalChampions - deploiement. A relancer a chaque mise a jour.
#
#     powershell -ExecutionPolicy Bypass -File .\deployer.ps1
#     ...\deployer.ps1 -Code      (code seulement)
#     ...\deployer.ps1 -Images    (images seulement, sans redemarrage)
#
#  Le depot ne suffit pas : assets/pics/ est dans le .gitignore, les images
#  custom ne voyagent que par ce script.
#
#  ATTENTION : l'etape « Images custom » ne synchronise que assets/pics.
#  Les scans francais (assets/pics-fr) sont deja sur le serveur et n'y
#  bougent plus ; un scan francais AJOUTE ici n'y montera pas tout seul.
#
#  N'utilise que ssh, scp et tar, tous fournis avec Windows 10/11.
# =============================================================================
param(
  [switch]$Code,
  [switch]$Images
)
$ErrorActionPreference = "Stop"

$IP      = "178.105.177.39"
$DOMAINE = "narwhalchampions.com"
$DIST    = "/opt/narwhal"

$ICI    = Split-Path -Parent $MyInvocation.MyCommand.Definition
$PROJET = Split-Path -Parent $ICI
$CLE    = Join-Path $ICI "cle_narwhal"
$PICS   = Join-Path $PROJET "Fusion\marvel-lcg-src\assets\pics"
$PICS_DIST = "$DIST/Fusion/marvel-lcg-src/assets/pics"

$faireCode   = -not $Images
$faireImages = -not $Code

function Ssh-Exec([string]$cmd) {
  & ssh -i $CLE -o StrictHostKeyChecking=accept-new "root@$IP" $cmd
  if ($LASTEXITCODE -ne 0) { throw "Commande distante en echec (code $LASTEXITCODE)" }
}

# --- Controles ---------------------------------------------------------------
Write-Host "== Controles" -ForegroundColor Cyan
foreach ($o in @("ssh","scp","tar")) {
  if (-not (Get-Command $o -ErrorAction SilentlyContinue)) { throw "$o introuvable." }
}
if (-not (Test-Path $CLE)) { throw "Cle SSH introuvable : $CLE" }
if (-not (Test-Path (Join-Path $PROJET "site\orchestrateur.py"))) {
  throw "orchestrateur.py introuvable dans $PROJET\site"
}
icacls $CLE /inheritance:r /grant:r "$($env:USERNAME):(R)" | Out-Null
& ssh -i $CLE -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 "root@$IP" "true"
if ($LASTEXITCODE -ne 0) { throw "SSH impossible vers $IP" }
Write-Host "   ok - serveur joignable"

# --- Code --------------------------------------------------------------------
if ($faireCode) {
  Write-Host "== Code du moteur et orchestrateur" -ForegroundColor Cyan
  $tgz = Join-Path $env:TEMP "narwhal-code.tgz"
  if (Test-Path $tgz) { Remove-Item $tgz -Force }

  # Les dossiers ecrits par les tables vivent sur le serveur : on ne les envoie
  # pas, donc l'extraction ne peut pas les ecraser.
  $exclus = @(
    "--exclude=.git","--exclude=node_modules","--exclude=__pycache__",
    # Dossiers COMPILES par le launcher (.game, .game-src, et une copie par
    # table multijoueur). Ils sont bourres de LIENS SYMBOLIQUES crees sous WSL
    # (88 au dernier comptage) que le tar.exe de Windows ne sait pas lire :
    # « Cannot stat: Invalid argument », archive en echec, aucun deploiement
    # possible des qu'une partie a tourne. Ils n'ont de toute facon rien a faire
    # sur le serveur : ils sont gitignores, ils pointent vers des chemins
    # Windows, et le launcher les reconstruit a son demarrage.
    "--exclude=.game","--exclude=.game-src*",
    "--exclude=*.pyc","--exclude=.venv","--exclude=venv",
    # Les scans voyagent par l'etape « Images custom », jamais dans
    # l'archive de code. Sans pics-fr, oubliee jusqu'au 06/09/2026,
    # l'archive pesait 922 Mo au lieu de 62 : 870 Mo de scans francais
    # renvoyes a chaque deploiement alors qu'ils ne changent jamais.
    "--exclude=assets/pics","--exclude=assets/pics-fr",
    "--exclude=assets/pics-proxy",
    "--exclude=sauvegardes","--exclude=saves","--exclude=decks",
    "--exclude=campagnes","--exclude=statistiques","--exclude=achievements",
    "--exclude=replays","--exclude=logs",
    "--exclude=comptes.json","--exclude=*.db","--exclude=*.sqlite3"
  )
  & tar -czf $tgz -C $PROJET @exclus "Fusion/marvel-lcg-src" "site"
  if ($LASTEXITCODE -ne 0) { throw "Creation de l'archive en echec." }
  $mo = [math]::Round((Get-Item $tgz).Length / 1MB, 1)
  Write-Host "   archive : $mo Mo"

  & scp -i $CLE $tgz "root@${IP}:/tmp/narwhal-code.tgz"
  if ($LASTEXITCODE -ne 0) { throw "Envoi du code en echec." }
  Ssh-Exec "mkdir -p $DIST && tar -xzf /tmp/narwhal-code.tgz -C $DIST && rm -f /tmp/narwhal-code.tgz && chown -R narwhal:narwhal $DIST"
  Remove-Item $tgz -Force
  Write-Host "   code deploye"
}

# --- Images custom -----------------------------------------------------------
if ($faireImages -and (Test-Path $PICS)) {
  Write-Host "== Images custom" -ForegroundColor Cyan

  # Inventaire distant : chemin relatif et taille.
  $distant = @{}
  $lignes = & ssh -i $CLE "root@$IP" "cd $PICS_DIST 2>/dev/null && find . -type f -printf '%P|%s\n' || true"
  foreach ($l in $lignes) {
    if ($l -match '^(.*)\|(\d+)$') { $distant[$Matches[1]] = [int64]$Matches[2] }
  }
  Write-Host "   deja sur le serveur : $($distant.Count) fichiers"

  # Ce qui manque ou differe.
  $prefixe = (Resolve-Path $PICS).Path.TrimEnd('\') + '\'
  $aEnvoyer = @()
  $poids = 0
  foreach ($f in Get-ChildItem -Path $PICS -Recurse -File) {
    $rel = $f.FullName.Substring($prefixe.Length).Replace('\','/')
    if (-not $distant.ContainsKey($rel) -or $distant[$rel] -ne $f.Length) {
      $aEnvoyer += [pscustomobject]@{ Rel = $rel; Taille = $f.Length }
      $poids += $f.Length
    }
  }

  if ($aEnvoyer.Count -eq 0) {
    Write-Host "   rien a envoyer, tout est a jour"
  } else {
    $totalMo = [math]::Round($poids / 1MB, 1)
    Write-Host "   a envoyer : $($aEnvoyer.Count) images, $totalMo Mo"
    Ssh-Exec "mkdir -p $PICS_DIST"

    # Envoi par lots d'environ 100 Mo : une coupure ne perd qu'un lot.
    $lot = @(); $lotPoids = 0; $numero = 0
    $limite = 100MB

    function Envoyer-Lot($fichiers, $numero) {
      $liste = Join-Path $env:TEMP "narwhal-lot.txt"
      $tgz   = Join-Path $env:TEMP "narwhal-lot.tgz"
      [IO.File]::WriteAllLines($liste, ($fichiers | ForEach-Object { $_.Rel }), (New-Object Text.UTF8Encoding $false))
      & tar -czf $tgz -C $script:PICS -T $liste
      if ($LASTEXITCODE -ne 0) { throw "Creation du lot $numero en echec." }
      & scp -i $script:CLE $tgz "root@$($script:IP):/tmp/narwhal-lot.tgz"
      if ($LASTEXITCODE -ne 0) { throw "Envoi du lot $numero en echec." }
      & ssh -i $script:CLE "root@$($script:IP)" "tar -xzf /tmp/narwhal-lot.tgz -C $script:PICS_DIST && rm -f /tmp/narwhal-lot.tgz && chown -R narwhal:narwhal $script:PICS_DIST"
      if ($LASTEXITCODE -ne 0) { throw "Extraction du lot $numero en echec." }
      Remove-Item $liste, $tgz -Force -ErrorAction SilentlyContinue
    }

    foreach ($img in $aEnvoyer) {
      $lot += $img; $lotPoids += $img.Taille
      if ($lotPoids -ge $limite) {
        $numero++
        Write-Host "   lot $numero : $($lot.Count) images, $([math]::Round($lotPoids/1MB,1)) Mo"
        Envoyer-Lot $lot $numero
        $lot = @(); $lotPoids = 0
      }
    }
    if ($lot.Count -gt 0) {
      $numero++
      Write-Host "   lot $numero : $($lot.Count) images, $([math]::Round($lotPoids/1MB,1)) Mo"
      Envoyer-Lot $lot $numero
    }
    Write-Host "   images deployees"
  }
}

# --- Python, redemarrage, verification ---------------------------------------
if ($faireCode) {
  Write-Host "== Environnement Python 3.10 et redemarrage" -ForegroundColor Cyan
  $distant = @"
set -e
[ -x $DIST/venv310/bin/python ] || python3.10 -m venv $DIST/venv310
$DIST/venv310/bin/python --version
for req in $DIST/Fusion/marvel-lcg-src/requirements.txt $DIST/site/requirements.txt; do
  [ -f "`$req" ] && $DIST/venv310/bin/pip install -q --upgrade -r "`$req" || true
done
chown -R narwhal:narwhal $DIST
systemctl restart narwhal
sleep 3
systemctl is-active narwhal
"@
  Ssh-Exec $distant

  Write-Host "== Sauvegarde des comptes rapatriee" -ForegroundColor Cyan
  $dossier = Join-Path $PROJET "sauvegardes-serveur"
  New-Item -ItemType Directory -Force -Path $dossier | Out-Null
  & ssh -i $CLE "root@$IP" "sudo -u narwhal RACINE=$DIST /usr/local/bin/narwhal-sauvegarde >/dev/null 2>&1 || true"
  $dest = Join-Path $dossier ("comptes-" + (Get-Date -Format "yyyy-MM-dd") + ".tar.gz")
  & scp -i $CLE "root@${IP}:/var/backups/narwhal/comptes-dernier.tar.gz" $dest 2>$null
  if (Test-Path $dest) { Write-Host "   $dest" } else { Write-Host "   (pas encore de sauvegarde sur le serveur)" }

  Write-Host "== Verification" -ForegroundColor Cyan
  try {
    $r = Invoke-WebRequest -Uri "https://$DOMAINE/" -UseBasicParsing -TimeoutSec 20
    Write-Host "   https://$DOMAINE/ -> HTTP $($r.StatusCode)" -ForegroundColor Green
  } catch {
    Write-Host "   le site ne repond pas encore : $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "   journaux : ssh -i `"$CLE`" root@$IP 'journalctl -u narwhal -n 50'"
  }
}

Write-Host ""
Write-Host "Termine." -ForegroundColor Green
