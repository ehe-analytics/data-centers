// EPA AQS daily summaries for the regulatory monitors in Loudoun (51-107) and Prince William (51-153) counties.
// Run in the browser console on any page under https://aqs.epa.gov/ (same-origin fetch).
// Uses EPA's public test credentials from the AQS API docs; register your own email/key for real use (https://aqs.epa.gov/aqsweb/documents/data_api.html).
// Result keys are site|poc|duration|units -> {date: [mean, max_hour, observation_count, validity]}. Save as data/epa_aqs_raw_extract.json.
(async()=>{const base='/data/api/dailyData/byCounty?email=test@aqs.api&key=test&bdate=20260224&edate=20261101&state=51&county=';
const out={};
for(const [name,p,c] of [['ld_pm','88101','107'],['ld_no2','42602','107'],['pw_no2','42602','153']]){
 const j=await (await fetch(base+c+'&param='+p)).json();const m={};
 for(const d of j.Data){const k=d.local_site_name+'|poc'+d.poc+'|dur'+d.sample_duration_code+'|'+d.units_of_measure;const o=m[k]||(m[k]={});
  if(!(d.date_local in o))o[d.date_local]=[d.arithmetic_mean,d.first_max_value,d.observation_count,d.validity_indicator];}
 out[name]=m;}
return JSON.stringify(out);})()
