import streamlit as st
import pandas as pd
import py3Dmol
import streamlit.components.v1 as components
from rdkit import Chem
from rdkit.Chem import Descriptors, Draw, rdMolDescriptors, AllChem
from rdkit.Chem.rdchem import PeriodicTable
from io import BytesIO
import requests
import re

st.set_page_config(page_title="Cheminformatics | 2D + 3D Lab", page_icon="⚛️", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #07111f 0%, #0b1728 55%, #101e32 100%); color: #edf4ff; }
[data-testid="stSidebar"] { background: #0a1423; }
.hero { padding: 1.5rem 1.7rem; border: 1px solid #20344d; border-radius: 18px;
        background: linear-gradient(120deg, #10243a, #0b1728); margin-bottom: 1rem; }
.eyebrow { color: #63e6be; text-transform: uppercase; letter-spacing: .16em; font-size: .75rem; font-weight: 700; }
.hero h1 { margin: .25rem 0 .5rem 0; color: #f4f8ff; font-size: 2.4rem; }
.hero p { color: #b8c8dc; margin-bottom: .2rem; }
div[data-testid="stMetric"] { background: #101f32; border: 1px solid #243a53; padding: 1rem; border-radius: 14px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
```python
st.markdown("""
<div class="hero">
  <div class="eyebrow">Molecular intelligence workspace</div>
  <h1>⚛️ Cheminformatics</h1>
  <p>Discover compounds and elements in interactive 2D and 3D.</p>
  <hr style="border-color:#20344d;">
  <p><b>Student Name:</b> RATHIESH D</p>
  <p><b>Registration Number:</b> RE2611026050338</p>
</div>
""", unsafe_allow_html=True)
```

""", unsafe_allow_html=True)

pt = Chem.GetPeriodicTable()

def pubchem_lookup(query):
    """Resolve a compound name using PubChem PUG REST."""
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{requests.utils.quote(query)}/property/CanonicalSMILES,IUPACName/JSON"
    try:
        response = requests.get(url, timeout=12)
        if response.ok:
            props = response.json()["PropertyTable"]["Properties"][0]
            return props.get("ConnectivitySMILES") or props.get("CanonicalSMILES"), props.get("IUPACName", "")
    except Exception:
        pass
    return None, ""

def build_3d(mol):
    mol3d = Chem.AddHs(Chem.Mol(mol))
    params = AllChem.ETKDGv3()
    params.randomSeed = 2026
    result = AllChem.EmbedMolecule(mol3d, params)
    if result != 0:
        return None, None
    try:
        AllChem.MMFFOptimizeMolecule(mol3d, maxIters=200)
    except Exception:
        try:
            AllChem.UFFOptimizeMolecule(mol3d, maxIters=200)
        except Exception:
            pass
    block = Chem.MolToMolBlock(mol3d)
    return mol3d, block

def show_3d(block, height=470):
    html = f"""
    <div id="viewer" style="width:100%;height:{height}px;position:relative;border-radius:14px;overflow:hidden;"></div>
    <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
    <script>
      const element = document.getElementById('viewer');
      const viewer = $3Dmol.createViewer(element, {{backgroundColor: '#0b1728'}});
      viewer.addModel({block!r}, 'mol');
      viewer.setStyle({{}}, {{stick: {{radius: 0.16}}, sphere: {{scale: 0.23}}}});
      viewer.zoomTo();
      viewer.render();
      viewer.zoom(0.9);
    </script>
    """
    components.html(html, height=height + 20, scrolling=False)

with st.sidebar:
    st.markdown("## ⚛️ Cheminformatics")
    page = st.radio("Workspace", ["2D + 3D Explorer", "About"])
    st.markdown("---")
    st.caption("Compound name lookup uses PubChem.")
    st.caption("3D geometry is computationally generated for supported molecules.")

if page == "About":
    st.title("About")
    st.write("Explore 2D structures and generated 3D conformations of supported molecules, plus a simple 3D display for individual elements.")
    st.warning("3D conformations are models, not experimentally determined structures. Element spheres are illustrative and not to scale.")
    st.stop()

st.subheader("Explore a compound or element")
mode = st.radio("What do you want to view?", ["Chemical compound", "Element"], horizontal=True)

if mode == "Chemical compound":
    source = st.radio("Input method", ["Compound name", "SMILES notation"], horizontal=True)
    if source == "Compound name":
        query = st.text_input("Compound name", "aspirin", placeholder="e.g. caffeine, glucose, ibuprofen")
        lookup = st.button("Find and visualize", type="primary")
        if lookup:
            with st.spinner("Looking up compound..."):
                smiles, iupac = pubchem_lookup(query.strip())
            if smiles:
                st.session_state["compound_smiles"] = smiles
                st.session_state["compound_name"] = query.strip()
                st.session_state["compound_iupac"] = iupac
            else:
                st.error("Could not find that compound by name. Try a common name or use SMILES notation.")
        smiles = st.session_state.get("compound_smiles", "CC(=O)Oc1ccccc1C(=O)O")
        compound_name = st.session_state.get("compound_name", "aspirin")
        iupac = st.session_state.get("compound_iupac", "")
        if not lookup and "compound_smiles" not in st.session_state:
            st.caption("Default example: aspirin. Press Find and visualize to look up a name.")
    else:
        smiles = st.text_input("SMILES notation", "CC(=O)Oc1ccccc1C(=O)O")
        compound_name = "Custom SMILES"
        iupac = ""
        st.session_state["compound_smiles"] = smiles

    if source == "SMILES notation" or "compound_smiles" in st.session_state:
        active_smiles = st.session_state.get("compound_smiles", smiles) if source == "Compound name" else smiles
        mol = Chem.MolFromSmiles(active_smiles) if active_smiles else None
        if mol is None:
            st.error("That SMILES string could not be parsed. Check it and try again.")
        else:
            canonical = Chem.MolToSmiles(mol)
            st.markdown(f"### {compound_name.title() if compound_name else 'Molecule'}")
            if iupac:
                st.caption(f"IUPAC name: {iupac}")
            tab2d, tab3d, tabdata = st.tabs(["🧬 2D structure", "🪐 Interactive 3D", "📊 Properties"])
            with tab2d:
                col1, col2 = st.columns([1.15, 1])
                with col1:
                    st.image(Draw.MolToImage(mol, size=(650, 440)), use_container_width=True)
                with col2:
                    st.markdown("#### Structure details")
                    st.write(f"**Canonical SMILES**")
                    st.code(canonical)
                    st.metric("Atoms (heavy)", mol.GetNumHeavyAtoms())
                    st.metric("Rings", rdMolDescriptors.CalcNumRings(mol))
            with tab3d:
                st.markdown("Rotate with your mouse or finger; zoom to inspect the structure.")
                with st.spinner("Generating a 3D conformation..."):
                    mol3d, block = build_3d(mol)
                if block:
                    show_3d(block)
                    st.download_button("Download 3D structure (.mol)", block, file_name="molecule_3d.mol", mime="chemical/x-mdl-mol")
                else:
                    st.warning("Could not generate a 3D conformation for this structure.")
            with tabdata:
                props = {
                    "Molecular weight (g/mol)": round(Descriptors.MolWt(mol), 3),
                    "Exact molecular weight (Da)": round(Descriptors.ExactMolWt(mol), 4),
                    "Calculated LogP": round(Descriptors.MolLogP(mol), 3),
                    "TPSA (Å²)": round(rdMolDescriptors.CalcTPSA(mol), 3),
                    "H-bond donors": int(rdMolDescriptors.CalcNumHBD(mol)),
                    "H-bond acceptors": int(rdMolDescriptors.CalcNumHBA(mol)),
                    "Rotatable bonds": int(rdMolDescriptors.CalcNumRotatableBonds(mol)),
                    "Heavy atoms": int(mol.GetNumHeavyAtoms()),
                    "Aromatic rings": int(rdMolDescriptors.CalcNumAromaticRings(mol)),
                    "Total rings": int(rdMolDescriptors.CalcNumRings(mol)),
                }
                st.dataframe(pd.DataFrame([{"Property": k, "Value": v} for k, v in props.items()]), hide_index=True, use_container_width=True)
                export_df = pd.DataFrame([{"Name": compound_name, "Input SMILES": active_smiles, "Canonical SMILES": canonical, **props}])
                st.download_button("Download properties as CSV", export_df.to_csv(index=False).encode(), "molecule_properties.csv", "text/csv")
            st.caption("Generated 3D conformations are estimates. Descriptor values do not establish biological activity, safety, or medical suitability.")

else:
    st.write("Choose an element to display an illustrative single-atom model.")
    symbols = [pt.GetElementSymbol(i) for i in range(1, 119)]
    symbol = st.selectbox("Element", symbols, index=5)
    atomic_num = pt.GetAtomicNumber(symbol)
    col1, col2 = st.columns([1, 1.25])
    with col1:
        st.markdown(f"### {pt.GetElementName(atomic_num)} ({symbol})")
        st.metric("Atomic number", atomic_num)
        st.metric("Atomic mass", f"{pt.GetAtomicWeight(atomic_num):.4f} u")
        st.info("This sphere is a schematic visualization of one atom. It does not show electron orbitals or the atom's true scale.")
    with col2:
        # A single atom represented as an XYZ model; viewer is interactive.
        xyz = f"1\n{symbol} atom (illustrative)\n{symbol} 0.0 0.0 0.0\n"
        html = f"""
        <div id="atomviewer" style="width:100%;height:430px;border-radius:14px;overflow:hidden;"></div>
        <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
        <script>
          const el = document.getElementById('atomviewer');
          const v = $3Dmol.createViewer(el, {{backgroundColor:'#0b1728'}});
          v.addModel({xyz!r}, 'xyz');
          v.setStyle({{}}, {{sphere: {{scale: 1.7}}}});
          v.zoomTo();
          v.render();
        </script>
        """
        components.html(html, height=450, scrolling=False)

st.markdown("---")
st.caption("Cheminformatics • 2D + 3D explorer • Powered by RDKit and 3Dmol.js")
