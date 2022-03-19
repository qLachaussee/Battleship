/// Fonction permettant de controler que le joueur ne place pas plus de 3 bateaux, sinon un pop-up le remmetra en ordre
function chkcontrol(j) {
    var checkboxes = document.querySelectorAll('input[type=checkbox]')
    var total = 0;
    for(var i=0; i < checkboxes.length; i++)
    {
        if(checkboxes[i].checked)
        {
        total = total + 1;
        }
        if(total > 3){
        alert("Faut 3 bateaux mec, pas " + total + ".\n\nFais un effort, merde !") 
        checkboxes[j].checked = false ;
        return false;
        }
    }
}

/// Fonction permettant de controler que le joueur ait bien placé ses 3 bateaux avant de commencer à jouer, sinon un pop-up le remmetra en ordre
function valider() {
    var checkboxes = document.querySelectorAll('input[type=checkbox]')
    var total = 0;
    for(var i=0; i < checkboxes.length; i++)
    {
        if(checkboxes[i].checked)
        {
        total = total + 1;
        }
    }
    if(total != 3){
        alert("Faut 3 bateaux mec, pas " + total + ".\n\nFais un effort, merde !") 
        return false;
    }
}

