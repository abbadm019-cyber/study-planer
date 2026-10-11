import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FICHIER_SAUVEGARDE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "taches.json"
)

COULEUR_FOND = "#F4F7FB"
COULEUR_BLEU = "#2563EB"
COULEUR_BLEU_FONCE = "#1E3A8A"
COULEUR_BLEU_CLAIR = "#DBEAFE"
COULEUR_VERT = "#16A34A"
COULEUR_ROUGE = "#DC2626"
COULEUR_BLANC = "#FFFFFF"
COULEUR_TEXTE = "#1F2937"
COULEUR_GRIS = "#64748B"
COULEUR_JAUNE = "#F59E0B"


def charger_taches():
    if os.path.exists(FICHIER_SAUVEGARDE):
        try:
            with open(FICHIER_SAUVEGARDE, "r", encoding="utf-8") as fichier:
                return json.load(fichier)
        except:
            return []
    return []


def sauvegarder_taches():
    with open(FICHIER_SAUVEGARDE, "w", encoding="utf-8") as fichier:
        json.dump(taches, fichier, ensure_ascii=False, indent=4)


def ajouter_tache():
    matiere = entree_matiere.get().strip()
    description = entree_description.get().strip()
    duree = entree_duree.get().strip()

    if matiere == "":
        messagebox.showwarning(
            "Information manquante",
            "Veuillez entrer une matière."
        )
        return

    if description == "":
        messagebox.showwarning(
            "Information manquante",
            "Veuillez entrer une tâche."
        )
        return

    if duree == "":
        messagebox.showwarning(
            "Information manquante",
            "Veuillez entrer une durée."
        )
        return

    if not duree.isdigit():
        messagebox.showwarning(
            "Durée incorrecte",
            "La durée doit être un nombre."
        )
        return

    nouvelle_tache = {
        "matiere": matiere,
        "description": description,
        "duree": duree,
        "terminee": False
    }

    taches.append(nouvelle_tache)
    sauvegarder_taches()
    afficher_taches()

    entree_matiere.delete(0, tk.END)
    entree_description.delete(0, tk.END)
    entree_duree.delete(0, tk.END)


def afficher_taches():
    liste.delete(*liste.get_children())

    for numero, tache in enumerate(taches):
        statut = "✓ Terminée" if tache["terminee"] else "○ À faire"

        liste.insert(
            "",
            tk.END,
            iid=str(numero),
            values=(
                tache["matiere"],
                tache["description"],
                tache["duree"] + " min",
                statut
            )
        )

    mettre_a_jour_statistiques()


def terminer_tache():
    selection = liste.selection()

    if not selection:
        messagebox.showwarning(
            "Aucune sélection",
            "Sélectionnez une tâche."
        )
        return

    numero = int(selection[0])
    taches[numero]["terminee"] = True

    sauvegarder_taches()
    afficher_taches()


def supprimer_tache():
    selection = liste.selection()

    if not selection:
        messagebox.showwarning(
            "Aucune sélection",
            "Sélectionnez une tâche."
        )
        return

    numero = int(selection[0])

    confirmation = messagebox.askyesno(
        "Confirmation",
        "Voulez-vous vraiment supprimer cette tâche ?"
    )

    if confirmation:
        taches.pop(numero)
        sauvegarder_taches()
        afficher_taches()


def mettre_a_jour_statistiques():
    total = len(taches)
    terminees = 0
    temps_total = 0

    for tache in taches:
        if tache["terminee"]:
            terminees += 1

        temps_total += int(tache["duree"])

    if total > 0:
        progression = int((terminees / total) * 100)
    else:
        progression = 0

    texte_total.config(text=str(total))
    texte_terminees.config(text=str(terminees))
    texte_temps.config(text=f"{temps_total} min")
    texte_progression.config(text=f"{progression}%")


def creer_statistique(parent, titre, couleur):
    cadre = tk.Frame(
        parent,
        bg=COULEUR_BLANC,
        padx=20,
        pady=12,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )

    cadre.pack(
        side="left",
        expand=True,
        fill="x",
        padx=6
    )

    label_titre = tk.Label(
        cadre,
        text=titre,
        font=("Segoe UI", 10),
        bg=COULEUR_BLANC,
        fg=COULEUR_GRIS
    )

    label_titre.pack()

    label_valeur = tk.Label(
        cadre,
        text="0",
        font=("Segoe UI", 20, "bold"),
        bg=COULEUR_BLANC,
        fg=couleur
    )

    label_valeur.pack()

    return label_valeur


fenetre = tk.Tk()

fenetre.title("StudyPlanner")
fenetre.geometry("1000x700")
fenetre.minsize(850, 600)
fenetre.configure(bg=COULEUR_FOND)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=COULEUR_BLANC,
    foreground=COULEUR_TEXTE,
    rowheight=38,
    fieldbackground=COULEUR_BLANC,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background=COULEUR_BLEU_FONCE,
    foreground=COULEUR_BLANC,
    font=("Segoe UI", 10, "bold"),
    padding=10
)

style.map(
    "Treeview",
    background=[("selected", COULEUR_BLEU_CLAIR)],
    foreground=[("selected", COULEUR_TEXTE)]
)

entete = tk.Frame(
    fenetre,
    bg=COULEUR_BLEU_FONCE,
    height=120
)

entete.pack(fill="x")
entete.pack_propagate(False)

titre = tk.Label(
    entete,
    text="📚 StudyPlanner",
    font=("Segoe UI", 28, "bold"),
    bg=COULEUR_BLEU_FONCE,
    fg=COULEUR_BLANC
)

titre.pack(pady=(20, 2))

sous_titre = tk.Label(
    entete,
    text="Organise tes révisions • Suis ta progression • Atteins tes objectifs",
    font=("Segoe UI", 11),
    bg=COULEUR_BLEU_FONCE,
    fg="#DBEAFE"
)

sous_titre.pack()

cadre_stats = tk.Frame(
    fenetre,
    bg=COULEUR_FOND
)

cadre_stats.pack(
    fill="x",
    padx=30,
    pady=20
)

texte_total = creer_statistique(
    cadre_stats,
    "📚 Tâches",
    COULEUR_BLEU
)

texte_terminees = creer_statistique(
    cadre_stats,
    "✓ Terminées",
    COULEUR_VERT
)

texte_temps = creer_statistique(
    cadre_stats,
    "⏱ Temps prévu",
    COULEUR_JAUNE
)

texte_progression = creer_statistique(
    cadre_stats,
    "📈 Progression",
    COULEUR_BLEU_FONCE
)

cadre_ajout = tk.Frame(
    fenetre,
    bg=COULEUR_BLANC,
    padx=20,
    pady=18,
    highlightbackground="#E2E8F0",
    highlightthickness=1
)

cadre_ajout.pack(
    fill="x",
    padx=30,
    pady=5
)

label_formulaire = tk.Label(
    cadre_ajout,
    text="➕ Ajouter une nouvelle tâche",
    font=("Segoe UI", 13, "bold"),
    bg=COULEUR_BLANC,
    fg=COULEUR_TEXTE
)

label_formulaire.grid(
    row=0,
    column=0,
    columnspan=6,
    sticky="w",
    pady=(0, 12)
)

tk.Label(
    cadre_ajout,
    text="Matière",
    font=("Segoe UI", 9, "bold"),
    bg=COULEUR_BLANC,
    fg=COULEUR_GRIS
).grid(
    row=1,
    column=0,
    padx=5,
    sticky="w"
)

entree_matiere = tk.Entry(
    cadre_ajout,
    width=20,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

entree_matiere.grid(
    row=2,
    column=0,
    padx=5,
    pady=5
)

tk.Label(
    cadre_ajout,
    text="Tâche",
    font=("Segoe UI", 9, "bold"),
    bg=COULEUR_BLANC,
    fg=COULEUR_GRIS
).grid(
    row=1,
    column=1,
    padx=5,
    sticky="w"
)

entree_description = tk.Entry(
    cadre_ajout,
    width=35,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

entree_description.grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)

tk.Label(
    cadre_ajout,
    text="Durée (minutes)",
    font=("Segoe UI", 9, "bold"),
    bg=COULEUR_BLANC,
    fg=COULEUR_GRIS
).grid(
    row=1,
    column=2,
    padx=5,
    sticky="w"
)

entree_duree = tk.Entry(
    cadre_ajout,
    width=15,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

entree_duree.grid(
    row=2,
    column=2,
    padx=5,
    pady=5
)

bouton_ajouter = tk.Button(
    cadre_ajout,
    text="＋ Ajouter",
    command=ajouter_tache,
    bg=COULEUR_BLEU,
    fg=COULEUR_BLANC,
    activebackground=COULEUR_BLEU_FONCE,
    activeforeground=COULEUR_BLANC,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=20,
    pady=7,
    cursor="hand2"
)

bouton_ajouter.grid(
    row=2,
    column=3,
    padx=10
)

cadre_liste = tk.Frame(
    fenetre,
    bg=COULEUR_FOND
)

cadre_liste.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=15
)

colonnes = (
    "matiere",
    "description",
    "duree",
    "statut"
)

liste = ttk.Treeview(
    cadre_liste,
    columns=colonnes,
    show="headings"
)

liste.heading(
    "matiere",
    text="📚 Matière"
)

liste.heading(
    "description",
    text="📝 Tâche"
)

liste.heading(
    "duree",
    text="⏱ Durée"
)

liste.heading(
    "statut",
    text="📌 Statut"
)

liste.column(
    "matiere",
    width=160,
    anchor="center"
)

liste.column(
    "description",
    width=400,
    anchor="w"
)

liste.column(
    "duree",
    width=120,
    anchor="center"
)

liste.column(
    "statut",
    width=160,
    anchor="center"
)

liste.pack(
    fill="both",
    expand=True
)

cadre_boutons = tk.Frame(
    fenetre,
    bg=COULEUR_FOND
)

cadre_boutons.pack(
    pady=5
)

bouton_termine = tk.Button(
    cadre_boutons,
    text="✓ Marquer comme terminée",
    command=terminer_tache,
    bg=COULEUR_VERT,
    fg=COULEUR_BLANC,
    activebackground="#15803D",
    activeforeground=COULEUR_BLANC,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=15,
    pady=8,
    cursor="hand2"
)

bouton_termine.pack(
    side="left",
    padx=5
)

bouton_supprimer = tk.Button(
    cadre_boutons,
    text="✕ Supprimer",
    command=supprimer_tache,
    bg=COULEUR_ROUGE,
    fg=COULEUR_BLANC,
    activebackground="#B91C1C",
    activeforeground=COULEUR_BLANC,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=15,
    pady=8,
    cursor="hand2"
)

bouton_supprimer.pack(
    side="left",
    padx=5
)

taches = charger_taches()

afficher_taches()

fenetre.mainloop()