    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    document.querySelectorAll('.star').forEach(star => {
    star.addEventListener('click', function() {
        const productId = document.querySelector('.stars').dataset.productId;
        const rating = this.dataset.value;

        fetch(`/rate_product/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,  // добавляем CSRF токен
            },
            body: JSON.stringify({ rating: rating }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Rating updated!');
                } else {
                    alert('Error: ' + data.error);
                }
            });
    });
});

