import streamlit as st
import pandas as pd
import re
import requests

from rdkit import Chem
from rdkit.Chem import Draw, Descriptors, rdMolDescriptors, AllChem
from io import BytesIO
from PIL import Image
import py3Dmol
import streamlit.components.v1 as components

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------
st.set_page_config(
    page_title="Cheminformatics | Molecular Workspace",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #07111f, #0b1728, #101f33); color: #e8f0ff; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; }
.hero { padding: 30px; border-radius: 22px; background: linear-gradient(120deg, #14243a, #1b3150); border: 1px solid #294563; box-shadow: 0 10px 35px rgba(0,0,0,.25); margin-bottom: 25px; }
.eyebrow { color: #52e0c4; font-size: 12px; text-transform: uppercase; letter-spacing: 3px; font-weight: bold; }
.hero h1 { font-size: 42px; color: #fff; margin-bottom: 10px; }
.hero p { color: #c2d2e8; font-size: 16px; }
.student-card, .section-card { background: #12243a; padding: 18px; border-radius: 14px; border: 1px solid #294563; margin: 12px 0; }
.small-label { color: #52e0c4; font-size: 12px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
div[data-testid="stMetric"] { background: #12243a; border: 1px solid #294563; padding: 15px; border-radius: 14px; }
h2, h3 { color: #fff; }
.stButton > button { border-radius: 10px; border: 1px solid #52e0c4; background: #17374a; color: white; font-weight: bold; }
.stButton > button:hover { background: #24576a; color: white; border-color: #52e0c4; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# MOLECULE EXAMPLES
# -----------------------------------
MOLECULES = {
    "Water": "O",
    "Methane": "C",
    "Ammonia": "N",
    "Carbon dioxide": "O=C=O",
    "Oxygen": "O=O",
    "Hydrogen peroxide": "OO",
    "Ethanol": "CCO",
    "Acetic acid": "CC(=O)O",
    "Glucose": "C(C1C(C(C(C(O1)O)O)O)O)O",
    "Benzene": "c1ccccc1",
    "Caffeine": "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
    "Aspirin": "CC(=O)Oc1ccccc1C(=O)O",
    "Paracetamol": "CC(=O)NC1=CC=C(C=C1)O",
    "Ibuprofen": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
    "Nicotine": "CN1CCC[C@H]1c2cccnc2",
    "Vitamin C": "O=C1OC(C(O)CO)C(O)=C1O",
    "Lactic acid": "CC(O)C(=O)O",
    "Urea": "NC(=O)N",
    "Sodium acetate": "CC(=O)[O-].[Na+]",
}

# -----------------------------------
# HELPERS
# -----------------------------------
def fetch_smiles_from_pubchem(name: str):
    """Try PubChem by name; returns a SMILES string or None."""
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{requests.utils.quote(name)}/property/CanonicalSMILES,ConnectivitySMILES/JSON"
        response = requests.get(url, timeout=7)
        if response.ok:
            properties = response.json().get("PropertyTable", {}).get("Properties", [])
            if properties:
                item = properties[0]
                return item.get("ConnectivitySMILES") or item.get("CanonicalSMILES")
    except (requests.RequestException, ValueError, KeyError):
        return None
    return None


def make_molecule(smiles: str):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return mol


def make_3d_molecule(mol):
    """Create a hydrogenated molecule with a 3D conformer."""
    mol3d = Chem.AddHs(Chem.Mol(mol))
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    result = AllChem.EmbedMolecule(mol3d, params)
    if result != 0:
        # Try a second embedding method for molecules that are difficult to embed.
        result = AllChem.EmbedMolecule(mol3d, randomSeed=7)
    if result != 0:
        return None
    try:
        if AllChem.MMFFHasAllMoleculeParams(mol3d):
            AllChem.MMFFOptimizeMolecule(mol3d, maxIters=150)
        else:
            AllChem.UFFOptimizeMolecule(mol3d, maxIters=150)
    except Exception:
        pass
    return mol3d


def show_3d_viewer(mol3d, height=470):
    """Render a py3Dmol viewer in Streamlit."""
    mol_block = Chem.MolToMolBlock(mol3d)
    viewer = py3Dmol.view(width=800, height=height)
    viewer.addModel(mol_block, "mol")
    viewer.setStyle({"stick": {"radius": 0.18}, "sphere": {"scale": 0.23}})
    viewer.setBackgroundColor("0x0b1728")
    viewer.zoomTo()
    components.html(viewer._make_html(), height=height + 30, scrolling=False)


def hero(title, subtitle, eyebrow="Molecular intelligence workspace"):
    st.markdown(f"""
    <div class="hero">
      <div class="eyebrow">{eyebrow}</div>
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------
st.sidebar.markdown("# ⚛️ ChemLab")
st.sidebar.caption("Molecular Intelligence Workspace")
st.sidebar.divider()

pages = ["Home", "Molecular Explorer (2D & 3D)", "Periodic Table", "Molecular Calculator", "About"]
page = st.sidebar.radio("NAVIGATION", pages, key="navigation_page")

st.sidebar.divider()
st.sidebar.markdown("### Student Profile")
st.sidebar.write("**Name:** RATHIESH D")
st.sidebar.write("**Register No.:** RE2611026050338")
st.sidebar.caption("Cheminformatics Project")

# -----------------------------------
# HOME PAGE
# -----------------------------------
if page == "Home":
    hero("⚛️ Cheminformatics", "Discover compounds and elements with interactive 2D and 3D molecular views.")
    st.markdown("""
    <div class="student-card">
      <p><b>Student Name:</b> RATHIESH D</p>
      <p><b>Registration Number:</b> RE2611026050338</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Explore Your Chemistry Workspace")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="section-card"><div class="small-label">MODULE 01</div><h3>🧬 Molecular Explorer</h3><p>Search molecules and inspect 2D structures and interactive 3D models.</p></div>', unsafe_allow_html=True)
        if st.button("Open Molecular Explorer", use_container_width=True):
            st.session_state["navigation_page"] = "Molecular Explorer (2D & 3D)"
            st.rerun()
    with col2:
        st.markdown('<div class="section-card"><div class="small-label">MODULE 02</div><h3>🧪 Periodic Table</h3><p>Explore element symbols, atomic numbers, and atomic masses.</p></div>', unsafe_allow_html=True)
        if st.button("Explore Elements", use_container_width=True):
            st.session_state["navigation_page"] = "Periodic Table"
            st.rerun()
    with col3:
        st.markdown('<div class="section-card"><div class="small-label">MODULE 03</div><h3>🧮 Molecular Calculator</h3><p>Calculate molecular formula and molecular mass.</p></div>', unsafe_allow_html=True)
        if st.button("Calculate Mass", use_container_width=True):
            st.session_state["navigation_page"] = "Molecular Calculator"
            st.rerun()

    st.subheader("Workspace Overview")
    a, b, c = st.columns(3)
    a.metric("Project", "Cheminformatics")
    b.metric("Core Modules", "3")
    c.metric("Molecular Views", "2D + 3D")
    st.markdown('<div class="section-card"><h3>🎯 Project Objective</h3><p>This project introduces computational chemistry through molecule visualization, element exploration, and molecular calculations.</p></div>', unsafe_allow_html=True)

# -----------------------------------
# MOLECULAR EXPLORER
# -----------------------------------
elif page == "Molecular Explorer (2D & 3D)":
    hero("🧬 Molecular Explorer", "Search a molecule by name or choose an example to view its 2D structure and interactive 3D model.", "2D + 3D molecular workspace")

    method = st.radio("Choose how to find a molecule", ["Choose an example", "Search by name", "Enter SMILES"], horizontal=True)
    selected_name = None
    smiles = None

    if method == "Choose an example":
        selected_name = st.selectbox("Example molecules", list(MOLECULES.keys()), index=list(MOLECULES.keys()).index("Aspirin"))
        smiles = MOLECULES[selected_name]
    elif method == "Search by name":
        query = st.text_input("Molecule name", placeholder="Try Aspirin, Caffeine, Ethanol, or Glucose")
        if query.strip():
            match = next((name for name in MOLECULES if name.casefold() == query.strip().casefold()), None)
            if match:
                selected_name = match
                smiles = MOLECULES[match]
            else:
                with st.spinner("Searching PubChem for this molecule..."):
                    smiles = fetch_smiles_from_pubchem(query.strip())
                if smiles:
                    selected_name = query.strip().title()
                    st.success(f"Found {selected_name} in PubChem.")
                else:
                    st.warning("No match found. Check the spelling, choose an example, or enter a SMILES string.")
    else:
        smiles = st.text_input("SMILES string", placeholder="Example: CCO")
        selected_name = "Custom molecule"

    if smiles:
        mol = make_molecule(smiles)
        if mol is None:
            st.error("This molecule could not be interpreted. Please check the molecule name or SMILES string.")
        else:
            canonical_smiles = Chem.MolToSmiles(mol)
            formula = rdMolDescriptors.CalcMolFormula(mol)
            mass = Descriptors.MolWt(mol)
            st.markdown(f"### {selected_name or 'Molecule'}")
            m1, m2, m3 = st.columns(3)
            m1.metric("Molecular Formula", formula)
            m2.metric("Molecular Mass", f"{mass:.3f} g/mol")
            m3.metric("Heavy Atoms", str(mol.GetNumHeavyAtoms()))
            with st.expander("Canonical SMILES"):
                st.code(canonical_smiles)

            left, right = st.columns(2)
            with left:
                st.markdown("#### 🧪 2D Molecular Structure")
                try:
                    image = Draw.MolToImage(mol, size=(650, 450), kekulize=True, wedgeBonds=True)
                    st.image(image, caption=f"2D structure of {selected_name or 'molecule'}", use_container_width=True)
                except Exception as exc:
                    st.error(f"Could not draw the 2D structure: {exc}")
            with right:
                st.markdown("#### 🧬 Interactive 3D Molecular Structure")
                with st.spinner("Building the 3D molecular model..."):
                    mol3d = make_3d_molecule(mol)
                if mol3d is None:
                    st.warning("A 3D model could not be generated for this molecule. Try another example.")
                else:
                    try:
                        show_3d_viewer(mol3d)
                        st.caption("Drag to rotate • Scroll to zoom • Use two fingers or right-drag to move the view. The 3D model is generated locally from the molecule structure.")
                    except Exception as exc:
                        st.error("The 3D viewer could not load. Please refresh the app and try again.")
                        st.caption(f"Technical detail: {exc}")

            st.info("The molecule search uses a built-in example list first. For other names, it tries PubChem online; an internet connection is required for that lookup.")
    else:
        st.info("Choose an example, search for a molecule name, or enter a SMILES string to display its 2D and 3D structures.")

# -----------------------------------
# PERIODIC TABLE PAGE
# -----------------------------------
elif page == "Periodic Table":
    hero("🧪 Periodic Table", "Search and explore common chemical elements.", "Chemical element explorer")
    elements = [
        {"Atomic Number": 1, "Symbol": "H", "Element": "Hydrogen", "Atomic Mass": 1.008},
        {"Atomic Number": 2, "Symbol": "He", "Element": "Helium", "Atomic Mass": 4.0026},
        {"Atomic Number": 3, "Symbol": "Li", "Element": "Lithium", "Atomic Mass": 6.94},
        {"Atomic Number": 4, "Symbol": "Be", "Element": "Beryllium", "Atomic Mass": 9.0122},
        {"Atomic Number": 5, "Symbol": "B", "Element": "Boron", "Atomic Mass": 10.81},
        {"Atomic Number": 6, "Symbol": "C", "Element": "Carbon", "Atomic Mass": 12.011},
        {"Atomic Number": 7, "Symbol": "N", "Element": "Nitrogen", "Atomic Mass": 14.007},
        {"Atomic Number": 8, "Symbol": "O", "Element": "Oxygen", "Atomic Mass": 15.999},
        {"Atomic Number": 9, "Symbol": "F", "Element": "Fluorine", "Atomic Mass": 18.998},
        {"Atomic Number": 10, "Symbol": "Ne", "Element": "Neon", "Atomic Mass": 20.180},
        {"Atomic Number": 11, "Symbol": "Na", "Element": "Sodium", "Atomic Mass": 22.990},
        {"Atomic Number": 12, "Symbol": "Mg", "Element": "Magnesium", "Atomic Mass": 24.305},
        {"Atomic Number": 13, "Symbol": "Al", "Element": "Aluminium", "Atomic Mass": 26.982},
        {"Atomic Number": 14, "Symbol": "Si", "Element": "Silicon", "Atomic Mass": 28.085},
        {"Atomic Number": 15, "Symbol": "P", "Element": "Phosphorus", "Atomic Mass": 30.974},
        {"Atomic Number": 16, "Symbol": "S", "Element": "Sulfur", "Atomic Mass": 32.06},
        {"Atomic Number": 17, "Symbol": "Cl", "Element": "Chlorine", "Atomic Mass": 35.45},
        {"Atomic Number": 18, "Symbol": "Ar", "Element": "Argon", "Atomic Mass": 39.948},
        {"Atomic Number": 19, "Symbol": "K", "Element": "Potassium", "Atomic Mass": 39.098},
        {"Atomic Number": 20, "Symbol": "Ca", "Element": "Calcium", "Atomic Mass": 40.078},
    ]
    df = pd.DataFrame(elements)
    search = st.text_input("Search by element name or symbol", placeholder="Example: Carbon or C")
    if search:
        df = df[df["Element"].str.contains(search, case=False, na=False) | df["Symbol"].str.contains(search, case=False, na=False)]
    st.dataframe(df, use_container_width=True, hide_index=True)
    selected_symbol = st.selectbox("Choose an element for details", [item["Symbol"] for item in elements])
    selected = next(item for item in elements if item["Symbol"] == selected_symbol)
    st.markdown(f"""
    <div class="section-card"><div class="small-label">ELEMENT DETAILS</div><h1>{selected['Symbol']}</h1><h3>{selected['Element']}</h3><p>Atomic Number: {selected['Atomic Number']}</p><p>Standard Atomic Mass: {selected['Atomic Mass']}</p></div>
    """, unsafe_allow_html=True)

# -----------------------------------
# MOLECULAR CALCULATOR PAGE
# -----------------------------------
elif page == "Molecular Calculator":
    hero("🧮 Molecular Calculator", "Calculate molecular formula and molecular mass from a SMILES string or formula.", "Molecular analysis tools")
    calc_mode = st.radio("Calculation type", ["Calculate from formula", "Calculate from SMILES"], horizontal=True)
    if calc_mode == "Calculate from SMILES":
        calc_smiles = st.text_input("SMILES string", placeholder="Example: CCO")
        if calc_smiles:
            calc_mol = Chem.MolFromSmiles(calc_smiles)
            if calc_mol is None:
                st.error("Invalid SMILES string. Please check it and try again.")
            else:
                st.metric("Molecular Formula", rdMolDescriptors.CalcMolFormula(calc_mol))
                st.metric("Molecular Mass", f"{Descriptors.MolWt(calc_mol):.4f} g/mol")
    else:
        st.info("Enter a formula using element symbols and numbers, such as H2O, CO2, NaCl, or C6H12O6. Parentheses are not supported in this formula mode.")
        atomic_masses = {
            "H": 1.008, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81,
            "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
            "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974,
            "S": 32.06, "Cl": 35.45, "Ar": 39.948, "K": 39.098, "Ca": 40.078,
            "Fe": 55.845, "Cu": 63.546, "Zn": 65.38, "Ag": 107.868, "I": 126.904,
            "Ba": 137.327, "Au": 196.967, "Hg": 200.592, "Pb": 207.2,
        }
        formula = st.text_input("Chemical Formula", placeholder="Example: H2O", key="formula_input")
        if st.button("Calculate Molecular Mass", type="primary"):
            if not formula.strip():
                st.warning("Please enter a chemical formula.")
            else:
                tokens = re.findall(r"[A-Z][a-z]?|[0-9]+", formula.strip())
                if "".join(tokens) != formula.strip() or not tokens:
                    st.error("Invalid formula. Use element symbols and numbers only, without spaces or parentheses.")
                else:
                    mass = 0.0
                    composition = {}
                    i = 0
                    valid = True
                    while i < len(tokens):
                        symbol = tokens[i]
                        if symbol not in atomic_masses:
                            st.error(f"Atomic mass data is unavailable for {symbol}.")
                            valid = False
                            break
                        count = 1
                        if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                            count = int(tokens[i + 1])
                            i += 1
                        if count <= 0:
                            st.error("Atom counts must be greater than zero.")
                            valid = False
                            break
                        mass += atomic_masses[symbol] * count
                        composition[symbol] = composition.get(symbol, 0) + count
                        i += 1
                    if valid:
                        st.success("Calculation completed successfully!")
                        c1, c2 = st.columns(2)
                        c1.metric("Molecular Mass", f"{mass:.4f} g/mol")
                        c2.metric("Unique Elements", str(len(composition)))
                        st.subheader("Element Composition")
                        result_df = pd.DataFrame([{"Element": symbol, "Atom Count": count, "Atomic Mass": atomic_masses[symbol], "Contribution (g/mol)": atomic_masses[symbol] * count} for symbol, count in composition.items()])
                        st.dataframe(result_df, use_container_width=True, hide_index=True)

# -----------------------------------
# ABOUT PAGE
# -----------------------------------
elif page == "About":
    hero("📘 About Cheminformatics", "Connecting chemistry and computational science.", "Project information")
    st.subheader("What is Cheminformatics?")
    st.write("Cheminformatics applies computer science, data analysis, and information technology to chemical research. It helps organize chemical information, study molecular structures, analyze chemical properties, and support research such as drug discovery.")
    st.subheader("Project Features")
    st.markdown("""
    - **Molecular Explorer:** Search by molecule name or choose an example; view 2D structures and interactive 3D models.
    - **Periodic Table:** Search and explore selected chemical elements.
    - **Molecular Calculator:** Calculate molecular formula and mass.
    - **Student Profile:** Display the student's name and registration number.
    """)
    st.subheader("Student Details")
    st.markdown('<div class="section-card"><p><b>Student Name:</b> RATHIESH D</p><p><b>Registration Number:</b> RE2611026050338</p><p><b>Project Title:</b> Cheminformatics</p></div>', unsafe_allow_html=True)
    st.subheader("Conclusion")
    st.write("This project demonstrates how computational tools can make chemical information easier to explore and understand. It combines molecule visualization, element exploration, and molecular calculations in one interactive workspace.")

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#91a7c2; padding:15px;">
  ⚛️ Cheminformatics Workspace<br>
  Student Project | RATHIESH D<br>
  Registration Number: RE2611026050338
</div>
""", unsafe_allow_html=True)
