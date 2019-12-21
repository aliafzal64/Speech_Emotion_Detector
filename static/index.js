// Author: Ali Afzal

$( document ).ready(function() {
    console.log( "ready!" );

    $.ajax({
        type: 'GET',
        url: '/files',
        contentType: false,
        processData: false,
        dataType: 'json',
        success: function(data) {
            for(var file in data) {
                temp = data[file].split("/")
                filename = temp[temp.length-2] + '/' + temp[temp.length - 1]
                $('#sel1').append('<option>' + filename + '</option>')
            }
        }
    });

    $('select').on('change', function()
    {
        $('#audio').html('<audio controls><source src=\"static/data/' + this.value + '\" type=\"audio/mpeg\">Your browser does not support the audo element</audio>')
    });

    $('#predict-button').click( function() {
        event.preventDefault();

            var form_data = new FormData($('#uploadform')[0]);
            $('#predict-button').attr("disabled", true)
            $('#alert').html('')
            $('#cards').html('')
            $('#loading').html('<br><div class=\"spinner-border text-primary\" role=\"status\"> <span class=\"sr-only\">Loading...</span> </div>')
            $.ajax({
                type: 'POST',
                data: form_data,
                url: '/predict',
                contentType: false,
                processData: false,
                dataType: 'json',
                success: function(data) {
                    console.log(data)
                    if (data['status'] == 'success') {
                        $('#alert').html('<br><div class=\"alert alert-success\" role=\"alert\">  Success! </div>')
                        $('#loading').html("")
                        $('#predict-button').attr("disabled", false)

                        // display card
                        $('#cards').html('<div class=\"card\" style=\"width: 18rem;\"><img src=\"static/images/' + data['prediction'] + '.jpg\" class=\"card-img-top\"> <div class=\"card-body\"> <h5 class=\"card-title\">' + capitalize(data['prediction']) + '</h5> <p class=\"card-text\"> ' + (data['accuracy'] * 100) + '% Accuracy! </p> </div> </div>')
                    }
                },
                failure: function(data) {
                    console.log("failure")
                }
            })

        console.log("button clicked!")

    });
});

function capitalize(s)
{
    return s && s[0].toUpperCase() + s.slice(1);
}