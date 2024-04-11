document.addEventListener('DOMContentLoaded', function () {
        var close = document.querySelector('.close');
        var modal = document.getElementById('errorModal');
        close.onclick = function() {
            modal.style.display = 'none';
        }
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
    });