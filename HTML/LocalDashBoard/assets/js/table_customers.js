demo.customer_id='';
demo.agent_id='';

table_customers = {
    initTableValues: function(){
	
				$.ajax({
					type: "GET",
					url: "http://localhost:8080/get_customer_ids",
					dataType: "json",
					processData: false
				 }).done(function(result) 
				{
						var myObj = result;
						console.log(myObj);
						
						var table_body= document.getElementById('table_body');

						for(i=0; i<myObj.length; i++){
						
							var TR = document.createElement('TR');	
							var TD = document.createElement('TD');	
							TR.id = myObj[i];
							TD.innerHTML = myObj[i];
							
							TR.appendChild(TD);
							table_body.appendChild(TR);
							
						
						}
				
						//Appends a function to the table
						$("#table_body tr").click(function(){
						 	 $(this).addClass('selected').siblings().removeClass('selected');    
						 	localStorage.setItem('customer_id',$(this).find('td:first').html()); //security check here.
						  	alert(localStorage.getItem('customer_id'));    
						  });
						
						 $('.ok').on('click', function(e){
						 	  alert($("#table tr.selected td:first").html());
						 });
				
					

				 })
    
		 }  
    
    
}


