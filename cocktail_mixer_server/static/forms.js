function remove_recipe_row(index) {
    var row = document.getElementById('ingredient' + index);
    row.parentElement.removeChild(row);

    removed_elemtents++;

    decrement_ingredient_count();
}

function add_row() {
    var total_tries = removed_elemtents + parseInt(document.getElementById('total_ingredients').value, 10); 

    for(var i = 0; i < total_tries; i++) {
        var name = 'ingredient' + i;
        var element = document.getElementById(name);

        if(element != undefined) {
            clone = element.cloneNode(true);
            var cloneId = total_tries; 

            var select = document.getElementById('beverages' + i);
            select.id = 'beverages' + cloneId;
            select.name = 'beverage' + cloneId;

            var amount = document.getElementById('amount' + i);
            amount.id = 'amount' + cloneId;
            amount.name = 'amount' + cloneId;

            var button = document.getElementById('remove_button' + i)
            button.id = 'remove_button' + cloneId;

            document.getElementById('form_recipe').appendChild(clone);

            increment_ingredient_count();

            break;
        }
    }
}

function increment_ingredient_count() {
    var value = parseInt(document.getElementById('total_ingredients').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById('number').value = value;
}

function decrement_ingredient_count() {
    var value = parseInt(document.getElementById('total_ingredients').value, 10);
    value = isNaN(value) ? 0 : value;
    value--;
    document.getElementById('number').value = value;
}

var removed_elemtents = 0;

