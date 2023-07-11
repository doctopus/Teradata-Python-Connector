[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
<div align="center">
  <h1>Teradata&nbsp;Python&nbsp;Connector</h1>
  <h2> Fetch SQL Database Using Python and SQLAlchemy&nbsp;</h2>
</div>
 
<br />

![READ ME Image of Project](https://upload.wikimedia.org/wikipedia/commons/1/10/Teradata_Logo.png)

<br />

<h5>What is this!</h5>
=========================
    * The code connects to teradata using SQLAlchemy from python
    * Fetches the dataframes, wrangles to come up with query list
    * Connects to query back to the Teradata with the processed list
    * This could be repuposed for other queries involving Teradata

<h5>What does this output</h5>
=========================
    * Annual report summarizing ethnic groups of enrolled patients
    * Get the consented patient list from Caris Tableau Dashboard for the IRB
    * Match with all caris patient MRNs to filter only consented patients in the time range
    * Query back to find ethnic properties and summarize

<h5>Preparing the Report</h5>
====================
    * Get Caris Consented Patients from Tableau Dashboard
    * Have only the MRNs of consented patients as .xlsx file with header PAT_MRN_ID
    * Define Date Range for report and location of MRNs.xlsx in the main.py
    * login details to be locally written in the .env file from .env_template
    * MRNs.xlsx is a dummy list of MRNS to show structure
    * No PHI in the repo

    

***




<h6>Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)</h6>
<div style="width:300px; height:200px">
</div>