function check(){
             var one=0;
             var two=0;
             var three=0;
             var four=0;
             var five=0;
             var six=0;
             var seven=0;
             var eight=0;
             var result="";
             var choice;
             for (var v=1; v<=5; v++)
             {
             var question = document.forms["quiz"].elements["vopros"+v];
              for (var i=0; i<question.length; i++)
              {
              if (question[i].checked) {
              choice=question[i].value;
              }
              }
              if (choice=="MERCURY") {one++;}
              if (choice=="VENUS") {two++;}
              if (choice=="EARTH") {three++;}
              if (choice=="MARS") {four++;}
              if (choice=="JUPITER") {five++;}
              if (choice=="SATURN") {six++;}
              if (choice=="URANUS") {seven++;}
              if (choice=="NEPTUN") {eight++;}
             }
             switch (true) {
             case (one==2): result="Вам следует полететь на Меркурий";break;
             case (two==2): result="Вам следует полететь на Венеру";break;
             case (three==2): result="Вам следует остаться на Земле";break;
             case (four==2): result="Вам следует полететь на Марс";break;
             case (five==2): result="Вам следует полететь на Юпитер";break;
             case (six==2): result="Вам следует полететь на Сатурн";break;
             case (seven==2): result="Вам следует полететь на Уран";break;
             case (eight==2): result="Вам следует полететь на Нептун";break;
             default: result="Вам следует остаться на Земле";break;
             }
             alert(result);
             document.getElementById("submit").innerHTML += "<br>" + result;
}

function next_question(){
    if(document.getElementById('quiz4').style.display == "block"){
        document.getElementById('quiz4').style.display = "none";
        document.getElementById('quiz5').style.display = "block";
        document.getElementById('kn_sl').style.display = "none";
        document.getElementById('submit').style.display = "block";
        }
    if(document.getElementById('quiz1').style.display == "block"){
        document.getElementById('quiz1').style.display = "none";
        document.getElementById('quiz2').style.display = "block";
        document.getElementById('submit').style.display = "none";
    }
    if(document.getElementById('quiz2').style.display == "block"){
        document.getElementById('quiz2').style.display = "none";
        document.getElementById('quiz3').style.display = "block";
    }
    if(document.getElementById('quiz3').style.display == "block"){
        document.getElementById('quiz3').style.display = "none";
        document.getElementById('quiz4').style.display = "block";
    }
}
document.getElementById("kn_sl").addEventListener("click", next_question());