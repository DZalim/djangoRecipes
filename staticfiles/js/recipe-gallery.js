document.addEventListener("DOMContentLoaded", function () {
    const photoContainers = document.querySelectorAll(".photo-container");
    const images = document.querySelectorAll(".recipe-image");
    const prevBtn = document.querySelector(".prev-btn");
    const nextBtn = document.querySelector(".next-btn");
    let currentIndex = 0;

    function showImage(index) {
        photoContainers.forEach((container, i) => {
            container.style.display = i === index ? "block" : "none";
        });
        images.forEach((img, i) => {
            img.style.display = i === index ? "block" : "none";
        });
    }

    window.openDeleteModal = function (button) {
        const photoContainer = button.closest('.photo-container');
        const modal = photoContainer.querySelector('.delete-modal');
        modal.style.display = 'flex';
    };

    window.closeDeleteModal = function (button) {
        const modal = button.closest('.delete-modal');
        modal.style.display = 'none';
    };

    prevBtn.addEventListener("click", () => {
        currentIndex = (currentIndex - 1 + photoContainers.length) % photoContainers.length;
        showImage(currentIndex);
    });

    nextBtn.addEventListener("click", () => {
        currentIndex = (currentIndex + 1) % photoContainers.length;
        showImage(currentIndex);
    });

    showImage(currentIndex);
});
