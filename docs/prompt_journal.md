# prompt journal

## 2026-02-01
* maintain a record of how you are prompting with AI Code assistant and how you ask it to use AGENTS.md, Specs and SKILLS 
* start with the speckit constitution and link it to AGENTS.md 
* prep-work -- i already placed all three in respective locations: AGENTS.md, SKILLS.md, Speckit
* this application is a python application with frontend and backend uses EDA to show mosquito risk for a given location and date range
* skills saved here are for python code review and for EDA analysis 
* AGENTS.md has the role of a senior python developer and EDA analyst

## speckit.constitution
* this application is a python application with frontend and backend uses EDA to show mosquito risk for a given location and date range; the constitution guidelines for a senior python developer is documented in AGENTS.md; the skills for python code review and EDA analysis are documented in respective folders under ./.windsurf/skills/ under the projects root folder; As a senior python developer, use the guidelines from AGENTS.md as well as the skills from ./.windsurf/skills/ to guide your work; 

## speckit.specify
* Create a python application with frontend and backend. The application uses EDA to show mosquito risk for a given location and date range; as first feature, extract the data exploration and analysis methods from the jupyter notebooks which are under ./notebooks/ folder; modularize these methods so that these can be re-used in the backend service classes; as second feature, when the application runs, on the home page it should show two charts; one being the mosquito risk for a default location (state of florida) and first chart showing the risk overlayed on a map for last month (last 30 days) and second chart showing the risk overlayed on a map for last year (last 12 months); as third feature, on the top of the home page above these two charts, it should show form elements to select a location and date range; as fourth feature, provide a link to another page, which takes as input a location and shows three tiles; first tile should show vegetation cover changes over last two years; second tile showing temperature changes over last two years; third tile showing precipitation changes and standing water changes over last two years

## speckit.plan
* prepare a plan to implement the specifications in spec.md; make use of AGENTS.md located in the root folder of this project to guide your work; for the foundational layer, make use of the dataset information in resources/sources.yaml located in the root folder of this project; extract the data exploration and analysis methods from the jupyter notebooks which are under ./notebooks/ folder; modularize these methods so that these can be re-used in the backend service classes; 

## speckit.tasks
* prepare a task list to implement the specifications in spec.md; make use of AGENTS.md located in the root folder of this project to guide your work; make use of Skills located in ./.windsurf/skills/ to guide your work; especially for exploratory-data-analysis skill, make use of the data_exploration.md and visualization.md skills; 

## speckit.implement
* implement all tasks under phase 1 from tasks.md; make use of AGENTS.md located in the root folder of this project to guide your work; make use of Skills located in ./.windsurf/skills/ to guide your work; especially use the skill code-review as you implement the tasks; 
* implement under Phase 2, only tasks T010, T011
* implement remaining tasks under Phase 2

## review
* review the code changes made so far
