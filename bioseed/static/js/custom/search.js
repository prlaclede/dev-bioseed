$(function (search, $, undefined) {
    
    $('body')
            
            .change('#searchOptions', function() {
                console.log($('#searchOptions').val());
                var selectedOption = $('#searchOptions').val();
                if (!$('#searchParams').html().length) {
                    $('#searchParams').append($('#searchOptions').val());
                } else {
                   $('#searchParams').append(', ' + $('#searchOptions').val()); 
                }
                $("option[value='" + selectedOption + "']").prop('disabled', true);
            })
            
            .on('click', '#clearSearchParams', function() {
                $('#searchParams').empty();
                $('#searchOptions > option').each(function() {
                    $(this).prop('disabled', false);
                });
                
            })
    
}( window.search = window.search || {}, jQuery ));