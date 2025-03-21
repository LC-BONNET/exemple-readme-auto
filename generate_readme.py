import os
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

def generate_readme():
    current_date = datetime.now().strftime('%Y-%m-%d')
    structure = generate_tree_structure()

    content = (
f"# 📁 {GITHUB_REPO}\n\n"
f"![Mise à jour automatique du README](https://github.com/{GITHUB_USER}/{GITHUB_REPO}/actions/workflows/update-readme.yml/badge.svg)\n\n"
f"> 🗓️ Généré automatiquement le {current_date}\n\n"
f"![Stars](https://img.shields.io/github/stars/{GITHUB_USER}/{GITHUB_REPO}?style=social)\n"
f"![Forks](https://img.shields.io/github/forks/{GITHUB_USER}/{GITHUB_REPO}?style=social)\n"
f"![Issues](https://img.shields.io/github/issues/{GITHUB_USER}/{GITHUB_REPO})\n"
f"![GitHub contributors](https://img.shields.io/github/contributors/{GITHUB_USER}/{GITHUB_REPO})\n\n"
f"![Dernière mise à jour](https://img.shields.io/github/last-commit/{GITHUB_USER}/{GITHUB_REPO})\n\n"
"---\n\n"
"## 🧭 Sommaire\n\n"
"- [📂 Structure du projet](#-structure-du-projet)\n"
"- [📝 Description des fichiers](#-description-des-fichiers)\n"
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
"## 🚀 Utilisation\n\n"
"Ajoutez ici les instructions pour lancer ou tester le projet.\n\n"
"---\n\n"
"## ✅ TODO\n\n"
"- [ ] Ajouter une documentation plus détaillée\n"
"- [ ] Créer des tests unitaires\n"
"- [ ] Ajouter un fichier de configuration\n\n"
"---\n\n"
"## 📄 Licence\n\n"
"Ajoutez ici les détails de la licence du projet (MIT, GPL, etc.)\n\n"
"---\n\n"
"*Ce fichier README a été généré automatiquement avec 💻 Python.* 🛠️\n"
    )

    with open("README.md", "w") as f:
        f.write(content)

    print("✅ README.md généré avec succès.")

if __name__ == "__main__":
    generate_readme()
