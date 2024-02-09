function goBack() {
    window.history.back();
  }

function doVisible() {
    
    document.addEventListener('DOMContentLoaded', function() {
      // Get the element by its ID
      var myElement = document.getElementById("recordsContainer");

      // Change the display property to 'block' to make it visible
      myElement.style.display = 'block';
  });
}
