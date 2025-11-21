import importlib
import streamlit as st

# This wrapper tries to import common Streamlit entry modules from the repository.
# If it finds a module and a callable entrypoint (main or run) it will call it.
# Otherwise it shows a helpful placeholder message so you can update the file path
# used by Streamlit Cloud or replace this wrapper with your real entrypoint.

candidates = [
    ("streamlit_app", "main"),
    ("streamlit_app", "run"),
    ("app", "main"),
    ("app", "run"),
    ("main", "main"),
    ("main", "run"),
    ("src.app", "main"),
    ("src.app", "run"),
    ("app", ""),
    ("streamlit_app", ""),
]

ran = False
for module_name, func_name in candidates:
    try:
        module = importlib.import_module(module_name)
        if func_name:
            func = getattr(module, func_name, None)
            if callable(func):
                func()
                ran = True
                break
        else:
            # import may run top-level streamlit code
            ran = True
            break
    except ModuleNotFoundError:
        continue
    except Exception as e:
        st.error(f"Error while running {module_name}.{func_name}: {e}")
        ran = True
        break

if not ran:
    st.title("Streamlit app placeholder")
    st.write(
        "No existing Streamlit entrypoint module was found in the repository."
        " If your real app file is named something else, either rename it to one of"
        " common names (streamlit_app.py, app.py, main.py) or point Streamlit Cloud"
        " to the correct file path when you create the app."
    )
    st.write("Tips:")
    st.write("- Ensure a requirements.txt exists listing 'streamlit' and other dependencies.")
    st.write("- If your app expects API keys, configure them in Streamlit Cloud Settings → Secrets.")
