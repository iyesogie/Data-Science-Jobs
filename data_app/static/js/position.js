



  
   
        
       
  
          
       
     
      var outdoorsmap=L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
              attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
              maxZoom: 18,
              id: "outdoors-v10",
              accessToken: API_KEY
            });
        // Create the satellite tile layer
        var satellitemap=L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
              attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
              tileSize:512,
              maxZoom: 18,
              zoomOffset: -1,
              id: "satellite-v9",
              accessToken: API_KEY
            });
        // Create the gray tile layer
        var grayscalemap=L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
              attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
              maxZoom: 18,
              id: "light-v10",
              accessToken: API_KEY
            });
        var baseMaps={
              "Satellite":satellitemap,
              "Grayscale":grayscalemap,
              "Outdoors":outdoorsmap
      
          };
        // create myMap
        var myMap = L.map("map", {
            center: [38.52, -98.67],
            zoom: 5,
            layers:[grayscalemap]
          });
        // create layer control
          L.control.layers(baseMaps).addTo(myMap);
              
       
        
  
        engineerlatitude=[];
        engineerlongitude=[];
        engineercity=[];
        for (n=0;n<data.length;n++){
          for (o=0;o<codata.length;o++){
            if (data[n].location.split(",")[0]===codata[o].city&&data[n].location.split(",")[1].charAt(1)===codata[o].state.charAt(0)&&data[n].position.includes("Engineer")){
                   
  
                   engineerlatitude.push(codata[o].latitude)
                   engineerlongitude.push(codata[o].longitude)
                   engineercity.push(data[n].location)
                   
                    }}}
       
        engineermarker=[];
        for(p=0;p<engineerlatitude.length;p++){
          engineermarker.push(L.circleMarker([engineerlatitude[p],engineerlongitude[p]],{
            radius:"10",
            color:"red",
            stroke:false,
            opacity:0.1,
            fillcolor:"red",
            weight:0.1,
            fillopacity:0.1
          }).bindPopup(engineercity[p]))};
          L.layerGroup(engineermarker).addTo(myMap);
        analystlatitude=[];
        analystlongitude=[];
        analystcity=[];
        for (i=0;i<data.length;i++){
          for (j=0;j<codata.length;j++){
        if (data[i].location.split(",")[0]===codata[j].city&&data[i].location.split(",")[1].charAt(1)===codata[j].state.charAt(0)&&data[i].position.includes("Analyst")){
                   analystlatitude.push(codata[j].latitude)
                   analystlongitude.push(codata[j].longitude)
                   analystcity.push(data[i].location)
                   
        }}}
       
        analystmarker=[];
        for(h=0;h<analystlatitude.length;h++){
          analystmarker.push(L.circleMarker([analystlatitude[h],analystlongitude[h]],{
            radius:"10",
            color:"yellow",
            stroke:false,
            opacity:0.1,
            fillcolor:"yellow",
            weight:0.1,
            fillopacity:0.1
          }).bindPopup(analystcity[h]))};
          L.layerGroup(analystmarker).addTo(myMap);
  
          scientistlatitude=[];
          scientistlongitude=[];
          scientistcity=[];
          for (k=0;k<data.length;k++){
            for (l=0;l<codata.length;l++){
              if (data[k].location.split(",")[0]===codata[l].city&&data[k].location.split(",")[1].charAt(1)===codata[l].state.charAt(0)&&data[k].position.includes("Scientist")){
                     scientistlatitude.push(codata[l].latitude)
                     scientistlongitude.push(codata[l].longitude)
                     scientistcity.push(data[k].location)
                     
                }}}
         
          scientistmarker=[];
          for(m=0;m<scientistlatitude.length;m++){
            scientistmarker.push(L.circleMarker([scientistlatitude[m],scientistlongitude[m]],{
              radius:"10",
              color:"blue",
              stroke:false,
              opacity:0.1,
              fillcolor:"blue",
              weight:0.1,
              fillopacity:0.1
            }).bindPopup(scientistcity[m]))};
            L.layerGroup(scientistmarker).addTo(myMap);
            analystcompany=[];
            scientistcompany=[];
            engineercompany=[];
            othercompany=[];
            for (z=0;z<data.length;z++){
              if (data[z].position.includes("Analyst")){
                analystcompany.push(data[z].company)
              }
              else if(data[z].position.includes("Scientist")){
                scientistcompany.push(data[z].company)
              }            
              else if(data[z].position.includes("Engineer")){
                engineercompany.push(data[z].company)
  
              }
              else if(!data[z].position.includes("Analyst")&&!data[z].position.includes("Scientist")&&!data[z].position.includes("Engineer")){
                othercompany.push(data[z].company
                )}
              
            }
            var legend=L.control({position:"bottomright"});
            legend.onAdd=function(){
                var div=L.DomUtil.create("div","info legend");
                var categories=["#85C1E9","#F4D03F","#F1948A"];
                var labels=[];
                var legendInfo="<div class=\"labels\">"+"</div>";
                div.innerHTML=legendInfo;
               
                    labels.push(
                    "<li style=\"background-color:"+categories[0]+"\"></li>   "+"Distribution of Data Scientist (color deeper, company number larger)"+"<br>"
                    +"<li style=\"background-color:"+categories[1]+"\"></li>  "+"Distribution of Data Analyst (color deeper, company number larger)"+"<br>"
                    +"<li style=\"background-color:"+categories[2]+"\"></li>  "+"Distribution of Data Engineer (color deeper, company number larger)"+"<br>"
                    
                   );           
                
                 div.innerHTML="<ul>"+labels.join("")+"</ul>";   
                return div;
            };
            legend.addTo(myMap);
      // Create legend to indicate the color of the circle marker
     
  
  
  
      