add mode image text-first text-second text-third start resize size:
    mkdir -p pdfs jpgs typs
    python scripts/gen_typ.py {{mode}} "{{image}}" "{{text-first}}" "{{text-second}}" "{{text-third}}" "{{start}}" {{resize}} "{{size}}"