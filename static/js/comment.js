document.addEventListener('DOMContentLoaded', function () {
    const commentForm = document.querySelector('.add-comment-form form');
    const commentsContainer = document.querySelector('.comments-container');

    if (commentForm) {
        commentForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const recipeId = commentForm.dataset.recipeId;
            const commentText = commentForm.querySelector('textarea[name="description"]').value;

            const apiUrl = `/${recipeId}/comment/`;

            const formatDate = (isoDate) => {
                const date = new Date(isoDate);
                let formattedDate = new Intl.DateTimeFormat('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric',
                    hour: 'numeric',
                    minute: 'numeric',
                    hour12: true,
                }).format(date);

                formattedDate = formattedDate.replace(' AM', ' a.m.').replace(' PM', ' p.m.');
                return formattedDate.replace(/^(\w+)/, '$1.');
            };

            fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({description: commentText}),
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to create comment');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        const escapeHTML = (text) => {
                            const map = {
                                '&': '&amp;',
                                '<': '&lt;',
                                '>': '&gt;',
                                '"': '&quot;',
                                "'": '&#39;'
                            };
                            return text.replace(/[&<>"']/g, (char) => map[char]);
                        };

                        const newComment = document.createElement('div');
                        newComment.classList.add('comment-box');
                        newComment.setAttribute('data-comment-id', data.id);

                        const escapedDescription = escapeHTML(data.description);
                        newComment.innerHTML = `
                        <div class="comment-header">
                            <h3>${data.user}</h3>
                            <span>${formatDate(data.created_at)}</span>
                        </div>
                        <p class="comment-text">${escapedDescription}</p>
                    `;

                     newComment.innerHTML += `
                        <div class="comment-actions">
                            <form action="/${recipeId}/comment/${data.id}/" class="comment-edit-form">
                                <button type="button" class="edit-comment-btn" 
                                        data-recipe-id="${recipeId}" 
                                        data-comment-id="${data.id}" 
                                        data-description="${escapedDescription}">
                                    <i class="fa-solid fa-pen"></i>
                                </button>
                            </form>
                            <form action="/${recipeId}/comment/${data.id}/" class="comment-delete-form">
                                <button type="button" class="delete-comment-btn" 
                                        data-recipe-id="${recipeId}" 
                                        data-comment-id="${data.id}">
                                    <i class="fa-solid fa-trash"></i>
                                </button>
                            </form>
                        </div>
                    `;


                        commentsContainer.prepend(newComment);
                        newComment.scrollIntoView({behavior: 'smooth'});

                        // Attach dynamic events for edit and delete actions
                        const editButton = newComment.querySelector('.edit-comment-btn');
                        const deleteButton = newComment.querySelector('.delete-comment-btn');

                        // Update edit and delete button events dynamically
                        editButton.addEventListener('onclick', () => {
                            openEditCommentModal(recipeId, data.id, data.description);
                        });

                        deleteButton.addEventListener('onclick', () => {
                            openDeleteCommentModal(recipeId, data.id);
                         });

                        commentForm.reset();
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while adding the comment.');
                });

        });
    }
});

function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
