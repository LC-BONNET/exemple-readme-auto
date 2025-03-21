import os
import requests
from datetime import datetime

# Configuration
GITHUB_USER = "LC-BONNET"
GITHUB_REPO = os.path.basename(os.getcwd())

DESCRIPTIONS = {
    "main.py": "Point d'entrée principal du programme.",
    "README.md": "Documentation principale du dépôt.",
    "requirements.txt": "Liste des dépendances Python.",
    "setup.py": "Script d'installation du paquet.",
    ".gitignore": "Fichiers ignorés par Git.",
}

# 🔹 Fonction pour récupérer les 5 derniers commits du repo
def get_latest_commits(user, repo, count=5):
    url = f"https://api.github.com/repos/{user}/{repo}/commits"
    response = requests.get(url)
    if response.status_code == 200:
        commits = response.json()[:count]
        return [f"- {commit['commit']['message']} ({commit['sha'][:7]})" for commit in commits]
    return ["Aucun commit trouvé."]

# 🔹 Fonction pour détecter la licence du projet
def detect_license():
    if os.path.exists("LICENSE"):
        with open("LICENSE", "r", encoding="utf-8") as f:
            return f.readline().strip()
    return "Aucune licence détectée."

# 🔹 Fonction pour récupérer les contributeurs
def get_contributors(user, repo):
    url = f"https://api.github.com/repos/{user}/{repo}/contributors"
    response = requests.get(url)
    if response.status_code == 200:
        contributors = response.json()
        return [f"- [{c['login']}]({c['html_url']}) ({c['contributions']} contributions)" for c in contributors]
    return ["Aucun contributeur trouvé."]

# 🔹 Fonction pour générer l'arborescence du projet
def generate_tree_structure(path='.', prefix=''):
    tree = ''
    files = sorted(os.listdir(path))
    files = [f for f in files if f != '.git' and not f.startswith('.')]

    for i, file in enumerate(files):
        full_path = os.path.join(path, file)
        connector = '└── ' if i == len(files) - 1 else '├── '
        tree += f"{prefix}{connector}{file}"
        
        if file in DESCRIPTIONS:
            tree += f"  - {DESCRIPTIONS[file]}"
        tree += "\n"

        if os.path.isdir(full_path):
            extension = '    ' if i == len(files) - 1 else '│   '
            tree += generate_tree_structure(full_path, prefix + extension)
    return tree

# 🔹 Fonction principale pour générer le README
def generate_readme():
    current_date = datetime.now().strftime('%Y-%m-%d')
    structure = generate_tree_structure()
    latest_commits = get_latest_commits(GITHUB_USER, GITHUB_REPO)
    license_text = detect_license()
    contributors = get_contributors(GITHUB_USER, GITHUB_REPO)

    content = (
f"# 📁 {GITHUB_REPO}\n\n"
f"![Mise à jour automatique du README](https://github.com/{GITHUB_USER}/{GITHUB_REPO}/actions/workflows/update-readme.yml/badge.svg)\n\n"
f"> 🗓️ Généré automatiquement le {current_date}\n\n"
f"![Stars](https://img.shields.io/github/stars/{GITHUB_USER}/{GITHUB_REPO}?style=social)\n"
f"![Forks](https://img.shields.io/github/forks/{GITHUB_USER}/{GITHUB_REPO}?style=social)\n"
f"![Issues](https://img.shields.io/github/issues/{GITHUB_USER}/{GITHUB_REPO})\n"
f"![GitHub contributors](https://img.shields.io/github/contributors/{GITHUB_USER}/{GITHUB_REPO})\n"
f"![Dernière mise à jour](https://img.shields.io/github/last-commit/{GITHUB_USER}/{GITHUB_REPO})\n"
f"![Langage principal](https://img.shields.io/github/languages/top/{GITHUB_USER}/{GITHUB_REPO})\n"
f"![Langages utilisés](https://img.shields.io/github/languages/count/{GITHUB_USER}/{GITHUB_REPO})\n\n"
"---\n\n"
"## 🧭 Sommaire\n\n"
"- [📂 Structure du projet](#-structure-du-projet)\n"
"- [📝 Description des fichiers](#-description-des-fichiers)\n"
"- [📜 Changelog](#-changelog)\n"
"- [👥 Contributeurs](#-contributeurs)\n"
"- [🚀 Utilisation](#-utilisation)\n"
"- [✅ TODO](#-todo)\n"
"- [📄 Licence](#-licence)\n\n"
"---\n\n"
"## 📂 Structure du projet\n"
"```\n"
f"{structure}"
"```\n\n"
"---\n\n"
"## 📝 Description des fichiers\n\n"
"| Fichier | Description |\n"
"|--------|-------------|\n"
)

    for filename, desc in DESCRIPTIONS.items():
        if os.path.exists(filename):
            content += f"| `{filename}` | {desc} |\n"

    content += (
"\n---\n\n"
"## 📜 Changelog\n\n"
"Voici les dernières mises à jour du projet :\n\n"
+ "\n".join(latest_commits) + "\n\n"
"---\n\n"
"## 👥 Contributeurs\n\n"
"Merci aux contributeurs du projet :\n\n"
+ "\n".join(contributors) + "\n\n"
"---\n\n"
"## 🚀 Utilisation\n\n"
"Ajoutez ici les instructions pour lancer ou tester le projet.\n\n"
"---\n\n"
"## ✅ TODO\n\n"
"- [ ] Ajouter une documentation plus détaillée\n"
"- [ ] Créer des tests unitaires\n"
"- [ ] Ajouter un fichier de configuration\n\n"
"---\n\n"
"## 📄 Licence\n\n"
f"{license_text}\n\n"
"---\n\n"
"*Ce fichier README a été généré automatiquement avec 💻 Python.* 🛠️\n"
    )

    with open("README.md", "w") as f:
        f.write(content)

    print("✅ README.md généré avec succès.")

if __name__ == "__main__":
    generate_readme()
