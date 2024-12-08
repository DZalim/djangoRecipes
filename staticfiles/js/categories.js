let currentCategoryId = null;

// CSRF Token Helper
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Open Delete Modal
function openDeleteCategoryModal(categoryId) {
    currentCategoryId = categoryId;
    document.getElementById('categoryDeleteModal').style.display = 'flex';
}

// Close Delete Modal
function closeDeleteCategoryModal() {
    currentCategoryId = null;
    document.getElementById('categoryDeleteModal').style.display = 'none';
}

// Confirm Category Delete
function confirmCategoryDelete() {
    if (!currentCategoryId) return;

    const deleteUrl = `/category/${currentCategoryId}/`;

    fetch(deleteUrl, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCsrfToken()
        }
    })
        .then(response => {
            if (response.status === 204) {
                document.querySelector(`.category-box[data-category-id="${currentCategoryId}"]`).remove();
                closeDeleteCategoryModal();
            } else {
                return response.json();
            }
        })
        .then(data => {
            if (data && data.error) {
                alert('Error deleting category: ' + data.error);
            }
        })
        .catch(error => console.error('Error:', error));
}

// Open Edit Modal
function openEditCategoryModal(categoryId, categoryName) {
    currentCategoryId = categoryId;

    const currentText = document.querySelector(`.category-box[data-category-id="${categoryId}"] .category-name`).innerText;

    const modalTextarea = document.getElementById('editCategoryText');

    if (modalTextarea) {
        modalTextarea.value = currentText.trim();
        modalTextarea.dataset.originalCategoryName = currentText.trim()
    }

    const editModal = document.getElementById('categoryEditModal');
    if (editModal) {
        editModal.style.display = 'flex';
    }
}

// Close Edit Modal
function closeEditCategoryModal() {
    currentCategoryId = null;
    document.getElementById('categoryEditModal').style.display = 'none';
}

// Confirm Category Edit
function confirmEditCategory() {
    const modalTextarea = document.getElementById('editCategoryText');
    const newName = modalTextarea.value;


    if (newName === modalTextarea.dataset.originalCategoryName) {
        console.log('No changes were made.');
        return closeEditCategoryModal();
    }

    const editUrl = `/category/${currentCategoryId}/`;

    fetch(editUrl, {
        method: 'PUT',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ category_name: newName })
    })
        .then(response => {
            if (response.status === 200) {
                return response.json();
            } else if (response.status === 400) {
                return response.json().then(data => {
                    throw new Error(data.category_name?.[0] || "An error occurred.");
                });
            } else {
                throw new Error("An unexpected error occurred.");
            }
        })
        .then(data => {
            if (data.category_name === newName) {
                const categoryTextElement = document.querySelector(`.category-box[data-category-id="${currentCategoryId}"] .category-name`);
                if (categoryTextElement) {
                    categoryTextElement.innerText = newName;
                }
                closeEditCategoryModal();
            }

        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message);
        });
}
