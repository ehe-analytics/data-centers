// Pull hourly PM2.5 (1266), NO2 (1253) and CO (1263) for every DEQ location from the Kunak Cloud widget,
// and aggregate to EST daily [hours, mean, max] per element and day.
// Run in the browser console on https://kunakcloud.com/websites/VirginiaDEQ.html (it needs that page's widgetConfig token).
// Takes a few minutes; poll window.__job.done, then copy JSON.stringify(window.__job.H) into data/raw/kunak_hourly_agg.json.
// scripts/make_air_daily.py (see README) turns that into data/air_daily.json.
window.__job={done:false,err:null,prog:0,H:{}};
(async()=>{try{
 const locs=[679,680,681,682,683,684,685,686,736,779,780,781,822,823];
 const els=['1253','1263','1266'];
 const start=Date.UTC(2026,1,24),end=Date.UTC(2026,10,2),chunks=[];
 for(let t=start;t<end;t+=28*864e5){chunks.push([new Date(t).toISOString().slice(0,10),new Date(Math.min(t+27*864e5,end)).toISOString().slice(0,10)]);}
 for(const loc of locs){const H={};
  for(const [a,b] of chunks){
   const body=new URLSearchParams({token:widgetConfig.token,id:String(loc),pollutants:JSON.stringify(els),fromDate:a,toDate:b,groupBy:'1',unitGases:widgetConfig.unitGases,unitWindSpeed:widgetConfig.unitWindSpeed});
   const r=await (await fetch('/dashboards/services/getWidgetNavFromToChartData',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'},body})).json();
   let d=r.datesReadsCharts;if(typeof d==='string')d=JSON.parse(d);
   for(const e of els){for(const row of (d&&d[e])||[]){if(row[1]==null)continue;
     const day=new Date(row[0]-5*3600e3).toISOString().slice(0,10); // EST day
     const k=e+'|'+day;(H[k]=H[k]||new Map()).set(row[0],row[1]);}}}
  window.__job.H[loc]=Object.fromEntries(Object.entries(H).map(([k,m])=>{const v=[...m.values()];return [k,[v.length,+(v.reduce((s,x)=>s+x,0)/v.length).toFixed(4),Math.max(...v)]]}));
  window.__job.prog++;}
 window.__job.done=true;}catch(e){window.__job.err=String(e)}})();
