let currentCommentId = null;
let currentRecipeId = null;

// CSRF Token Helper
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Open Delete Modal
function openDeleteCommentModal(recipeId, commentId) {
    currentRecipeId = recipeId;
    currentCommentId = commentId;
    document.getElementById('commentDeleteModal').style.display = 'flex';
}

// Close Delete Modal
function closeDeleteCommentModal() {
    currentCommentId = null;
    document.getElementById('commentDeleteModal').style.display = 'none';
}

// Confirm Comment Delete
function confirmCommentDelete() {
    if (!currentCommentId) return;

    const deleteUrl = `/${currentRecipeId}/comment/${currentCommentId}/`;

    fetch(deleteUrl, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCsrfToken()
        }
    })
        .then(response => {
            if (response.status === 204) {
                document.querySelector(`.comment-box[data-comment-id="${currentCommentId}"]`).remove();
                closeDeleteCommentModal();
            } else {
                return response.json();
            }
        })
        .then(data => {
            if (data && data.error) {
                alert('Error deleting comment: ' + data.error);
            }
        })
        .catch(error => console.error('Error:', error));
}

// Open Edit Modal
function openEditCommentModal(recipeId, commentId, description) {
    currentRecipeId = recipeId;
    currentCommentId = commentId;

    const currentText = document.querySelector(`.comment-box[data-comment-id="${commentId}"] .comment-text`).innerText;

    const modalTextarea = document.getElementById('editCommentText');

    if (modalTextarea) {
        modalTextarea.value = currentText.trim();
    }

    const editModal = document.getElementById('commentEditModal');
    if (editModal) {
        editModal.style.display = 'flex';
    }
}

// Close Edit Modal
function closeEditCommentModal() {
    currentCommentId = null;
    document.getElementById('commentEditModal').style.display = 'none';
}

// Confirm Comment Edit
function confirmEditComment() {
    const modalTextarea = document.getElementById('editCommentText');
    const newDescription = modalTextarea.value;

    if (newDescription === modalTextarea.dataset.originalDescription) {
        console.log('No changes were made.');
        return closeEditCommentModal();
    }

    const editUrl = `/${currentRecipeId}/comment/${currentCommentId}/`;

    fetch(editUrl, {
        method: 'PUT',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ description: newDescription })
    })
        .then(response => {
            if (response.status === 200) {
                return response.json();
            } else {
                return response.text();
            }
        })
        .then(data => {
            if (data.success === true) {
                const commentTextElement = document.querySelector(`.comment-box[data-comment-id="${currentCommentId}"] .comment-text`);
                if (commentTextElement) {
                    commentTextElement.innerText = newDescription;
                }
                closeEditCommentModal();
            } else {
                alert('Error editing comment.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while editing the comment.');
        });
}

// Add Comment
document.addEventListener('DOMContentLoaded', function () {
    const commentForm = document.querySelector('.add-comment-form form');
    const commentsContainer = document.querySelector('.comments-container');

    if (commentForm) {
        commentForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const recipeId = commentForm.dataset.recipeId;
            const commentText = commentForm.querySelector('textarea[name="description"]').value;

            const apiUrl = `/${recipeId}/comment/`;

            fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({ description: commentText }),
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
                            
                            <div class="comment-actions">
                                <form class="comment-edit-form" onsubmit="return false;">
                                    <button type="button" class="edit-comment-btn" 
                                            onclick="openEditCommentModal(${recipeId}, ${data.id}, '${escapedDescription}')">
                                        <i class="fa-solid fa-pen"></i>
                                    </button>
                                </form>
                                <form class="comment-delete-form" onsubmit="return false;">
                                    <button type="button" class="delete-comment-btn" 
                                            onclick="openDeleteCommentModal(${recipeId}, ${data.id})">
                                        <i class="fa-solid fa-trash"></i>
                                    </button>
                                </form>
                            </div>
                        `;

                        commentsContainer.prepend(newComment);
                        newComment.scrollIntoView({ behavior: 'smooth' });
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

// Escape HTML helper
function escapeHTML(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
    };
    return text.replace(/[&<>"']/g, (char) => map[char]);
}

// Format Date helper
function formatDate(isoDate) {
    const date = new Date(isoDate);
    return new Intl.DateTimeFormat('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true,
    })
        .format(date)
        .replace(' AM', ' a.m.')
        .replace(' PM', ' p.m.')
        .replace(/^(\w+)/, '$1.');
}
