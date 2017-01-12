



jQuery(document).ready(function(){setInterval(function(){jQuery("#refresh").load('{% url "adminUser:tableview" %}');
   },6000)
       });