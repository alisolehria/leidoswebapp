  function getTable(){
             jQuery("#refresh").load('{% url "adminUser:tableview" %}');
         }