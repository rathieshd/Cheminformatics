
import streamlit as st
import pandas as pd
import requests
from rdkit import Chem
from rdkit.Chem import Descriptors, Draw, rdMolDescriptors, AllChem
import streamlit.components.v1 as components

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Cheminformatics | 2D + 3D Lab",
    page_icon="⚛️",
    layout="wide"
)

# --------------------------------------------------
# STUDENT DETAILS
# --------------------------------------------------

STUDENT_NAME = "RATHIESH D"
REGISTRATION_NUMBER = "RE2611026050338"

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg,
        #07111f 0%,
        #0b1728 55%,
        #101e32 100%
    );
    color: #edf4ff;
}

[data-testid="stSidebar"] {
    background: #0a1423;
}

.hero {
    padding: 1.7rem;
    border: 1px solid #20344d;
    border-radius: 18px;
    background: linear-gradient(120deg, #10243a, #0b1728);
    margin-bottom: 1.5rem;
}

.eyebrow {
    color: #63e6be;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    font-size: 0.75rem;
    font-weight: 700;
}

.hero h1 {
    margin: 0.4rem 0;
    color: #f4f8ff;
    font-size: 2.5rem;
}

.hero p {
    color: #b8c8dc;
}

.student-card {
    background: #101f32;
    border: 1px solid #29435f;
    border-radius: 14px;
    padding: 1rem;
    margin-top: 1rem;
}

.student-card p {
    margin: 0.4rem 0;
}

div[data-testid="stMetric"] {
    background: #101f32;
    border: 1px solid #243a53;
    padding: 1rem;
    border-radius: 14px;
}

.stTabs [data-baseweb="tab"] {
    color: #edf4ff;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# WEBSITE HEADER
# --------------------------------------------------

st.markdown(f"""
<div class="hero">
    <div class="eyebrow">
        Molecular Intelligence Workspace
    </div>

    <h1>⚛️ Cheminformatics</h1>

    <p>
        Discover compounds and elements in interactive
        2D and 3D molecular visualizations.
    </p>

    <div class="student-card">
        <p><b>Student Name:</b> {STUDENT_NAME}</p>
        <p><b>Registration Number:</b> {REGISTRATION_NUMBER}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# PERIODIC TABLE
# --------------------------------------------------

pt = Chem.GetPeriodicTable()

# --------------------------------------------------
# PUBCHEM COMPOUND SEARCH
# --------------------------------------------------

def pubchem_lookup(query):
    """Find compound information using PubChem."""

    url = (
        "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
        f"{requests.utils.quote(query)}/property/"
        "CanonicalSMILES,IUPACName/JSON"
    )

    try:
        response = requests.get(url, timeout=15)

        if response.ok:
            properties = response.json()[
                "PropertyTable"
            ]["Properties"][0]

            smiles = properties.get("ConnectivitySMILES")
            if not smiles:
                smiles = properties.get("CanonicalSMILES")

            iupac_name = properties.get("IUPACName", "")

            return smiles, iupac_name

    except (requests.RequestException, ValueError, KeyError, IndexError):
        pass

    return None, ""


# --------------------------------------------------
# GENERATE 3D MOLECULAR STRUCTURE
# --------------------------------------------------

def build_3d(mol):
    """Generate a computational 3D molecular conformation."""

    mol3d = Chem.AddHs(Chem.Mol(mol))

    params = AllChem.ETKDGv3()
    params.randomSeed = 2026

    result = AllChem.EmbedMolecule(mol3d, params)

    if result != 0:
        return None, None

    try:
        optimization_result = AllChem.MMFFOptimizeMolecule(
            mol3d,
            maxIters=200
        )

        if optimization_result == -1:
            AllChem.UFFOptimizeMolecule(mol3d, maxIters=200)

    except Exception:
        try:
            AllChem.UFFOptimizeMolecule(mol3d, maxIters=200)
        except Exception:
            pass

    mol_block = Chem.MolToMolBlock(mol3d)

    return mol3d, mol_block


# --------------------------------------------------
# INTERACTIVE 3D VIEWER
# --------------------------------------------------

def show_3d(mol_block, height=470):

    # JSON encoding safely transfers the molecule data into JavaScript.
    import json

    molecule_json = json.dumps(mol_block)

    html = f"""
    <div
        id="molecule-viewer"
        style="
            width:100%;
            height:{height}px;
            position:relative;
            border-radius:14px;
            overflow:hidden;
        ">
    </div>

    <script src="https://3Dmol.org/build/3Dmol-min.js"></script>

    <script>
        (function() {{
            const element =
                document.getElementById("molecule-viewer");

            function initializeViewer() {{
                if (!window.$3Dmol) {{
                    element.innerHTML =
                        "<p style='color:white;padding:20px;'>"
                        + "3D viewer could not load. "
                        + "Check your internet connection."
                        + "</p>";
                    return;
                }}

                const viewer = $3Dmol.createViewer(element, {{
                    backgroundColor: "#0b1728"
                }});

                viewer.addModel({molecule_json}, "mol");

                viewer.setStyle({{}}, {{
                    stick: {{ radius: 0.16 }},
                    sphere: {{ scale: 0.23 }}
                }});

                viewer.zoomTo();
                viewer.render();
            }}

            if (window.$3Dmol) {{
                initializeViewer();
            }} else {{
                const script =
                    document.querySelector(
                        'script[src*="3Dmol-min.js"]'
                    );

                if (script) {{
                    script.addEventListener(
                        "load",
                        initializeViewer,
                        {{ once: true }}
                    );
                }}
            }}
        }})();
    </script>
    """

    components.html(
        html,
        height=height + 20,
        scrolling=False
    )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## ⚛️ Cheminformatics")

    st.markdown("---")

    st.markdown("### Student Details")

    st.write(f"**Name:** {STUDENT_NAME}")

    st.write(f"**Reg. No.:** {REGISTRATION_NUMBER}")

    st.markdown("---")

    page = st.radio(
        "Workspace",
        [
            "2D + 3D Explorer",
            "About"
        ]
    )

    st.markdown("---")

    st.caption("Compound information: PubChem")

    st.caption("Molecular calculations: RDKit")

    st.caption("3D visualization: 3Dmol.js")


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

if page == "About":

    st.title("About Cheminformatics")

    st.write(
        "Cheminformatics combines chemistry, computer science, "
        "and data analysis to study and understand chemical compounds."
    )

    st.markdown("### Student Information")

    st.info(
        f"Student Name: {STUDENT_NAME}\n\n"
        f"Registration Number: {REGISTRATION_NUMBER}"
    )

    st.markdown("### Features")

    st.markdown("""
    - Explore 2D molecular structures.
    - Generate and inspect computational 3D conformations.
    - Search for chemical compounds using PubChem.
    - Calculate common molecular descriptors.
    - Explore elements and their atomic properties.
    - Download molecular structures and property reports.
    """)

    st.warning(
        "Generated 3D structures are computational models. "
        "They are not necessarily experimentally determined structures."
    )

    st.markdown("---")

    st.caption(
        f"Created by {STUDENT_NAME} | "
        f"Registration Number: {REGISTRATION_NUMBER}"
    )

    st.stop()


# --------------------------------------------------
# MAIN EXPLORER
# --------------------------------------------------

st.subheader("Explore a Compound or Element")

mode = st.radio(
    "Choose what you want to explore:",
    ["Chemical Compound", "Element"],
    horizontal=True
)


# ==================================================
# CHEMICAL COMPOUND EXPLORER
# ==================================================

if mode == "Chemical Compound":

    source = st.radio(
        "Input method",
        ["Compound Name", "SMILES Notation"],
        horizontal=True
    )

    smiles = ""
    compound_name = ""
    iupac_name = ""

    # ----------------------------------------------
    # INPUT BY COMPOUND NAME
    # ----------------------------------------------

    if source == "Compound Name":

        query = st.text_input(
            "Enter compound name",
            value="aspirin",
            placeholder="e.g. caffeine, glucose, ibuprofen"
        )

        if st.button(
            "🔍 Find and Visualize",
            type="primary"
        ):

            if not query.strip():

                st.error("Please enter a compound name.")

            else:

                with st.spinner("Searching PubChem..."):

                    found_smiles, found_iupac = pubchem_lookup(
                        query.strip()
                    )

                if found_smiles:

                    st.session_state["compound_smiles"] = found_smiles

                    st.session_state["compound_name"] = query.strip()

                    st.session_state["compound_iupac"] = found_iupac

                else:

                    st.error(
                        "Compound not found. Check the spelling "
                        "or try another compound name."
                    )

        smiles = st.session_state.get(
            "compound_smiles",
            "CC(=O)Oc1ccccc1C(=O)O"
        )

        compound_name = st.session_state.get(
            "compound_name",
            "aspirin"
        )

        iupac_name = st.session_state.get(
            "compound_iupac",
            ""
        )

        if "compound_smiles" not in st.session_state:

            st.caption(
                "Default example: Aspirin. Enter a name and "
                "click Find and Visualize to search."
            )

    # ----------------------------------------------
    # INPUT BY SMILES
    # ----------------------------------------------

    else:

        smiles = st.text_input(
            "Enter SMILES notation",
            value="CC(=O)Oc1ccccc1C(=O)O",
            help="Example: CCO represents ethanol."
        )

        compound_name = "Custom SMILES"

        iupac_name = ""

    # ----------------------------------------------
    # PARSE MOLECULE
    # ----------------------------------------------

    mol = Chem.MolFromSmiles(smiles) if smiles else None

    if mol is None:

        st.error(
            "Invalid SMILES notation. Please check the input."
        )

    else:

        canonical_smiles = Chem.MolToSmiles(mol)

        st.markdown(
            f"### 🧬 {compound_name.title()}"
        )

        if iupac_name:

            st.caption(f"IUPAC Name: {iupac_name}")

        tab2d, tab3d, tabdata = st.tabs([
            "🧬 2D Structure",
            "🪐 Interactive 3D",
            "📊 Molecular Properties"
        ])

        # ==========================================
        # 2D STRUCTURE
        # ==========================================

        with tab2d:

            col1, col2 = st.columns([1.2, 1])

            with col1:

                st.image(
                    Draw.MolToImage(
                        mol,
                        size=(650, 440)
                    ),
                    use_container_width=True
                )

            with col2:

                st.markdown("#### Structure Details")

                st.write("**Canonical SMILES**")

                st.code(canonical_smiles)

                st.metric(
                    "Heavy Atoms",
                    mol.GetNumHeavyAtoms()
                )

                st.metric(
                    "Number of Rings",
                    rdMolDescriptors.CalcNumRings(mol)
                )

                st.metric(
                    "Total Atoms (without added hydrogens)",
                    mol.GetNumAtoms()
                )

                st.download_button(
                    "📥 Download 2D Structure (PNG)",
                    data=Draw.MolToImage(
                        mol,
                        size=(900, 650)
                    ).save_to_bytes("PNG"),
                    file_name="molecule_2d.png",
                    mime="image/png"
                )

        # ==========================================
        # 3D STRUCTURE
        # ==========================================

        with tab3d:

            st.markdown(
                "Rotate the molecular model with your mouse. "
                "Use the mouse wheel to zoom."
            )

            with st.spinner(
                "Generating a 3D molecular conformation..."
            ):

                try:

                    mol3d, mol_block = build_3d(mol)

                except Exception:

                    mol3d, mol_block = None, None

            if mol_block:

                show_3d(mol_block)

                st.download_button(
                    "📥 Download 3D Structure (.mol)",
                    data=mol_block,
                    file_name="molecule_3d.mol",
                    mime="chemical/x-mdl-molfile"
                )

            else:

                st.warning(
                    "A 3D conformation could not be generated "
                    "for this molecule."
                )

        # ==========================================
        # MOLECULAR PROPERTIES
        # ==========================================

        with tabdata:

            properties = {
                "Molecular Weight (g/mol)": round(
                    Descriptors.MolWt(mol), 3
                ),

                "Exact Molecular Weight (Da)": round(
                    Descriptors.ExactMolWt(mol), 4
                ),

                "Calculated LogP": round(
                    Descriptors.MolLogP(mol), 3
                ),

                "TPSA (Å²)": round(
                    rdMolDescriptors.CalcTPSA(mol), 3
                ),

                "Hydrogen Bond Donors": int(
                    rdMolDescriptors.CalcNumHBD(mol)
                ),

                "Hydrogen Bond Acceptors": int(
                    rdMolDescriptors.CalcNumHBA(mol)
                ),

                "Rotatable Bonds": int(
                    rdMolDescriptors.CalcNumRotatableBonds(mol)
                ),

                "Heavy Atoms": int(
                    mol.GetNumHeavyAtoms()
                ),

                "Aromatic Rings": int(
                    rdMolDescriptors.CalcNumAromaticRings(mol)
                ),

                "Total Rings": int(
                    rdMolDescriptors.CalcNumRings(mol)
                )
            }

            properties_df = pd.DataFrame(
                [
                    {"Property": key, "Value": value}
                    for key, value in properties.items()
                ]
            )

            st.dataframe(
                properties_df,
                hide_index=True,
                use_container_width=True
            )

            export_df = pd.DataFrame([
                {
                    "Compound Name": compound_name,
                    "Input SMILES": smiles,
                    "Canonical SMILES": canonical_smiles,
                    **properties
                }
            ])

            st.download_button(
                "📥 Download Properties (CSV)",
                data=export_df.to_csv(
                    index=False
                ).encode("utf-8"),
                file_name="molecule_properties.csv",
                mime="text/csv"
            )

            st.caption(
                "Calculated descriptors are computational estimates. "
                "They do not establish biological activity, safety, "
                "or medical suitability."
            )


# ==================================================
# ELEMENT EXPLORER
# ==================================================

else:

    st.write(
        "Select a chemical element to view its basic atomic properties."
    )

    element_symbols = [
        pt.GetElementSymbol(i)
        for i in range(1, 119)
    ]

    symbol = st.selectbox(
        "Select an element",
        element_symbols,
        index=5
    )

    atomic_number = pt.GetAtomicNumber(symbol)

    element_name = pt.GetElementName(atomic_number)

    atomic_mass = pt.GetAtomicWeight(atomic_number)

    col1, col2 = st.columns([1, 1.25])

    with col1:

        st.markdown(
            f"### ⚛️ {element_name} ({symbol})"
        )

        st.metric(
            "Atomic Number",
            atomic_number
        )

        st.metric(
            "Atomic Mass",
            f"{atomic_mass:.4f} u"
        )

        st.info(
            "The 3D sphere is illustrative. It does not represent "
            "the true atomic scale, electron orbitals, or electron "
            "probability distribution."
        )

        element_data = pd.DataFrame([
            {
                "Element": element_name,
                "Symbol": symbol,
                "Atomic Number": atomic_number,
                "Atomic Mass (u)": atomic_mass
            }
        ])

        st.download_button(
            "📥 Download Element Data (CSV)",
            data=element_data.to_csv(
                index=False
            ).encode("utf-8"),
            file_name=f"{symbol}_element_data.csv",
            mime="text/csv"
        )

    with col2:

        import json

        xyz_data = (
            f"1\n"
            f"{symbol} illustrative atom\n"
            f"{symbol} 0.0 0.0 0.0\n"
        )

        xyz_json = json.dumps(xyz_data)

        html = f"""
        <div
            id="atom-viewer"
            style="
                width:100%;
                height:430px;
                border-radius:14px;
                overflow:hidden;
            ">
        </div>

        <script src="https://3Dmol.org/build/3Dmol-min.js"></script>

        <script>
            (function() {{
                const element =
                    document.getElementById("atom-viewer");

                function initializeAtomViewer() {{
                    if (!window.$3Dmol) {{
                        element.innerHTML =
                            "<p style='color:white;padding:20px;'>"
                            + "3D viewer unavailable. Check your "
                            + "internet connection."
                            + "</p>";
                        return;
                    }}

                    const viewer = $3Dmol.createViewer(element, {{
                        backgroundColor: "#0b1728"
                    }});

                    viewer.addModel({xyz_json}, "xyz");

                    viewer.setStyle({{}}, {{
                        sphere: {{ scale: 1.7 }}
                    }});

                    viewer.zoomTo();
                    viewer.render();
                }}

                if (window.$3Dmol) {{
                    initializeAtomViewer();
                }} else {{
                    const script = document.querySelector(
                        'script[src*="3Dmol-min.js"]'
                    );

                    if (script) {{
                        script.addEventListener(
                            "load",
                            initializeAtomViewer,
                            {{ once: true }}
                        );
                    }}
                }}
            }})();
        </script>
        """

        components.html(
            html,
            height=450,
            scrolling=False
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    f"""
    <div style="text-align:center; padding:1rem; color:#b8c8dc;">
        <p>⚛️ Cheminformatics | 2D + 3D Molecular Explorer</p>
        <p>Created by <b>{STUDENT_NAME}</b></p>
        <p>Registration Number: {REGISTRATION_NUMBER}</p>
        <p>Powered by RDKit, Streamlit, PubChem and 3Dmol.js</p>
    </div>
    """,
    unsafe_allow_html=True
)

