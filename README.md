# Cheminformatics — 2D + 3D Molecule Explorer

## Features
- Search common compound names via PubChem
- Enter SMILES directly
- Render 2D molecular structures
- Generate a computational 3D conformation and explore it interactively
- View basic descriptors and export CSV
- View an illustrative 3D sphere for any periodic-table element
- Download generated molecule coordinates as `.mol`

## Run locally
Python 3.10+ recommended.

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud
1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, and `README.md`.
3. Open https://share.streamlit.io/
4. Create an app and choose `app.py` as the main file.

## Notes and limitations
- Compound name lookup requires an internet connection and uses PubChem's public API.
- 3D conformations are computational estimates, not experimentally determined structures.
- The element sphere is illustrative only and does not depict orbitals or true scale.
- This app is for education and research support, not medical or safety decisions.
