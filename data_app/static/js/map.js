// load js file to JSON.

      //Get latitude and longitude from cities.json data  
      var cities=[]
      var latitudes=[]
      var longitudes=[]
      var states=[]
      var ratings=[]
      var salary=[]
      var salarydict=[]
      for (i=0;i<data.length;i++){
        for (j=0;j<codata.length;j++){
          if (data[i].location.split(",")[0]===codata[j].city&&data[i].location.split(",")[1].charAt(1)===codata[j].state.charAt(0)){
              cities.push(data[i].location)
              states.push(codata[j].state)
              latitudes.push(codata[j].latitude)
              longitudes.push(codata[j].longitude)      
              ratings.push(data[i].rating)
              // get average salary for each company
              salary.push((Number(data[i].salary.split("-")[0].replace(/[^0-9.-]+/g,""))+Number(data[i].salary.split("-")[1].replace(/[^0-9.-]+/g,"")))/2)
              salarydict.push({"city":city=data[i].location,"salary":(Number(data[i].salary.split("-")[0].replace(/[^0-9.-]+/g,""))+Number(data[i].salary.split("-")[1].replace(/[^0-9.-]+/g,"")))/2}) 
          }
        }
      }
    
    //  get unique city data and unique latitude, unique longitude data to create city marker
    function onlyUnique(value, index, self) {
        return self.indexOf(value) === index;
       }
    var uniquecity=cities.filter(onlyUnique);
    var uniquelatitude=latitudes.filter(onlyUnique);
    var uniquelongitude=longitudes.filter(onlyUnique);
    // get company count at each city     
    var dic={}
    for(c=0;c<cities.length;c++){
       if (!dic.hasOwnProperty(cities[c])){
        dic[cities[c]]=1;
      }
      else{dic[cities[c]]++}; 
      } 
    var dic2=[];
    for (var key in dic){
      dic2.push({name:key,count:dic[key]});
   }
    // get sum of rating
    var result = [];
    data.reduce(function(res, value) {
      if (!res[value.location]) {
        res[value.location] = { city: value.location, rating: 0 };
        result.push(res[value.location])
        }
      res[value.location].rating += value.rating;
      return res;
      }, {});

    // get sum of salary
    var salaryresult=[];
    salarydict.reduce(function(res,value){
    if(!res[value.city]){
     res[value.city]={city:value.city,salary:0};
     salaryresult.push(res[value.city])
      }
    res[value.city].salary+=value.salary;
    return res;
    },{});       
      // Create the outdoors tile layer
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
      // Add city circle marker to myMap
      var citymarker=[];
      var color="";
      for (q=0;q<uniquecity.length;q++){
        if (Math.round(result[q].rating/dic2[q].count)==-1|Math.round(result[q].rating/dic2[q].count)==1){
              color="#BB8FCE";
            }
        else if (Math.round(result[q].rating/dic2[q].count)==2|Math.round(result[q].rating/dic2[q].count)==3){
              color="#2ECC71";
            }
        else if (Math.round(result[q].rating/dic2[q].count)==4|Math.round(result[q].rating/dic2[q].count)==5){
              color="#17202A";
            }   
        citymarker.push(L.circleMarker([uniquelatitude[q],uniquelongitude[q]],{
              radius:Math.round(salaryresult[q].salary/dic2[q].count)/2,
              color:color,
              stroke:false,
              fillcolor:color,
              opacity:0.1,
              fillopacity:0.1,
              weight:1
            }).bindPopup(result[q].city+"<hr>Data Company Number: "+dic2[q].count+"<br>Average Data Company Rating: "+ Math.round(result[q].rating/dic2[q].count)+"<br>Average Data Job Salary: $"+Math.round(salaryresult[q].salary/dic2[q].count)+"K"))
          }
        L.layerGroup(citymarker).addTo(myMap);        
      // Add engineer marker
      var engineerlatitude=[];
      var engineerlongitude=[];
      var engineercity=[];
      for (n=0;n<data.length;n++){
        for (o=0;o<codata.length;o++){
          if (data[n].location.split(",")[0]===codata[o].city&&data[n].location.split(",")[1].charAt(1)===codata[o].state.charAt(0)&&data[n].position.includes("Engineer")){
                 engineerlatitude.push(codata[o].latitude)
                 engineerlongitude.push(codata[o].longitude)
                 engineercity.push(data[n].location)
                  }}}
      var engineermarker=[];
      for(p=0;p<engineerlatitude.length;p++){
        engineermarker.push(L.circleMarker([engineerlatitude[p],engineerlongitude[p]],{
          radius:"10",
          color:"#C0392B",
          stroke:false,
          opacity:0.1,
          fillcolor:"#C0392B",
          weight:0.1,
          fillopacity:0.1
        }))};
        L.layerGroup(engineermarker).addTo(myMap);
       //Add analyst marker 
        var analystlatitude=[];
        var analystlongitude=[];
        var analystcity=[];
        for (i=0;i<data.length;i++){
          for (j=0;j<codata.length;j++){
            if (data[i].location.split(",")[0]===codata[j].city&&data[i].location.split(",")[1].charAt(1)===codata[j].state.charAt(0)&&data[i].position.includes("Analyst")){
                  analystlatitude.push(codata[j].latitude)
                  analystlongitude.push(codata[j].longitude)
                  analystcity.push(data[i].location)           
        }}}
        var analystmarker=[];
        for(h=0;h<analystlatitude.length;h++){
          analystmarker.push(L.circleMarker([analystlatitude[h],analystlongitude[h]],{
            radius:"10",
            color:"#F1C40F",
            stroke:false,
            opacity:0.1,
            fillcolor:"#F1C40F",
            weight:0.1,
            fillopacity:0.1
          }))};
          L.layerGroup(analystmarker).addTo(myMap);
        // Add scientist marker
        var scientistlatitude=[];
        var scientistlongitude=[];
        var scientistcity=[];
        for (k=0;k<data.length;k++){
          for (l=0;l<codata.length;l++){
            if (data[k].location.split(",")[0]===codata[l].city&&data[k].location.split(",")[1].charAt(1)===codata[l].state.charAt(0)&&data[k].position.includes("Scientist")){
                   scientistlatitude.push(codata[l].latitude)
                   scientistlongitude.push(codata[l].longitude)
                   scientistcity.push(data[k].location)    
              }}}
       var scientistmarker=[];
        for(m=0;m<scientistlatitude.length;m++){
          scientistmarker.push(L.circleMarker([scientistlatitude[m],scientistlongitude[m]],{
            radius:"10",
            color:"#3498DB",
            stroke:false,
            opacity:0.1,
            fillcolor:"#3498DB",
            weight:0.1,
            fillopacity:0.1
          }))};
          L.layerGroup(scientistmarker).addTo(myMap);    
        //Create legend to indicate the color of the circle marker
        var legend=L.control({position:"bottomright"});
        legend.onAdd=function(){
            var div=L.DomUtil.create("div","info legend");
            var categories=["#85C1E9","#F4D03F","#F1948A","#D7BDE2","#A3E4D7","#ABB2B9"];
            var labels=[];
            var legendInfo="<div class=\"labels\">"+"</div>";
            div.innerHTML=legendInfo;
           
                labels.push(
                "<li style=\"background-color:"+categories[0]+"\"></li>   "+"Distribution of Data Scientist (color deeper, company number larger)"+"<br>"
                +"<li style=\"background-color:"+categories[1]+"\"></li>  "+"Distribution of Data Engineer (color deeper, company number larger)"+"<br>"
                +"<li style=\"background-color:"+categories[2]+"\"></li>  "+"Distribution of Data Analyst (color deeper, company number larger)"+"<br>"
                +"<li style=\"background-color:"+categories[3]+"\"></li>  "+"Data Company Average Rating -1--1 (circle larger, average salary higher)"+"<br>"
                +"<li style=\"background-color:"+categories[4]+"\"></li>  "+"Data Company Average Rating 2--3 (circle larger, average salary higher)"+"<br>"
                +"<li style=\"background-color:"+categories[5]+"\"></li>  "+"Data Company Average Rating 4--5 (circle larger, average salary higher)"+"<br>"
               );           
            
             div.innerHTML="<ul>"+labels.join("")+"</ul>";   
            return div;
        };
        legend.addTo(myMap);
    
   





    