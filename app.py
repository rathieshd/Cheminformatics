```python
import streamlit as st
import pandas as pd

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------
st.set_page_config(
    page_title="Cheminformatics | Molecular Workspace",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #07111f, #0b1728, #101f33);
    color: #e8f0ff;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

.hero {
    padding: 35px;
    border-radius: 22px;
    background: linear-gradient(120deg, #14243a, #1b3150);
    border: 1px solid #294563;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.25);
    margin-bottom: 25px;
}

.eyebrow {
    color: #52e0c4;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-weight: bold;
}

.hero h1 {
    font-size: 48px;
    color: #ffffff;
    margin-bottom: 10px;
}

.hero p {
    color: #c2d2e8;
    font-size: 16px;
}

.student-card {
    background: #12243a;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #294563;
    margin-top: 20px;
}

.section-card {
    background: #112138;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #263e59;
    margin-bottom: 15px;
}

.small-label {
    color: #52e0c4;
    font-size: 13px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
}

div[data-testid="stMetric"] {
    background: #12243a;
    border: 1px solid #294563;
    padding: 18px;
    border-radius: 14px;
}

h2, h3 {
    color: #ffffff;
}

.stButton > button {
    border-radius: 10px;
    border: 1px solid #52e0c4;
    background: #17374a;
    color: white;
    font-weight: bold;
}

.stButton > button:hover {
    background: #24576a;
    color: white;
    border-color: #52e0c4;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.markdown("# ⚛️ ChemLab")
st.sidebar.caption("Molecular Intelligence Workspace")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Home",
        "Periodic Table",
        "Molecular Calculator",
        "About"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### Student Profile")
st.sidebar.write("**Name:** RATHIESH D")
st.sidebar.write("**Register No.:** RE2611026050338")
st.sidebar.caption("Cheminformatics Project")

# -----------------------------------
# HOME PAGE
# -----------------------------------
if page == "Home":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">Molecular intelligence workspace</div>
        <h1>⚛️ Cheminformatics</h1>
        <p>Discover compounds and elements in interactive 2D and 3D.</p>
        <hr style="border-color:#20344d;">
        <div class="student-card">
            <p><b>Student Name:</b> RATHIESH D</p>
            <p><b>Registration Number:</b> RE2611026050338</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Explore Your Chemistry Workspace")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="small-label">MODULE 01</div>
            <h3>🧪 Periodic Table</h3>
            <p>Explore chemical elements, atomic numbers,
            symbols, and atomic masses.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Explore Elements", use_container_width=True):
            st.session_state["page"] = "Periodic Table"
            st.info("Select Periodic Table from the sidebar.")

    with col2:
        st.markdown("""
        <div class="section-card">
            <div class="small-label">MODULE 02</div>
            <h3>🧬 Molecular Calculator</h3>
            <p>Calculate approximate molecular masses
            using chemical formulas.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Calculate Mass", use_container_width=True):
            st.info("Select Molecular Calculator from the sidebar.")

    with col3:
        st.markdown("""
        <div class="section-card">
            <div class="small-label">MODULE 03</div>
            <h3>🔬 Research Workspace</h3>
            <p>Learn about cheminformatics and
            computer-assisted chemical research.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("About Project", use_container_width=True):
            st.info("Select About from the sidebar.")

    st.subheader("Workspace Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Project", "Cheminformatics")
    col2.metric("Core Modules", "2")
    col3.metric("Workspace", "Interactive")

    st.markdown("""
    <div class="section-card">
        <h3>🎯 Project Objective</h3>
        <p>
        This project introduces cheminformatics through chemical
        element exploration, molecular mass calculations, and
        digital chemistry tools.
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------
# PERIODIC TABLE PAGE
# -----------------------------------
elif page == "Periodic Table":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">Chemical element explorer</div>
        <h1>🧪 Periodic Table</h1>
        <p>Search and explore common chemical elements.</p>
    </div>
    """, unsafe_allow_html=True)

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
        {"Atomic Number": 20, "Symbol": "Ca", "Element": "Calcium", "Atomic Mass": 40.078}
    ]

    df = pd.DataFrame(elements)

    search = st.text_input(
        "Search by element name or symbol",
        placeholder="Example: Carbon or C"
    )

    if search:
        df = df[
            df["Element"].str.contains(search, case=False, na=False)
            | df["Symbol"].str.contains(search, case=False, na=False)
        ]

    st.dataframe(df, use_container_width=True, hide_index=True)

    selected_symbol = st.selectbox(
        "Choose an element for details",
        [item["Symbol"] for item in elements]
    )

    selected = next(
        item for item in elements
        if item["Symbol"] == selected_symbol
    )

    st.markdown(f"""
    <div class="section-card">
        <div class="small-label">ELEMENT DETAILS</div>
        <h1>{selected["Symbol"]}</h1>
        <h3>{selected["Element"]}</h3>
        <p>Atomic Number: {selected["Atomic Number"]}</p>
        <p>Standard Atomic Mass: {selected["Atomic Mass"]}</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------
# MOLECULAR CALCULATOR PAGE
# -----------------------------------
elif page == "Molecular Calculator":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">Molecular analysis tools</div>
        <h1>🧬 Molecular Calculator</h1>
        <p>Calculate molecular mass from a simple chemical formula.</p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "Enter a formula using element symbols and numbers, "
        "such as H2O, CO2, or NaCl. Parentheses are not supported."
    )

    atomic_masses = {
        "H": 1.008,
        "He": 4.0026,
        "Li": 6.94,
        "Be": 9.0122,
        "B": 10.81,
        "C": 12.011,
        "N": 14.007,
        "O": 15.999,
        "F": 18.998,
        "Ne": 20.180,
        "Na": 22.990,
        "Mg": 24.305,
        "Al": 26.982,
        "Si": 28.085,
        "P": 30.974,
        "S": 32.06,
        "Cl": 35.45,
        "Ar": 39.948,
        "K": 39.098,
        "Ca": 40.078,
        "Fe": 55.845,
        "Cu": 63.546,
        "Zn": 65.38,
        "Ag": 107.868,
        "I": 126.904,
        "Ba": 137.327,
        "Au": 196.967,
        "Hg": 200.592,
        "Pb": 207.2
    }

    formula = st.text_input(
        "Chemical Formula",
        placeholder="Example: H2O"
    )

    if st.button("Calculate Molecular Mass", type="primary"):

        import re

        if not formula:
            st.warning("Please enter a chemical formula.")

        else:
            tokens = re.findall(r"[A-Z][a-z]?|[0-9]+", formula)

            reconstructed = "".join(tokens)

            if reconstructed != formula or not tokens:
                st.error(
                    "Invalid formula format. Use element symbols "
                    "and numbers only, without spaces or parentheses."
                )

            else:
                mass = 0.0
                composition = {}
                i = 0
                valid = True

                while i < len(tokens):
                    symbol = tokens[i]

                    if symbol not in atomic_masses:
                        st.error(
                            f"Atomic mass data is unavailable for {symbol}."
                        )
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
                    composition[symbol] = (
                        composition.get(symbol, 0) + count
                    )

                    i += 1

                if valid:
                    st.success("Calculation completed successfully!")

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Molecular Mass",
                        f"{mass:.4f} g/mol"
                    )

                    col2.metric(
                        "Unique Elements",
                        str(len(composition))
                    )

                    st.subheader("Element Composition")

                    result_df = pd.DataFrame([
                        {
                            "Element": symbol,
                            "Atom Count": count,
                            "Atomic Mass": atomic_masses[symbol],
                            "Contribution (g/mol)": (
                                atomic_masses[symbol] * count
                            )
                        }
                        for symbol, count in composition.items()
                    ])

                    st.dataframe(
                        result_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.caption(
                        "This calculator supports simple formulas only. "
                        "It does not interpret parentheses, hydrates, "
                        "ionic charges, or complex formula notation."
                    )

# -----------------------------------
# ABOUT PAGE
# -----------------------------------
elif page == "About":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">Project information</div>
        <h1>📘 About Cheminformatics</h1>
        <p>Connecting chemistry and computational science.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("What is Cheminformatics?")

    st.write("""
    Cheminformatics is the application of computer science,
    data analysis, and information technology to chemical research.

    It helps researchers organize chemical information, study
    molecular structures, analyze chemical properties, and
    support drug discovery.
    """)

    st.subheader("Project Features")

    st.markdown("""
    - **Periodic Table:** Search and explore selected chemical elements.
    - **Molecular Calculator:** Calculate approximate molecular masses.
    - **Interactive Interface:** Navigate between the project's modules.
    - **Student Profile:** Display the student's name and registration number.
    """)

    st.subheader("Student Details")

    st.markdown("""
    <div class="section-card">
        <p><b>Student Name:</b> RATHIESH D</p>
        <p><b>Registration Number:</b> RE2611026050338</p>
        <p><b>Project Title:</b> Cheminformatics</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Conclusion")

    st.write("""
    This project demonstrates how computational tools can make
    chemical information easier to explore and understand.
    It provides a starting point for learning about chemical
    data, molecular mass calculations, and digital chemistry.
    """)

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("---")

st.markdown("""
<div style="text-align:center; color:#91a7c2; padding:15px;">
    ⚛️ Cheminformatics Workspace
    <br>
    Student Project | RATHIESH D
    <br>
    Registration Number: RE2611026050338
</div>
""", unsafe_allow_html=True)
```
