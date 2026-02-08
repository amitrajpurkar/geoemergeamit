## GeoEmerge Hackathon: 2026/01/31

#### hackathon presentation:
* https://docs.google.com/presentation/d/1zMvGHKv9YEAXWflaAI4yl27FRFYphxvL/edit?slide=id.g3c2275cb651_0_224#slide=id.g3c2275cb651_0_224
* https://geoemerge.devpost.com. -- this is where you submit your project
* https://github.com/geo-di-lab


#### quick start
* run backend using `.venv/bin/python -m uvicorn backend.src.api.main:app --reload --host 127.0.0.1 --port 8000` 
* or run backend using `uv run python -m backend`
* verify using `curl http://127.0.0.1:8000/health`
* run `npm run dev -- --host 127.0.0.1 --port 5173` to start the frontend
* try this one `uv run python -m backend`

#### main references..
* https://geo-di-lab.github.io/emerge-lessons/intro.html
* https://geo-di-lab.github.io/emerge-lessons/docs/ch2/lesson2.html
* .. take the lessons from chapters 2 and 4.. and apply them to the data provided.. 
* create a gogle earth engine account.. 
* create a gogle earth engine project.. and register it.. anr-41793
* something to try `earthengine authenticate` from terminal
* https://console.cloud.google.com/home/dashboard?project=anr-41793&organizationId=0
* my key/token... 4/1ASc3gC10Rr2sTMCixTQBluw7j0ERfTI5DtjdHlVClvQvsSleHKJT9la2wPI




#### i was teamed with experts from UF in the intermediate level track
* experts being Delilah Penate, Thomas Barbato, and RamyaLakshmi KS, and the novice, Amit.
* https://devpost.com/software/intermediate-mosquito-risk-mapping/joins/4fMCrrQazod7qWdh_ibMJg
* https://devpost.com/software/intermediate-mosquito-risk-mapping


#### to be done.. 
* jupyter nbconvert --clear-output --inplace your_notebook.ipynb
* -- with above before git commit, always clear outputs from jupyter notebooks
* -- recommended: add a pre-commit hook or CI check to prevent committing large notebook outputs