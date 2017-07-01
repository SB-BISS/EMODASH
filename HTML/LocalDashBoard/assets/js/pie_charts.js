


pie_charts = {
              
initPieCharts: function(){
	
	//console.log("http://localhost:8080/customer_lastcall?customer_id="+localStorage.getItem("customer_id"));

	$.ajax({
				type: "GET",
				url: "http://localhost:8080/customer_lastcall?customer_id="+localStorage.getItem("customer_id"),
				dataType: "json",
				processData: false
			 }).done(function(result) 
			{
					var myObj = result;
					
		
					  var myObj = result;
					
						
						var ctx = document.getElementById("CustomerChart");
						var myChart = new Chart(ctx, {
							type: 'horizontalBar',
							data: {
							labels: ["Anger", "Surprise", "Happiness", "Neutral", "Sadness", "Fear", "Disgust"],
							datasets: [{
								label: 'EMODASH',
								data: [Math.round(myObj['anger']*100)/100, Math.round(myObj['surprise']*100)/100,
								       Math.round(myObj['happiness']*100)/100,  Math.round(myObj['neutral']*100)/100, 
								       Math.round(myObj['sadness']*100)/100, Math.round(myObj['fear']*100)/100,
								       Math.round(myObj['disgust']*100)/100],
                          backgroundColor: [
                              'rgba(255, 0, 0, 0.2)',
                              'rgba(253, 153, 0, 0.2)',
                              'rgba(0, 255, 255, 0.2)',
                              'rgba(216, 216, 216, 0.2)',
                              'rgba(0, 0, 255, 0.2)',
                              'rgba(0, 255, 0, 0.2)',
                              'rgba(255, 0, 255, 0.2)'
                          ],
                          borderColor: [
                              'rgba(255, 0, 0, 0.2)',
                              'rgba(253, 153, 0, 0.2)',
                              'rgba(0, 255, 255, 0.2)',
                              'rgba(216, 216, 216, 0.2)',
                              'rgba(0, 0, 255, 0.2)',
                              'rgba(0, 255, 0, 0.2)',
                              'rgba(255, 0, 255, 0.2)'
                          ],
                          borderWidth: 1
                      }]
                  },
                  options: {
                      scales: {
                          yAxes: [{
                              ticks: {
                                  beginAtZero:true
                              }
                          }]
                      }
                  }
              });




				});


		$.ajax({
				type: "GET",
				url: "http://localhost:8080/agent_lastcall?agent_id="+localStorage.getItem("agent_id"),
				dataType: "json",
				processData: false
			 }).done(function(result) 
			{
					var myObj = result;
					
						
						var ctx = document.getElementById("AgentChart");
						var myChart = new Chart(ctx, {
							type: 'horizontalBar',
							data: {
							labels: ["Anger", "Surprise", "Happiness", "Neutral", "Sadness", "Fear", "Disgust"],
							datasets: [{
								label: 'EMODASH',
								data: [Math.round(myObj['anger']*100)/100, Math.round(myObj['surprise']*100)/100,
								       Math.round(myObj['happiness']*100)/100,  Math.round(myObj['neutral']*100)/100, 
								       Math.round(myObj['sadness']*100)/100, Math.round(myObj['fear']*100)/100,
								       Math.round(myObj['disgust']*100)/100],
                          backgroundColor: [
                              'rgba(255, 0, 0, 0.2)',
                              'rgba(253, 153, 0, 0.2)',
                              'rgba(0, 255, 255, 0.2)',
                              'rgba(216, 216, 216, 0.2)',
                              'rgba(0, 0, 255, 0.2)',
                              'rgba(0, 255, 0, 0.2)',
                              'rgba(255, 0, 255, 0.2)'
                          ],
                          borderColor: [
                             'rgba(255, 0, 0, 0.2)',
                              'rgba(253, 153, 0, 0.2)',
                              'rgba(0, 255, 255, 0.2)',
                              'rgba(216, 216, 216, 0.2)',
                              'rgba(0, 0, 255, 0.2)',
                              'rgba(0, 255, 0, 0.2)',
                              'rgba(255, 0, 255, 0.2)'
                          ],
                          borderWidth: 1
                      }]
                  },
                  options: {
                      scales: {
                          yAxes: [{
                              ticks: {
                                  beginAtZero:true
                              }
                          }]
                      }
                  }
              });


				});

	
},


updateActiveCharts: function(entity,anger,surprise,happiness,neutral,sadness,fear,disgust){

 var data = {
          labels: ['3','6','9','12','15','18','21','24','27','30'],    
          series: [
            anger,
            surprise,
            happiness,
            neutral,
            sadness,
            fear,
            disgust
          ]
        };
        
         var optionsSales = {
          lineSmooth: false,
          low: 0,
          high: 1,
          showArea: false,
          height: "245px",
          axisX: {
            showGrid: false,
          },
          lineSmooth: Chartist.Interpolation.simple({
            divisor: 3
          }),
          showLine: true,
          showPoint: true,
        };
        
        var responsiveSales = [
          ['screen and (max-width: 640px)', {
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];
        
     Chartist.Line("#chartEmotions"+entity, data, optionsSales, responsiveSales);


},



plotActiveWidget:function(Series){
	
var ctx = document.getElementById("myChart");
						var myChart = new Chart(ctx, {
							type: 'horizontalBar',
							data: {
							labels: ["Anger", "Surprise", "Happiness", "Neutral", "Sadness", "Fear", "Disgust"],
							datasets: [{
								label: 'EMODASH',
								data: Series,
                          backgroundColor: [
                              'rgba(255, 0, 0, 0.2)',
                              'rgba(253, 153, 0, 0.2)',
                              'rgba(0, 255, 255, 0.2)',
                              'rgba(216, 216, 216, 0.2)',
                              'rgba(0, 0, 255, 0.2)',
                              'rgba(0, 255, 0, 0.2)',
                              'rgba(255, 0, 255, 0.2)'
                          ],
                          borderColor: [
                              'rgba(255, 0, 0, 0.2)',
                              'rgba(253, 153, 0, 0.2)',
                              'rgba(0, 255, 255, 0.2)',
                              'rgba(216, 216, 216, 0.2)',
                              'rgba(0, 0, 255, 0.2)',
                              'rgba(0, 255, 0, 0.2)',
                              'rgba(255, 0, 255, 0.2)'
                          ],
                          borderWidth: 1
                      }]
                  },
                  options: {
                      scales: {
                          yAxes: [{
                              ticks: {
                                  beginAtZero:true
                              }
                          }]
                      }
                  }
              });




},



initActiveWidget:function(entity){

	 $.ajax({
				type: "GET",
				url: "http://localhost:8080/get_call_id_with_customer?agent_id="+localStorage.getItem("agent_id") + '&customer_id='+localStorage.getItem("customer_id"),
				dataType: "json",
				processData: false
			 }).done(function(result) 
			{
				mycurrentcall = result['call_id'];
		
				//console.log(mycurrentcall);
			//NESTED AJAX CALL
         $.ajax({
				type: "GET",
				url: "http://localhost:8080/customer_emotions_live?call_id="+mycurrentcall + '&customer_id='+localStorage.getItem(entity+"_id"),
				dataType: "json",
				processData: false
			 }).done(function(result2) 
			{
				
			
				 var anger = [];	
				 var happiness = [];
				 var disgust = [];
				 var neutral = [];
				 var sadness = [];
				 var fear = [];
				 var surprise = [];
				 var myObj = result2;
				
				for(i=0;i<myObj.length;i++){
						
						SingleEmotionObj = myObj[i];
						//console.log(""+SingleEmotionObj['Emotiontype']);
						if(SingleEmotionObj['Emotiontype'] == 'anger'){
							
						 anger.push(SingleEmotionObj['value'])
						}
						
						if(SingleEmotionObj['Emotiontype'] == 'happiness'){
							
						 happiness.push(SingleEmotionObj['value'])
						}
						
						if(SingleEmotionObj['Emotiontype'] == 'neutral'){
							
						 neutral.push(SingleEmotionObj['value'])
						}

						if(SingleEmotionObj['Emotiontype'] == 'disgust'){
							
						 disgust.push(SingleEmotionObj['value'])
						}
						
						if(SingleEmotionObj['Emotiontype'] == 'sadness'){
							
						 sadness.push(SingleEmotionObj['value'])
						}
						
						if(SingleEmotionObj['Emotiontype'] == 'fear'){
							
						 fear.push(SingleEmotionObj['value'])
						}
						
						if(SingleEmotionObj['Emotiontype'] == 'surprise'){
							
						 surprise.push(SingleEmotionObj['value'])
						}

				}
				
				if(anger.length>=1){
					Series = [anger[anger.length-1], 
			         surprise[surprise.length-1],
					 happiness[happiness.length-1],  
					 neutral[neutral.length-1], 
					 sadness[sadness.length-1], 
					 fear[fear.length-1],
					 disgust[disgust.length-1]];
					
				}
			 
			 pie_charts.plotActiveWidget(Series)
			 setTimeout(function(){pie_charts.initActiveWidget(entity)}, 2000);
			
			});

			
	
	});
			
			





},



initActiveCharts: function(entity){
	
 
//http://localhost:8080/customer_emotions_live?call_id=645dfb70-e048-4174-b473-3c32cf6acc52&customer_id=c0
//http://localhost:8080/get_call_id_with_customer?customer_id=c0&agent_id=ag1
 var mycurrentcall = '';

       $.ajax({
				type: "GET",
				url: "http://localhost:8080/get_call_id_with_customer?agent_id="+localStorage.getItem("agent_id") + '&customer_id='+localStorage.getItem("customer_id"),
				dataType: "json",
				processData: false
			 }).done(function(result) 
			{
				mycurrentcall = result['call_id'];
		
				//console.log(mycurrentcall);
			//NESTED AJAX CALL


         $.ajax({
				type: "GET",
				url: "http://localhost:8080/customer_emotions_live?call_id="+mycurrentcall + '&customer_id='+localStorage.getItem(entity+"_id"),
				dataType: "json",
				processData: false
			 }).done(function(result2) 
			{
				
			
				 var anger = [];	
				 var happiness = [];
				 var disgust = [];
				 var neutral = [];
				 var sadness = [];
				 var fear = [];
				 var surprise = [];
				 var myObj = result2;
				
				for(i=0;i<myObj.length;i++){
						
						SingleEmotionObj = myObj[i];
						//console.log(""+SingleEmotionObj['Emotiontype']);
						if(SingleEmotionObj['Emotiontype'] == 'anger'){
							
						 anger.push(SingleEmotionObj['value'])
						}
						
						if(SingleEmotionObj['Emotiontype'] == 'happiness'){
							
						 happiness.push(SingleEmotionObj['value'] )
						}
						
						if(SingleEmotionObj['Emotiontype'] == 'neutral'){
							
						 neutral.push(SingleEmotionObj['value'])
						}

						if(SingleEmotionObj['Emotiontype'] == 'disgust'){
							
						 disgust.push(SingleEmotionObj['value'])
						}
						
						if(SingleEmotionObj['Emotiontype'] == 'sadness'){
							
						 sadness.push(SingleEmotionObj['value'])
						}
						
						if(SingleEmotionObj['Emotiontype'] == 'fear'){
							
						 fear.push(SingleEmotionObj['value'])
						}
						
						if(SingleEmotionObj['Emotiontype'] == 'surprise'){
							
						 surprise.push(SingleEmotionObj['value'])
						}

				}
					
				pie_charts.updateActiveCharts(entity,anger,surprise,happiness,neutral,sadness,fear,disgust);
				setTimeout(function(){pie_charts.initActiveCharts(entity)}, 2000);
			});


});
       

                   


}






}