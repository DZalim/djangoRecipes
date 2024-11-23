let currentCommentId = null;
let currentRecipeId = null;

function openDeleteCommentModal(recipeId, commentId) {
    currentRecipeId = recipeId;
    currentCommentId = commentId;
    document.getElementById('commentDeleteModal').style.display = 'flex';
}

function closeDeleteCommentModal() {
    currentCommentId = null;
    document.getElementById('commentDeleteModal').style.display = 'none';
}

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


function openEditCommentModal(recipeId, commentId, description) {
    currentRecipeId = recipeId;
    currentCommentId = commentId;
    document.getElementById('editCommentText').value = description;
    document.getElementById('commentEditModal').style.display = 'flex';
}

function closeEditCommentModal() {
    currentCommentId = null;
    document.getElementById('commentEditModal').style.display = 'none';
}

function confirmEditComment() {
    const newDescription = document.getElementById('editCommentText').value;

    const editUrl = `/${currentRecipeId}/comment/${currentCommentId}/`;

    fetch(editUrl, {
        method: 'PUT',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({description: newDescription})
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
                document.querySelector(`.comment-box[data-comment-id="${currentCommentId}"] .comment-text`).innerText = newDescription;
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

// CSRF Token Helper
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
