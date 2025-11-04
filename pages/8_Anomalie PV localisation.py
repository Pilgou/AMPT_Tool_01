import streamlit as st

with open("./SVG/solar_layout_clean05.svg", "r") as f:
    svg_code = f.read()


html_code = f"""
<div style="position: relative; display: inline-block;">

  <div style="position: absolute; top: 100px; left: 250px;
              width: 150px; height: 120px;
              border: 3px solid red; background-color: rgba(255,0,0,0.2);"></div>
  {svg_code}
</div>

<!-- Texte sous le rectangle -->
  <div style="position: absolute; top: 230px; left: 250px; 
              width: 150px; text-align: center; 
              color: red; font-weight: bold; font-family: Arial; font-size: 16px;">
    Zone critique
  </div>
"""

st.markdown(html_code, unsafe_allow_html=True)

