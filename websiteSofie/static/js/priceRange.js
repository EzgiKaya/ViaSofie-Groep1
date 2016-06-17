$(function() {
  $( "#slider-range" ).slider({
    range: true,
    min: 0,
    max: 2000000,
    values: [ 0, 20000000 ],
    slide: function( event, ui ) {
      $( "#amount" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
      console.log($('#amount').val());
    }
  });
  $( "#amount" ).val( $( "#slider-range" ).slider( "values", 0 ) +
    " - " + $( "#slider-range" ).slider( "values", 1 ) );
});
