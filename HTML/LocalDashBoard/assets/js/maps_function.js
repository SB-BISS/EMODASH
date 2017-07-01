

/**
 * 
 * JS object for the manipulation of maps.
 * 
 */


maps_obj = {
            


generatePoints: function(lon ,lat){
	
	LonLats = [];
	for(var i=0; i<10;i++){
	  for(var j = 0; j<10;j++){
		lon = lon + Math.random()*0.01 * ((Math.random() - 0.5)*2);
		lat= lat + Math.random()*0.01 * ((Math.random() - 0.5)*2);
	  
		var lonLat = new OpenLayers.LonLat( lon ,lat).transform(
	            new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
	            map.getProjectionObject() // to Spherical Mercator Projection
	          );
		LonLats.push(lonLat);
	  }
	}	
	
	return LonLats;

},



	initMapMarkers: function(){
	
	//MAP IS A GLOBAL VARIABLE
	 map = new OpenLayers.Map("map");
     map.addLayer(new OpenLayers.Layer.OSM());
     zoom = 16
     var lonLat = new OpenLayers.LonLat(5.29,52.2 ).transform(
            new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
            map.getProjectionObject() // to Spherical Mercator Projection
          );
     
     console.log(lonLat);
     map.setCenter(lonLat,zoom);
     
	 var location = 'Heerlen,Limburg';

	 // we are using MapQuest's Nominatim service
    //http://nominatim.openstreetmap.org/search?q=135+pilkington+avenue,+birmingham&format=json&polygon=1&addressdetails=1
	 var geocode = ' http://nominatim.openstreetmap.org/search?q=' + location + "&format=json&addressdetails=1";

	 // use jQuery to call the API and get the JSON results
	 $.getJSON(geocode, function(data) {
		 
		  // get lat + lon from first match
		  console.log(data);
		  
		   LonLatsH = maps_obj.generatePoints(parseFloat(data[0]['lon']) ,parseFloat(data[0]['lat']));
		   LonLatsS = maps_obj.generatePoints(parseFloat(data[0]['lon']) ,parseFloat(data[0]['lat']));

		   var lonLat = new OpenLayers.LonLat( parseFloat(data[0]['lon']) ,parseFloat(data[0]['lat'])).transform(
            new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
            map.getProjectionObject() // to Spherical Mercator Projection
            );
		    
           var markers = new OpenLayers.Layer.Markers( "Markers" );
	 	   map.addLayer(markers);
		  
	 	   var zoom=13;
	 	   
	 	    map.setCenter (lonLat, zoom);
	 	    
	 	   var icon = new OpenLayers.Icon('http://www.clker.com/cliparts/m/L/6/g/k/2/blue-smiley-face-md.png', size, offset);
	 	  var icon2 = new OpenLayers.Icon('https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Gnome3-surprise.svg/1000px-Gnome3-surprise.svg.png', size, offset);
	 	   
	 	   for(var i =0; i<LonLatsH.length;i++){
	 		  
	 		   var size = new OpenLayers.Size(40,40);
	 		  var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);

	 		  
	 		  var mymarker = new OpenLayers.Marker(LonLatsH[i],icon.clone());
	 		   
	 		  
	 		   markers.addMarker(mymarker);
    
	 	   }
	 	   
	 	    for(var i =0; i<LonLatsS.length;i++){
	 		  
	 		   var size = new OpenLayers.Size(40,40);
	 		  var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);

	 		  
	 		  var mymarker = new OpenLayers.Marker(LonLatsS[i],icon2.clone());
	 		   
	 		  
	 		   markers.addMarker(mymarker);
    
	 	   }


	 });
	 
	 
		 // get lat + lon from first match
    // var latlng = [data[0].lat, data[0].lon]];
	 //console.log(latlng);
	 //map.getView().setCenter(latlng);
     // let's stringify it
     //var latlngAsString = latlng.join(',');
  //console.log(latlngAsString);

  // the full results JSON
  //console.log(data);
	 //});
	 
	
}

	
	

/*addCustomersMap:function(){
	
		$.ajax({
			type: "GET",
			url: "http://localhost:8080/get_customer_ids",
			dataType: "json",
			processData: false
		 }).done(function(result) 
		{	
			
		}
		

}*/



}