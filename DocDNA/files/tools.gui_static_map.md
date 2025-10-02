# tools.gui_static_map

> GUI Static Map: Analyze chatterbox_gui.py to map buttons → slots → inputs → external calls.

## Public API

### Classes
- **GUISpy**  
  Methods: visit_Assign, visit_Call, visit_FunctionDef
- **SlotAnalyzer**  
  Methods: visit_Call, generic_visit

### Functions
- **qualname_from_attr**
- **build_feature_map**
- **main**
- **visit_Assign**
- **visit_Call**
- **visit_FunctionDef**
- **visit_Call**
- **generic_visit**

## Imports (local guesses)
- __future__, ast, json, pathlib, typing

## Entrypoint
- Contains `if __name__ == '__main__':` block