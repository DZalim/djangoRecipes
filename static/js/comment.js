document.addEventListener('DOMContentLoaded', function () {
    const commentForm = document.querySelector('.add-comment-form form');
    const commentsSection = document.querySelector('.comment-section');

    if (commentForm) {
        commentForm.addEventListener('submit', function (event) {
            event.preventDefault(); //

            const url = commentForm.getAttribute('action');
            const formData = new FormData(commentForm);

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {

                    const newComment = document.createElement('div');
                    newComment.classList.add('comment-box');
                    newComment.innerHTML = `
                        <div class="comment-header">
                            <h3>${data.user}</h3>
                            <span>${data.created_at}</span>
                        </div>
                        <p>${data.description}</p>
                    `;

                    commentsSection.appendChild(newComment);

                    newComment.scrollIntoView({ behavior: 'smooth' });

                    commentForm.reset();
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
