import streamlit as st
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import py3Dmol
from stmol import showmol

import streamlit.components.v1 as components
from rdkit.Chem import Draw

# Configuración de página
st.set_page_config(page_title="Generador de Macrociclos", layout="wide")
st.title("🧪 Generador Molecular 3D")

# 1. Barra Lateral de Opciones
with st.sidebar:
    st.header("Configuración del Ensamblaje")
    smiles = st.text_input("SMILES del monómero", value="C12C(NC(=O)N1)NC(=O)N2")
    left_conns = st.text_input("Conexiones Izquierdas (índices)", value="3, 7")
    right_conns = st.text_input("Conexiones Derechas (índices)", value="6, 10")
    n_units = st.number_input("Número de Unidades", min_value=2, max_value=20, value=6)
    
    generar = st.button("Generar Macrociclo", type="primary")

# 2. Pantalla principal dividida en columnas
col1, col2 = st.columns([1, 2])

# Intentar parsear el monómero para la vista 2D al instante
mol = Chem.MolFromSmiles(smiles)

if mol:
    with col1:
        st.subheader("Monómero 2D")
        # Generar SVG (Aquí deberías añadir la lógica para resaltar colores en índices)
        drawer = rdMolDraw2D.MolDraw2DSVG(350, 350)
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        st.image(drawer.GetDrawingText(), use_column_width=True)

# 3. Lógica al presionar "Generar Macrociclo"
if generar:
    with col2:
        st.subheader("Visor 3D Interactivo")
        with st.spinner("Construyendo geometría y optimizando energía..."):
            # AQUI VA TU LÓGICA DE ENSAMBLAJE MATEMÁTICO:
            # (En Python trasladarías las funciones de generar_macrociclo() 
            # rotando coordenadas usando matrices de numpy/rdkit)
            
            # --- Código demostrativo (solo genera el monómero 3D original) ---
            mol_3d = Chem.AddHs(mol)
            AllChem.EmbedMolecule(mol_3d, AllChem.ETKDGv3())
            AllChem.MMFFOptimizeMolecule(mol_3d)
            pdb_block = Chem.MolToPDBBlock(mol_3d)
            # -----------------------------------------------------------------
            
            # Renderizando modelo 3D
            view = py3Dmol.view(width=600, height=450)
            view.addModel(pdb_block, "pdb")
            view.setStyle({'stick': {}, 'sphere': {'radius': 0.3}}) # Usa tu estilo
            view.setBackgroundColor('#f8fafc')
            view.zoomTo()
            
            showmol(view, height=450, width=600)
            
        st.success("¡Generación completada!")
        
        # Para descargar el archivo usando el sistema nativo de Streamlit
        st.download_button(
            label="Descargar Modelo PDB",
            data=pdb_block,
            file_name=f"macrocycle_{n_units}units.pdb",
            mime="text/plain"
        )
