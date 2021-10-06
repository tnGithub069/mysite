$(function () {
    window.onload = function() {
        $('#openModal').modal('show');
    }
    $('#openModal').click(function(){
        $('#modalArea').fadeIn();
    });
    $('#closeModal , #modalBg').click(function(){
      $('#modalArea').fadeOut();
    });
  });

